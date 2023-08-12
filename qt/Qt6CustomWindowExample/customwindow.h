#ifndef CUSTOMWINDOW_H
#define CUSTOMWINDOW_H

#include <QtWidgets/QWidget>
#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QFormLayout>
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

    QLineEdit *eventLineEdit;
    QLineEdit *messageLineEdit;
    QTextEdit *detailsTextEdit;
    QPushButton *detailsToggleBtn;
    QLineEdit *statusLineEdit;
    bool detailsCollapsed;
};

#endif // CUSTOMWINDOW_H
