/*
 * https://stackoverflow.com/questions/42328538/how-do-i-add-curses-to-cmake
 * https://exceptionshub.com/cmake-cant-find-curses.html
 * https://gist.github.com/xaizek -> list-picker.cpp
 */

#include <vector>
#include <ncursesw/cursesapp.h>


class App : public NCursesApplication
{
  std::vector<std::string> args;

public:
  App() : NCursesApplication(false)
  {
  }
  
  virtual void handleArgs(int argc, char *argv[])
  {
    args.assign(argv + 1, argv + argc);
  }
  
  virtual int run()
  {
    int answer = 0;
    return answer;
  }
};

int main(int argc, char* argv[]) {
  int answer;
  
  std::setlocale(LC_ALL, "");

  try {
    App app;
    app.handleArgs(argc, argv);
    answer = app();
    endwin();
  } catch (const NCursesException *e) {
    endwin();
    std::cerr << e->message << std::endl;
    answer = e->errorno;
  } catch (const NCursesException &e) {
    endwin();
    std::cerr << e.message << std::endl;
    answer = e.errorno;
  } catch (const std::exception &e) {
    endwin();
    std::cerr << "Exception: " << e.what() << std::endl;
    answer = EXIT_FAILURE;
  }
  return answer;
}
