#include <iostream>
#include <istream>
#include <fstream>
#include <string>
#include <vector>

enum class CSVState {
		     UnquotedField,
		     QuotedField,
		     QuotedQuote
};

typedef std::vector<std::vector<std::string>> table_t;

std::vector<std::string> readCSVRow(const std::string &row) {
  CSVState state = CSVState::UnquotedField;
  std::vector<std::string> fields {""};
  size_t i = 0; // index of the current field
  
  for (char c : row) {
    switch (state) {
    case CSVState::UnquotedField:
      switch (c) {
      case ',': // end of field
	fields.push_back(""); i++;
	break;
      case '"': state = CSVState::QuotedField;
	break;
      default:  fields[i].push_back(c);
	break; }
      break;
    case CSVState::QuotedField:
      switch (c) {
      case '"': state = CSVState::QuotedQuote;
	break;
      default:  fields[i].push_back(c);
	break; }
      break;
    case CSVState::QuotedQuote:
      switch (c) {
      case ',': // , after closing quote
	fields.push_back(""); i++;
	state = CSVState::UnquotedField;
	break;
      case '"': // "" -> "
	fields[i].push_back('"');
	state = CSVState::QuotedField;
	break;
      default:  // end of quote
	state = CSVState::UnquotedField;
	break; }
      break;
    }
  }
  return fields;
}

/// Read CSV file, Excel dialect. Accept "quoted fields ""with quotes"""
table_t readCSV(std::istream &in) {
  table_t table;
  std::string row;
  
  while (!in.eof()) {
    std::getline(in, row);
    if (in.bad() || in.fail()) {
      break;
    }
    auto fields = readCSVRow(row);
    table.push_back(fields);
  }
  return table;
}

void reverse_table(table_t& table) {
  std::vector<std::string> fields;
  int col, row = 0;
  
  for(; !table.empty(); table.pop_back()) {
    fields = table.back();
    col = 0;
    for(; !fields.empty(); fields.pop_back()) {
      std::string cell = fields.back();
      std::cout << "(" << row << "," << col << "): " << cell << std::endl;
      col++;
    }
    row++;
  }
}

int main(int argc, char* argv[]) {
  std::filebuf fb;

  if(fb.open(argv[argc-1], std::ios::in)) {
    std::istream csv_in(&fb);
    table_t parsed = readCSV(csv_in);
    fb.close();

    reverse_table(parsed);
  }
  
  return 0;
}
