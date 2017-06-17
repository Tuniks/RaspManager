#include <QDebug>
#include <QDir>
#include <QDirIterator>
#include "raspui.h"
#include "ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    ui->Path->setText(QDir::homePath());
}

MainWindow::~MainWindow(){
    delete ui;
}

void MainWindow::on_Execute_clicked(){
    QDirIterator it(ui->Path->text(), QDirIterator::NoIteratorFlags);
    while (it.hasNext()) {
        ui->Log->appendPlainText(it.next());

    }
}

