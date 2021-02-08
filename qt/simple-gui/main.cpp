#include <QApplication>
#include "widget.h"

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    Widget w;

    w.setName("Slim Shady");
    w.show();

    return a.exec();
}
