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

    QFormLayout *formLayout = new QFormLayout();

    eventLineEdit = new QLineEdit(this);
    eventLineEdit->setReadOnly(true);
    formLayout->addRow("Event:", eventLineEdit);

    messageLineEdit = new QLineEdit(this);
    messageLineEdit->setReadOnly(true);
    formLayout->addRow("Message:", messageLineEdit);

    detailsTextEdit = new QTextEdit(this);

    statusLineEdit = new QLineEdit(this);
    statusLineEdit->setReadOnly(true);
    formLayout->addRow("Status:", statusLineEdit);

    layout->addLayout(formLayout);

    detailsToggleBtn = new QPushButton("Show Details", this);
    connect(detailsToggleBtn, &QPushButton::clicked, this, &CustomWindow::toggleDetails);
    layout->addWidget(detailsToggleBtn);

    layout->addWidget(detailsTextEdit);
    detailsTextEdit->setVisible(false);

    setLayout(layout);

    detailsCollapsed = true;
}
