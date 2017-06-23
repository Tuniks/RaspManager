#include <QDebug>
#include <QDir>
#include <QDirIterator>
#include "raspui.h"
#include "ui_mainwindow.h"

QDir currentDir = QDir::homePath();

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    ui->Path->setText(currentDir.absolutePath());
    QObject::connect(ui->Path,SIGNAL(editingFinished()),this,SLOT(textChangedSlot()));
}

MainWindow::~MainWindow(){
    delete ui;
}

void MainWindow::on_Execute_clicked(){
    ui->Log->clear();
    QDirIterator it(currentDir, QDirIterator::NoIteratorFlags);
    while (it.hasNext()) {
        ui->Log->appendPlainText(it.next());

    }
}

void MainWindow::on_Back_clicked(){
    currentDir.cdUp();
    ui->Log->clear();
    ui->Path->setText(currentDir.absolutePath());
    QDirIterator it(currentDir, QDirIterator::NoIteratorFlags);
    while (it.hasNext()) {
        ui->Log->appendPlainText(it.next());

    }
}

 void MainWindow::textChangedSlot(){
    currentDir.cd(ui->Path->text());
 }
