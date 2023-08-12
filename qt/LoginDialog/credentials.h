#ifndef CREDENTIALS_H
#define CREDENTIALS_H

#include <QString>

class Credentials
{
public:
    Credentials(const QString& username, const QString& password)
        : username(username), password(password) {}

    QString getUsername() const { return username; }
    QString getPassword() const { return password; }

private:
    QString username;
    QString password;
};

#endif // CREDENTIALS_H
