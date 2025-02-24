from __future__ import annotations

from PySide6.QtWidgets import (QWidget, QFrame, QScrollArea, QVBoxLayout, 
    QDateEdit, QHBoxLayout, QLabel, QLayout, QSizePolicy, QGridLayout, 
    QPushButton, QSpacerItem, QMessageBox)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QDateTime, QDate, QEvent, Signal
from core.core import get_commande, delete_commande
from core.Produit import CommandeData
import sys


class Commande(QFrame):
    deleted = Signal()
    
    def __init__(self: Commande, parent: QWidget, commande: CommandeData) -> None:
        super().__init__(parent)
        self.setFixedSize(400, 70)
        self.commande = commande
        self.setStyleSheet(
            """
            QFrame{
                border-radius: 10px;
                border: 1px solid black;
            } 
            QLabel { 
                border: none;
                color: black;
            }
            """)

        self.div = QGridLayout(self)
        
        self.identifiant = QLabel(self)
        self.identifiant.setStyleSheet("font-size: 20px; text-decoration: underline; font: bold;")
        self.identifiant.setText(f"Commande {self.commande.id_commande}")
        self.div.addWidget(self.identifiant, 0, 0, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)


        self.spacer = QSpacerItem(1, 1, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.div.addItem(self.spacer, 0, 1, 2, 1)

        self.total = QLabel(self)
        self.total.setStyleSheet("font-size: 20px; font: bold;")
        self.total.setText("{:.2f} €".format(self.commande.total))
        self.div.addWidget(self.total, 0, 2, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)

        self.date_heure = QLabel(self)
        self.date_heure.setText(f"Le {self.commande.date} à {self.commande.heure}")
        self.div.addWidget(self.date_heure, 1, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignLeft)

        self.delete_button = QPushButton(self)
        self.delete_button.setIcon(QIcon(sys.path[0] + "\\assets\\delete.png"))
        self.delete_button.clicked.connect(self.delete_commande)
        self.delete_button.setFixedSize(30, 30)
        self.delete_button.setStyleSheet("border: none;")
        self.div.addWidget(self.delete_button, 0, 4, 2, 1, alignment=Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
    
    def delete_commande(self):
        confirme = QMessageBox(self)
        confirme.setStyleSheet("QLabel#qt_msgbox_label { font: bold 15px; }")
        confirme.setText(f"Voulez-vous supprimer la commande ?")
        confirme.setIcon(QMessageBox.Icon.Warning)
        confirme.setInformativeText(
            f"Vous vous appraitez à supprimer la commande {self.commande.id_commande}. Appuyez sur Oui pour supprimer")
        confirme.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        confirme.setDefaultButton(QMessageBox.StandardButton.No)
        button = confirme.exec()

        if button == QMessageBox.StandardButton.Yes:
            delete_commande(self.commande.id_commande)
            self.deleted.emit()
    
    def sizeHint(self):
        # return super().sizeHint()
        return self.minimumSizeHint()
    
    def minimumSizeHint(self):
        return self.minimumSize()


class ListeCommandes(QFrame):
    def __init__(self: ListeCommandes, parent: QWidget) -> None:
        super().__init__(parent)
        self.div = QVBoxLayout(self)
        self.div.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.commande_liste: list = []

        self.widget_liste: list[QWidget] = []
        self.fill()

    def fill(self):
        self.commande_liste = get_commande()
        for commande in self.commande_liste:
            commande_widget = Commande(self, commande)
            commande_widget.deleted.connect(self.update)
            self.div.addWidget(commande_widget)
            self.widget_liste.append(commande_widget)
        
    def clear(self):
        for w in self.widget_liste:
            self.div.removeWidget(w)
            w.deleteLater()
        
        self.widget_liste.clear()
        
    def update(self):
        print("update")
        self.clear()
        self.fill()


class HistoriquePage(QScrollArea):
    def __init__(self: HistoriquePage, parent: QWidget) -> None:
        super().__init__(parent)
        self.setObjectName("Historique")
        # self.setStyleSheet("QLabel, QDateEdit { background-color: yellow; }")
        self.today: QDate = QDateTime.currentDateTime().date()
        self.setStyleSheet("color: black;")

        self.div = QVBoxLayout(self)
        self.div.setContentsMargins(0, 10, 0, 10)
        self.div.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.div.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        self.div.setSpacing(40)

        self.dates = QHBoxLayout()
        self.dates.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.dates.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        self.from_label = QLabel(self)
        self.from_label.setText("Du ")
        self.from_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.dates.addWidget(self.from_label, alignment=Qt.AlignmentFlag.AlignRight)
        self.from_date = QDateEdit(self)
        self.from_date.setDate(self.today.addDays(-1))
        self.dates.addWidget(self.from_date, alignment=Qt.AlignmentFlag.AlignLeft)
        self.to_label = QLabel(self)
        self.to_label.setText(" au ")
        self.to_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.dates.addWidget(self.to_label, alignment=Qt.AlignmentFlag.AlignRight)
        self.to_date = QDateEdit(self)
        self.to_date.setDate(self.today)
        self.dates.addWidget(self.to_date, alignment=Qt.AlignmentFlag.AlignLeft)
        self.div.addLayout(self.dates)

        self.listecommande = ListeCommandes(self)
        self.div.addWidget(self.listecommande)
    
    def event(self, event: QEvent):
        if event.type() is QEvent.Type.ApplicationActivated:
            self.listecommande.update()
        return super().event(event)
