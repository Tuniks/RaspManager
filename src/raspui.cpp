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
    connect(ui->Path,SIGNAL(editingFinished()),this,SLOT(textChangedSlot()));
    //changing context menu policy and connecting signal-slot
    ui->Log->setContextMenuPolicy(Qt::CustomContextMenu);
    connect(ui->Log, SIGNAL(customContextMenuRequested(QPoint)),this,SLOT(showContextMenu(QPoint)));
    connect(ui->Log, SIGNAL(itemDoubleClicked(QListWidgetItem*)), this, SLOT(onItemDoubleClicked(QListWidgetItem*)));

}

MainWindow::~MainWindow(){
    delete ui;
}

void MainWindow::on_Execute_clicked(){
    ui->Log->clear();
    ui->Path->setText(currentDir.absolutePath());
    QDirIterator it(currentDir, QDirIterator::NoIteratorFlags);
    while (it.hasNext()) {
        ui->Log->addItem(it.next());
    }
}

void MainWindow::on_Back_clicked(){
    currentDir.cdUp();
    on_Execute_clicked();
}

 void MainWindow::textChangedSlot(){
    currentDir.cd(ui->Path->text());
    //on_Execute_clicked();
 }

 void MainWindow::showContextMenu(const QPoint &pos){
     QPoint globalPos = ui->Log-> mapToGlobal(pos);
     QMenu dropMenu;
     dropMenu.addAction("Delete", this, SLOT(eraseItem()));
     dropMenu.exec(globalPos);
 }

 void MainWindow::eraseItem(){
     //TODO Handle error, progress bar, pop up window
     for (int i=0; i < ui->Log->selectedItems().size(); i++){
         QListWidgetItem *item = ui->Log->takeItem(ui->Log->currentRow());
         QDir dirToDelete(item->text());
         dirToDelete.removeRecursively();
         delete item;
     }

 }

 void MainWindow::onItemDoubleClicked(QListWidgetItem *item){
     currentDir.cd(item->text());
     on_Execute_clicked();

 }
