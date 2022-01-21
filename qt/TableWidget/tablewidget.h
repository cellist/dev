#ifndef TABLEWIDGET_H
#define TABLEWIDGET_H

#include <QMainWindow>
#include <QTableWidgetItem>

QT_BEGIN_NAMESPACE
namespace Ui { class TableWidget; }
QT_END_NAMESPACE

class TableWidget : public QMainWindow
{
    Q_OBJECT

public:
    TableWidget(QWidget *parent = nullptr);
    ~TableWidget();

private slots:
    void on_okButton_clicked();

    void on_cancelButton_clicked();

    void on_tableWidget_currentCellChanged(int currentRow, int currentColumn, int previousRow, int previousColumn);

    void on_tableWidget_itemEntered(QTableWidgetItem *item);

private:
    void displayStatus(const QString& text, bool append);
    Ui::TableWidget *ui;
};
#endif // TABLEWIDGET_H
