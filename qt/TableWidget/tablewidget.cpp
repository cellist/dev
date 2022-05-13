#include <QTextStream>
#include "tablewidget.h"
#include "ui_tablewidget.h"

typedef struct {
    const char*    article;
    unsigned short quantity;
    double         price;
} article_t;

TableWidget::TableWidget(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::TableWidget)
{
    QTableWidget     *tab;
    QTableWidgetItem *cell;
    char buf[10];
    article_t data[] = {
        { .article = "apple",     .quantity = 5, .price = 2.85 },
        { .article = "pear",      .quantity = 8, .price = 5.84 },
        { .article = "banana",    .quantity = 3, .price = 2.74 },
        { .article = "bun",       .quantity = 4, .price = 1.80 },
        { .article = "pineapple", .quantity = 2, .price = 3.90 },
        { .article = "yoghurt",   .quantity = 8, .price = 4.10 }
    };

    ui->setupUi(this);
    tab = ui->tableWidget;

    for(unsigned short r = 0; r < sizeof(data)/sizeof(article_t); r++) {
        tab->insertRow(r);
        cell = new QTableWidgetItem(tr(data[r].article));
        tab->setItem(r, 0, cell);

        snprintf(buf, sizeof(buf)-1, "%d", data[r].quantity);
        cell = new QTableWidgetItem(tr(buf));
        tab->setItem(r, 1, cell);

        snprintf(buf, sizeof(buf)-1, "%4.2f", data[r].price);
        cell = new QTableWidgetItem(tr(buf));
        tab->setItem(r, 2, cell);
    }
}

TableWidget::~TableWidget()
{
    ui->tableWidget->clear();
    delete ui;
}


void TableWidget::on_okButton_clicked()
{
    this->close();
}

void TableWidget::on_cancelButton_clicked()
{
    this->close();
}

void TableWidget::displayStatus(const QString& text, bool append=true)
{
    if(!append) ui->plainTextEdit->clear();
    ui->plainTextEdit->appendPlainText(text);
}

void TableWidget::on_tableWidget_currentCellChanged(int currentRow, int currentColumn, int previousRow, int previousColumn)
{
    QString event;
    QTextStream(&event) << "EVENT[cell changed]: (" << previousRow << "," << previousColumn
                        << ") -> (" << currentRow << "," << currentColumn << ")";
    this->displayStatus(event);
}

void TableWidget::on_tableWidget_itemEntered(QTableWidgetItem *item)
{
    QString event;
    QTextStream(&event) << "EVENT[item entered]: (" << item->row() << "," << item->column() << ")";
    this->displayStatus(event, false);
}
