#include <QApplication>
#include <QMessageBox>
#include <QFont>
#include "login_dialog.h"

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);

    // Set the serif font
    QFont serifFont("Times", 12, QFont::Normal);

    LoginDialog loginDialog;
    if (loginDialog.exec() == QDialog::Accepted)
    {
        Credentials credentials = loginDialog.getCredentials();
        QString username = credentials.getUsername();
        QString password = credentials.getPassword();

        // Display the entered username and password using a QMessageBox
        QMessageBox msgBox;
        msgBox.setWindowTitle("Entered Credentials");
        msgBox.setText("Username: " + username);
        msgBox.setDetailedText("Password: " + password);
        msgBox.setFont(serifFont); // Set the serif font
        msgBox.exec();
    }

    return 0;
}
