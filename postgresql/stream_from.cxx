#include <iostream>
#include <pqxx/pqxx>

int main()
{  
  try
  {
    pqxx::connection conn("postgresql://<user>:<pass>@<host>:<port>/<db>");
    std::cout << "Connected as " << conn.username()
	      << "@" << conn.hostname()
	      << ":" << conn.port()
	      << "/" << conn.dbname() << std::endl;

    // Start a transaction.  In libpqxx, you always work in one.
    pqxx::work txn(conn);
    std::tuple <int, std::string, std::string> row;
    pqxx::stream_from stream(
			     txn,
			     "SELECT id, aconcept, atag "
			     " FROM tags"
			     " WHERE atag NOT LIKE '%e%'"
			     );
    txn.commit();

    while(stream >> row)
      {
	int         theId      = std::get<0>(row);
	std::string theConcept = std::get<1>(row);
	std::string theTag     = std::get<2>(row);

	std::cout << "|" << theId
		  << "| " << theConcept
		  << " | " << theTag
		  << " |" << std::endl;
      }
    stream.complete();
  }
  catch (std::exception const &e)
  {
    std::cerr << e.what() << std::endl;
    return 1;
  }
  
  return 0;
}
