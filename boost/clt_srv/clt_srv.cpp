#include <boost/asio/io_service.hpp>
#include <boost/asio/write.hpp>
#include <boost/asio/buffer.hpp>
#include <boost/asio/ip/tcp.hpp>
#include <chrono>
#include <iostream>
#include <boost/exception/all.hpp>
#include <exception>
#include <thread>
#include <array>
#include <boost/asio.hpp>

namespace ba = boost::asio;
  
void server()
{
  std::array<char, 4096> bytes;
  ba::io_service io;
  ba::ip::tcp::acceptor acc(io, ba::ip::tcp::endpoint(ba::ip::tcp::v4(), 5006));
  ba::ip::tcp::socket skt(io);
  
  std::cout << "server listening" << std::endl;
  acc.listen();
  acc.accept(skt);
  std::cout << "server accepted" << std::endl;
  // now the connection is made and we can send and receive data
  // send
  for (;;) {
    skt.write_some(ba::buffer("message from server"));
    std::cout << "server writing" << std::endl;
    skt.read_some(ba::buffer(bytes));
    std::cout << "server reading" << std::endl;
  }
}

void client()
{
  std::array<char, 4096> bytes;
  ba::io_service io;
  ba::ip::tcp::resolver::query qury{ "localhost", "5006" };
  ba::ip::tcp::resolver rslv(io);
  ba::ip::tcp::socket skt(io);
  boost::system::error_code error_ = ba::error::host_not_found;
  auto it = rslv.resolve(qury, error_);
  ba::ip::tcp::resolver::iterator end;
  
  std::cout << "client try to connect" << std::endl;
  ba::connect(skt, it);
  
  std::cout << "client connected" << std::endl;
  //now we are connected
  //read data!
  
  for (;;) {
    skt.write_some(ba::buffer("message from client "));
    std::cout << "client writing" << std::endl;
    skt.read_some(ba::buffer(bytes));
    std::cout << "client reading" << std::endl;
  }
}

int main()
{
  std::thread t1{ &client }, t2{ &server };
  t1.join();
  t2.join();
  std::cin.get();
}
