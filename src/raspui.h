#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QListWidget>

namespace Ui {
    class MainWindow;
}

class MainWindow : public QMainWindow{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow();

private slots:
    void on_Execute_clicked();
    void on_Back_clicked();
    void showContextMenu(const QPoint&);
    void eraseItem();
    void createItem();
    void onItemDoubleClicked(QListWidgetItem*);

public slots:
    void textChangedSlot();


private:
    Ui::MainWindow *ui;
};

#endif // MAINWINDOW_H
