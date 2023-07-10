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
    pqxx::connection c(
		       "user=<username> "
		       "host=<hostname> "
		       "password=<secret> "
		       "dbname=<database name>"
		       );

    std::cout << "Connected as " << c.username()
	      << "/" << c.dbname()
	      << "@" << c.hostname()
	      << ":" << c.port() << std::endl;

    // Start a transaction.  In libpqxx, you always work in one.
    pqxx::work w(c);
    pqxx::result result = w.exec(
				 "SELECT id, aconcept, atag "
				 " FROM tags"
				 " WHERE atag NOT LIKE '%e%'"
				 );
    w.commit();

    for (auto row = std::begin(result); row != std::end(result); row++)
      {
	std::cout << "| ";
	for (auto field = std::begin(row); field != std::end(row); field++)
	  {
	    std::cout << field->c_str() << " | ";
	  }
	std::cout << std::endl;
      }
  }
  catch (std::exception const &e)
  {
    std::cerr << e.what() << std::endl;
    return 1;
  }
  
  return 0;
}
