#include <iostream>
#include <pqxx/pqxx>

int main()
{  
  try
  {
    // Connect to the database.  In practice we may have to pass some
    // arguments to say where the database server is, and so on.
    // The constructor parses options exactly like libpq's
    // PQconnectdb/PQconnect, see:
    // https://www.postgresql.org/docs/10/static/libpq-connect.html
    pqxx::connection c;

    // Start a transaction.  In libpqxx, you always work in one.
    pqxx::work w(c);
    pqxx::result result = w.exec(
				 "SELECT id, anobject, atag "
				 " FROM tags"
				 " WHERE atag NOT LIKE '%e%'"
				 );
    w.commit();

    for(auto const &row: result)
      {
	int col1 = row[0].as<int>();
	std::string col2 = row[1].as<std::string>();
	std::string col3 = row[2].as<std::string>();
	
	std::cout << col1 << "|" << col2 << "|" << col3 << std::endl;
      }
  }
  catch (std::exception const &e)
  {
    std::cerr << e.what() << std::endl;
    return 1;
  }
  
  return 0;
}
