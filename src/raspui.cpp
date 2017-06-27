#include <QDebug>
#include <QDir>
#include <QDirIterator>
#include <QMessageBox>
#include <QInputDialog>
#include "raspui.h"
#include "ui_mainwindow.h"

QDir currentDir = QDir::homePath();

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    ui->Path->setText(currentDir.absolutePath());
    ui->Log->setSelectionMode(QAbstractItemView::ExtendedSelection);
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
    QDirIterator it(currentDir, QDirIterator::NoIteratorFlags);
    while (it.hasNext()) {
        ui->Log->addItem(it.next());
    }
}

void MainWindow::on_Back_clicked(){
    currentDir.cdUp();
    on_Execute_clicked();
    ui->Path->setText(currentDir.absolutePath());
}

 void MainWindow::textChangedSlot(){
    currentDir.cd(ui->Path->text());
    on_Execute_clicked();
 }

 void MainWindow::showContextMenu(const QPoint &pos){
     QPoint globalPos = ui->Log-> mapToGlobal(pos);
     QMenu dropMenu;
     dropMenu.addAction("Delete", this, SLOT(eraseItem()));
     dropMenu.addAction("Create", this, SLOT(createItem()));
     dropMenu.exec(globalPos);
 }

 void MainWindow::eraseItem(){                  //TODO Handle error, progress bar
     QMessageBox::StandardButton confirmation;
     QList<QListWidgetItem*> items = ui->Log->selectedItems();
     foreach(QListWidgetItem * item, items){
        confirmation = QMessageBox::question(this, "RASP", "Are you sure you want to delete "+ item->text(), QMessageBox::Yes|QMessageBox::No);
        if(confirmation == QMessageBox::Yes){
            QDir dirToDelete(item->text());
            dirToDelete.removeRecursively();
            delete item;
         }
     }
 }

 void MainWindow::createItem(){
    bool ok;
    QMessageBox::StandardButton info;
    QString dirName = QInputDialog::getText(this, "RASP", "Directory Name:", QLineEdit::Normal, "", &ok);
    if(ok && !dirName.isEmpty()){
        if(currentDir.mkdir(dirName)){
            info = QMessageBox::information(this, "RASP", "Directory successfully created.");
        }
        else
            info = QMessageBox::information(this, "RASP", "Directory could not be created.");
    }
 }

 void MainWindow::onItemDoubleClicked(QListWidgetItem *item){
     currentDir.cd(item->text());
     on_Execute_clicked();
     ui->Path->setText(currentDir.absolutePath());
 }
