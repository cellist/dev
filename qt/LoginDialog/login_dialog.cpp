#include "login_dialog.h"
#include "credentials.h"
#include <QFormLayout>
#include <QLineEdit>
#include <QPushButton>
#include <QFont>

LoginDialog::LoginDialog(QWidget *parent) :
    QDialog(parent)
{
    setWindowTitle("Login");

    usernameLineEdit = new QLineEdit(this);
    passwordLineEdit = new QLineEdit(this);
    passwordLineEdit->setEchoMode(QLineEdit::Password);

    loginButton = new QPushButton("Login", this);

    // Create a larger font and apply it to all the widgets and layouts
    QFont largerFont;
    largerFont.setPointSize(14); // Change the size as needed
    usernameLineEdit->setFont(largerFont);
    passwordLineEdit->setFont(largerFont);
    loginButton->setFont(largerFont);

    QFormLayout *formLayout = new QFormLayout;
    formLayout->addRow("Username:", usernameLineEdit);
    formLayout->addRow("Password:", passwordLineEdit);

    QHBoxLayout *buttonLayout = new QHBoxLayout;
    buttonLayout->addStretch();
    buttonLayout->addWidget(loginButton);

    QVBoxLayout *mainLayout = new QVBoxLayout(this);
    mainLayout->addLayout(formLayout);
    mainLayout->addStretch();
    mainLayout->addLayout(buttonLayout);

    connect(loginButton, &QPushButton::clicked, this, &LoginDialog::onLoginButtonClicked);
}

LoginDialog::~LoginDialog()
{
    // No need to manually delete UI elements as Qt handles the cleanup
}

Credentials LoginDialog::getCredentials() const
{
    QString username = usernameLineEdit->text();
    QString password = passwordLineEdit->text();

    return Credentials(username, password);
}

void LoginDialog::onLoginButtonClicked()
{
    accept(); // Close the dialog and return QDialog::Accepted
}
