#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>

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
public slots:
    void textChangedSlot();

private:
    Ui::MainWindow *ui;
};

#endif // MAINWINDOW_H
