#include "customwindow.h"

CustomWindow::CustomWindow(QWidget *parent) : QWidget(parent) {
    setupUI();
}

void CustomWindow::setEvent(const QString &event) {
    eventLineEdit->setText(event);
}

void CustomWindow::setMessage(const QString &message) {
    messageLineEdit->setText(message);
}

void CustomWindow::setDetails(const QString &details) {
    detailsTextEdit->setPlainText(details);
}

void CustomWindow::setStatus(const QString &status) {
    statusLineEdit->setText(status);
}

void CustomWindow::toggleDetails() {
    detailsCollapsed = !detailsCollapsed;
    if (detailsCollapsed) {
        detailsTextEdit->setVisible(false);
        detailsToggleBtn->setText("Show Details");
    } else {
        detailsTextEdit->setVisible(true);
        detailsToggleBtn->setText("Hide Details");
    }
}

void CustomWindow::setupUI() {
    QVBoxLayout *layout = new QVBoxLayout(this);

    eventLabel = new QLabel("Events:", this);
    layout->addWidget(eventLabel);

    eventLineEdit = new QLineEdit(this);
    eventLineEdit->setReadOnly(true);
    layout->addWidget(eventLineEdit);

    messageLabel = new QLabel("Message:", this);
    layout->addWidget(messageLabel);

    messageLineEdit = new QLineEdit(this);
    messageLineEdit->setReadOnly(true);
    layout->addWidget(messageLineEdit);

    detailsToggleBtn = new QPushButton("Show Details", this);
    connect(detailsToggleBtn, &QPushButton::clicked, this, &CustomWindow::toggleDetails);
    layout->addWidget(detailsToggleBtn);

    detailsTextEdit = new QTextEdit(this);
    layout->addWidget(detailsTextEdit);
    detailsTextEdit->setVisible(false);

    statusLabel = new QLabel("Status:", this);
    layout->addWidget(statusLabel);

    statusLineEdit = new QLineEdit(this);
    statusLineEdit->setReadOnly(true);
    layout->addWidget(statusLineEdit);

    setLayout(layout);

    detailsCollapsed = true;
}
