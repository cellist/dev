#include "widget.h"
#include "ui_widget.h"

Widget::Widget(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::Widget)
{
    ui->setupUi(this);
}

Widget::~Widget()
{
    delete ui;
}

void Widget::setName(const QString &name)
{
 ui->lineEdit->setText(name);
}

QString Widget::name() const
{
 return ui->lineEdit->text();
}
