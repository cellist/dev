#include <QApplication>
#include "login_dialog.h"

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);

    LoginDialog loginDialog;
    if (loginDialog.exec() == QDialog::Accepted)
    {
        Credentials credentials = loginDialog.getCredentials();
        // You can use the entered credentials here
        QString username = credentials.getUsername();
        QString password = credentials.getPassword();
        // Perform login validation or other actions with the credentials
    }

    return 0;
}
