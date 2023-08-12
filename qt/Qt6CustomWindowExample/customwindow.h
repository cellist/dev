#ifndef CUSTOMWINDOW_H
#define CUSTOMWINDOW_H

#include <QtWidgets/QWidget>
#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QHBoxLayout>
#include <QtWidgets/QLabel>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QTextEdit>
#include <QtWidgets/QLineEdit>

class CustomWindow : public QWidget {
    Q_OBJECT

public:
    CustomWindow(QWidget *parent = nullptr);

    void setEvent(const QString &event);
    void setMessage(const QString &message);
    void setDetails(const QString &details);
    void setStatus(const QString &status);

private slots:
    void toggleDetails();

private:
    void setupUI();

    QLabel *eventLabel;
    QLabel *messageLabel;
    QPushButton *detailsToggleBtn;
    QTextEdit *detailsTextEdit;
    QLabel *statusLabel;
    QLineEdit *eventLineEdit;
    QLineEdit *messageLineEdit;
    QLineEdit *statusLineEdit;
    bool detailsCollapsed;
};

#endif // CUSTOMWINDOW_H
