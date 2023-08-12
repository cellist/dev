#include <QtWidgets/QApplication>
#include "customwindow.h"

class Watchdog {
public:
    Watchdog(CustomWindow *window) : window(window) {}

    void simulateEvent() {
        window->setEvent("An event occurred");
        window->setMessage("This is a message");
        window->setDetails("These are the message details");
        window->setStatus("Status is fine");
    }

private:
    CustomWindow *window;
};

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);

    CustomWindow window;
    window.setWindowTitle("Qt6 Custom Window");
    window.setGeometry(100, 100, 600, 400);
    window.show();

    Watchdog watchdog(&window);
    watchdog.simulateEvent();

    return app.exec();
}
