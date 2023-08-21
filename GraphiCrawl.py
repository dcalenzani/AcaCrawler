# Form implementation generated from reading ui file 'AcaCrawl.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt
from acaCrawler import get_current_page, get_data, get_soup, get_total_articles, get_total_pages, create_csv, Article, articles, scrape_articles_data, update_url
import time

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Crawler Académico")
        Form.resize(650, 298)
        self.RBSelection = QtWidgets.QRadioButton(parent=Form)
        self.RBSelection.setGeometry(QtCore.QRect(390, 170, 201, 20))
        self.RBSelection.setObjectName("RBSelection")
        self.RBSelection.setChecked(True)
        self.RBSelection.toggled.connect(self.select_all)

        self.SearchButton = QtWidgets.QPushButton(parent=Form)
        self.SearchButton.setGeometry(QtCore.QRect(430, 250, 80, 22))
        self.SearchButton.setObjectName("SearchButton")
        self.SearchButton.clicked.connect(self.run_search)

        self.ExportButton = QtWidgets.QPushButton(parent=Form)
        self.ExportButton.setGeometry(QtCore.QRect(530, 250, 80, 22))
        self.ExportButton.setObjectName("ExportButton")
        self.ExportButton.clicked.connect(self.run_export)

        self.SearchLine = QtWidgets.QLineEdit(parent=Form)
        self.SearchLine.setGeometry(QtCore.QRect(50, 60, 561, 22))
        self.SearchLine.setObjectName("SearchLine")
        
        self.SearchLabel = QtWidgets.QLabel(parent=Form)
        self.SearchLabel.setGeometry(QtCore.QRect(60, 30, 131, 16))
        self.SearchLabel.setObjectName("SearchLabel")
        
        self.SelectionLabel = QtWidgets.QLabel(parent=Form)
        self.SelectionLabel.setGeometry(QtCore.QRect(390, 130, 141, 16))
        self.SelectionLabel.setObjectName("SelectionLabel")
        
        self.PagesNumber = QtWidgets.QSpinBox(parent=Form)
        self.PagesNumber.setGeometry(QtCore.QRect(390, 210, 43, 23))
        self.PagesNumber.setObjectName("PagesNumber")
        self.PagesNumber.setEnabled(False)
        
        self.ComsLabel = QtWidgets.QTextBrowser(parent=Form)
        self.ComsLabel.setGeometry(QtCore.QRect(50, 100, 301, 81))
        self.ComsLabel.setObjectName("ComsLabel")
        
        self.PagesLabel = QtWidgets.QLabel(parent=Form)
        self.PagesLabel.setGeometry(QtCore.QRect(460, 210, 57, 21))
        self.PagesLabel.setObjectName("PagesLabel")
        
        self.ComsLabel_2 = QtWidgets.QTextBrowser(parent=Form)
        self.ComsLabel_2.setGeometry(QtCore.QRect(50, 190, 301, 81))
        self.ComsLabel_2.setObjectName("ComsLabel_2")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def run_search(self):
        search_url = update_url(self.SearchLine.text(),1,1)
        total_articles = get_total_articles(search_url)
        total_pages = get_total_pages(search_url)
        printable = f"Encontramos un total de: {total_articles} artículos\nEstan separados en {total_pages} páginas\n\nUrl de referencia: {search_url}"

        self.ComsLabel.setText(printable)

    def run_export(self):
        def progress_printer(message):
            progress_output = message
            #print(progress_output)

        if self.RBSelection.isChecked():
            print("procesando todos")
            search_url = update_url(self.SearchLine.text(),1,1)
            total_pages = int(get_total_pages(search_url))
            all_articles = scrape_articles_data(self.SearchLine.text(),total_pages, progress_printer)
            output = f'Articulos tabulados: {len(all_articles)}'
            # CSV function invocation
            create_csv(self.SearchLine.text(), all_articles)
            self.ComsLabel_2.setText(output + "\nCSV creado de manera existosa!")
        else:
            pages_selected = self.PagesNumber.value()
            all_articles = scrape_articles_data(self.SearchLine.text(),pages_selected, progress_printer)
            output = f'Articulos tabulados:  {len(all_articles)}'
            # CSV function invocation
            create_csv(self.SearchLine.text(), all_articles)
            self.ComsLabel_2.setText(output + "\nCSV creado de manera existosa!")

    def select_all(self):
        if self.RBSelection.isChecked():
            self.PagesNumber.setEnabled(False)
        else:                        
            self.PagesNumber.setEnabled(True)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Crawler Académico"))
        self.RBSelection.setText(_translate("Form", "Todas las páginas"))
        self.SearchButton.setText(_translate("Form", "Buscar"))
        self.ExportButton.setText(_translate("Form", "Exportar"))
        self.SearchLabel.setText(_translate("Form", "Ingrese su búsqueda"))
        self.SelectionLabel.setText(_translate("Form", "Páginas a descargar:"))
        self.PagesLabel.setText(_translate("Form", "Paginas"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec())
