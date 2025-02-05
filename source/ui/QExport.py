from __future__ import annotations

from PySide6.QtWidgets import (QPushButton, QDialog, QWidget, QFormLayout, QDateEdit, 
    QGridLayout, QGroupBox, QCalendarWidget, QFileDialog)
from PySide6.QtCore import QDateTime, QDate, Qt
from PySide6.QtGui import QPalette, QTextCharFormat

import csv
from os.path import exists

from core.core import generate_csv


class QCalendarRangeWidget(QCalendarWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.from_date = None
        self.to_date = None

        self.highlighter_format = QTextCharFormat()
        # get the calendar default highlight setting
        self.highlighter_format.setBackground(self.palette().brush(QPalette.Highlight))
        self.highlighter_format.setForeground(self.palette().color(QPalette.HighlightedText))

        super().dateTextFormat()

    def highlight_range(self, format):
        if self.from_date and self.to_date:
            d1 = min(self.from_date, self.to_date)
            d2 = max(self.from_date, self.to_date)
            while d1 <= d2:
                self.setDateTextFormat(d1, format)
                d1 = d1.addDays(1)
    
    def selectRange(self, date1: QDate, date2: QDate):
        self.highlight_range(QTextCharFormat())
        if date1 > date2:
            self.from_date = date1
            self.to_date = date2
        else:
            self.from_date = date2
            self.to_date = date1
        
        self.highlight_range(self.highlighter_format)


class QExport(QDialog):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setModal(True)
        self.resize(700, 500)
        self.today: QDate = QDateTime.currentDateTime().date()
        self.setStyleSheet("color: black;")

        # QGridLayout (#1)
        self.main_layout = QGridLayout(self)

        # QGroupBox (#2)
        self.previewBox = QGroupBox(self)
        self.main_layout.addWidget(self.previewBox, 0, 0, Qt.AlignmentFlag.AlignTop)
        self.calandrier_layout = QGridLayout(self.previewBox)
        self.calandrier = QCalendarRangeWidget(self)
        self.calandrier_layout.addWidget(self.calandrier, 0, 0, Qt.AlignmentFlag.AlignCenter)
        self.calandrier.setCurrentPage(self.today.year(), self.today.month())
        self.calandrier.setSelectionMode(QCalendarWidget.SelectionMode.NoSelection)

        # QGroupBox (#2)
        self.optionBox = QGroupBox(self)
        self.main_layout.addWidget(self.optionBox, 0, 1, Qt.AlignmentFlag.AlignTop)

        self.form = QFormLayout(self.optionBox)
        self.optionBox.setLayout(self.form)

        self.date_depart = QDateEdit(self)
        monday = self.get_monday()
        self.date_depart.setDate(monday)
        self.form.addRow("Date de départ", self.date_depart)
        #! TODO: make sure date_fin is always greater or equal to date_depart
        self.date_fin = QDateEdit(self)
        self.date_fin.setDate(self.today)
        self.form.addRow("Date de fin", self.date_fin)

        self.exporter_button = QPushButton(self)
        self.exporter_button.setText("Exporter")
        self.exporter_button.clicked.connect(self.exporter)
        self.exporter_button.adjustSize()
        self.exporter_button.move(
            self.width() - self.exporter_button.width() - 10, 
            self.height() - self.exporter_button.height() - 10)

        self.date_depart.dateChanged.connect(self.update_range)
        self.date_fin.dateChanged.connect(self.update_range)
        self.update_range()
    
    def exporter(self: QExport):
        enregistrer_fichier = QFileDialog(self, caption="Enregistrer sous")
        enregistrer_fichier.setFileMode(QFileDialog.FileMode.Directory)
        enregistrer_fichier.setOption(QFileDialog.Option.ShowDirsOnly, True)

        if enregistrer_fichier.exec():
            folder = enregistrer_fichier.selectedFiles()[0]
            depart = self.date_depart.date().toString("dd-MM-yyyy")
            fin = self.date_fin.date().toString("dd-MM-yyyy")
            fichier = f"/livre_comptes_{depart}_{fin}"
            
            self.exporter_as_csv(folder + fichier)
        
        self.close()
    
    def exporter_as_csv(self: QExport, filename):
        filename += ".csv"

        depart = self.date_depart.date()
        fin = self.date_fin.date()
        diff = depart.daysTo(fin) + 1
        dates: list[str] = []
        for i in range(diff):
            dates.append(depart.addDays(i).toString("dd/MM/yyyy"))

        donnees = generate_csv(dates)

        if exists(filename):
            mode = "w"
        else:
            mode = "a"

        with open(filename, mode, newline='', encoding="utf8") as file:
            try:
                writer = csv.writer(file)
                writer.writerows(donnees)
            finally:
                file.close()
    
    def get_monday(self: QExport):
        if self.today.dayOfWeek() > 1:
            return self.today.addDays(-self.today.dayOfWeek() + 1)
        else:
            return self.today
    
    def update_range(self: QExport):
        depart = self.date_depart.date()
        fin = self.date_fin.date()
        
        self.calandrier.selectRange(depart, fin)
