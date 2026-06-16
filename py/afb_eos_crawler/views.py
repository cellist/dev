import json
from collections import defaultdict
from models import MatchResult, STATUS_ICON, Variant

def print_report(results: list[MatchResult]) -> None:
    by_brand = defaultdict(list)
    for r in results: by_brand[r.brand].append(r)

    total = sum(len(v) for v in by_brand.values())
    print("\n" + "=" * 60)
    print(f"  AfB Shop x /e/OS Tablet Compatibility Report")
    print(f"  {total} compatible tablet model(s) found")
    print("=" * 60)

    for brand in sorted(by_brand.keys()):
        entries = sorted(by_brand[brand], key=lambda r: r.eos_device.model)
        print(f"\n  {brand} ({len(entries)} model(s))")
        for r in entries:
            icon = STATUS_ICON.get(r.eos_device.status, "[?]")
            if r.variants:
                best_v = r.variants[0]
                extra = f" (+{len(r.variants) - 1} more)" if len(r.variants) > 1 else ""
                print(f"     {icon:<12} {r.eos_device.model:<30} [{r.eos_device.codename}] -> {best_v.zustand} @ {best_v.price}{extra}")
            else:
                print(f"     {icon:<12} {r.eos_device.model:<30} [{r.eos_device.codename}] -> No stock/price data")
    print("=" * 60)

def print_changes(changes_log: list[str]) -> None:
    if not changes_log:
        print("\n  No changes detected since last run.")
        return
    print("\n" + "=" * 60)
    print("  CHANGE DETECTION REPORT")
    print("=" * 60)
    for change in changes_log:
        print(f"  {change}")
    print("=" * 60)

def save_json(results: list[MatchResult], filename: str = "afb_eos_results.json") -> None:
    output = [
        {
            "afb_url": r.slug,
            "brand": r.brand,
            "eos_model": r.eos_device.model,
            "eos_codename": r.eos_device.codename,
            "eos_status": r.eos_device.status,
            "eos_android_versions": r.eos_device.android_versions,
            "variants": [{"zustand": v.zustand, "price": v.price} for v in (r.variants or [])]
        }
        for r in results
    ]
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"\n  Results saved to {filename}")

def save_ods(results: list[MatchResult], filename: str = "afb_eos_results.ods") -> None:
    from odf.opendocument import OpenDocumentSpreadsheet
    from odf.style import Style, TextProperties, TableColumnProperties, TableCellProperties
    from odf.table import Table, TableColumn, TableRow, TableCell, TableHeaderRows, DatabaseRange, DatabaseRanges
    from odf.text import P
    from odf import text as odftext

    doc = OpenDocumentSpreadsheet()

    def _make_style(name: str, bold: bool = False, bg: str = "", wrap: bool = False) -> Style:
        style = Style(name=name, family="table-cell")
        if bold: style.addElement(TextProperties(fontweight="bold"))
        if bg or wrap:
            tcp = {}
            if bg: tcp["backgroundcolor"] = bg
            if wrap: tcp["wrapoption"] = "wrap"
            style.addElement(TableCellProperties(**tcp))
        doc.automaticstyles.addElement(style)
        return style

    header_style = _make_style("HeaderCell", bold=True, bg="#1c4587")
    url_style = _make_style("UrlCell", wrap=True)
    normal_style = _make_style("NormalCell")
    alt_style = _make_style("AltCell", bg="#e8f0fe")

    header_text_style = Style(name="HeaderText", family="text")
    header_text_style.addElement(TextProperties(color="#ffffff", fontweight="bold"))
    doc.automaticstyles.addElement(header_text_style)

    col_widths = ["3cm", "6cm", "4cm", "5cm", "3cm", "4cm", "4cm", "10cm"]
    table = Table(name="afb-eos")
    for i, w in enumerate(col_widths):
        cs = Style(name=f"Col{i}", family="table-column")
        cs.addElement(TableColumnProperties(columnwidth=w))
        doc.automaticstyles.addElement(cs)
        table.addElement(TableColumn(stylename=f"Col{i}"))

    headers = ["Brand", "Device", "Codename", "/e/OS Android Version", "Build Type", "Zustand", "Price (EUR)", "AfB Shop URL"]
    header_row = TableRow()
    for h in headers:
        cell = TableCell(stylename=header_style, valuetype="string")
        p = P()
        p.addElement(odftext.Span(stylename=header_text_style, text=h))
        cell.addElement(p)
        header_row.addElement(cell)

    header_rows_block = TableHeaderRows()
    header_rows_block.addElement(header_row)
    table.addElement(header_rows_block)

    sorted_results = sorted(results, key=lambda r: (r.brand, r.eos_device.model))
    total_rows = 1
    
    for r in sorted_results:
        url = r.slug if r.slug.startswith("http") else "https://www.afbshop.de/gebrauchte-tablets/"
        
        # FIXED: Use Variant objects instead of dictionaries
        variants_to_export = r.variants if r.variants else [Variant(zustand="Unknown", price="See website")]
        
        for v in variants_to_export:
            row_style = alt_style if total_rows % 2 == 0 else normal_style
            
            # FIXED: Access attributes via dot notation (v.zustand) instead of dictionary keys
            row_data = [r.brand, r.eos_device.model, r.eos_device.codename, r.eos_device.android_versions or "See doc.e.foundation", r.eos_device.status, v.zustand, v.price, url]

            data_row = TableRow()
            for col_idx, value in enumerate(row_data):
                cell_style = url_style if col_idx == 7 else row_style
                cell = TableCell(stylename=cell_style, valuetype="string")
                
                if col_idx == 6 and value not in ("See website", ""):
                    try:
                        float_val = float(value.replace(" EUR", "").replace(",", "."))
                        cell = TableCell(stylename=cell_style, valuetype="float", value=str(float_val))
                        cell.addElement(P(text=f"{float_val:.2f}"))
                    except ValueError:
                        cell.addElement(P(text=value))
                else:
                    cell.addElement(P(text=value))
                data_row.addElement(cell)
            table.addElement(data_row)
            total_rows += 1

    doc.spreadsheet.addElement(table)
    col_letter = chr(ord("A") + len(headers) - 1)
    db_ranges = DatabaseRanges()
    db_ranges.addElement(DatabaseRange(name="__AutoFilter__", targetrangeaddress=f"afb-eos.A1:{col_letter}{total_rows}", displayfilterbuttons="true"))
    doc.spreadsheet.addElement(db_ranges)

    doc.save(filename)
    print(f"\n  Spreadsheet saved to {filename}  ({total_rows - 1} data rows)")
