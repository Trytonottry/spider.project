# -*- coding: utf-8 -*-
"""
Created on Sun Mar  9 12:45:00 2025

@author: Semyon
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class Plugin:
    def __init__(self):
        self.name = "Database Search"
        self.widget = DatabaseSearchTab()

class DatabaseSearchTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.label = QLabel("Поиск по базам данных")
        layout.addWidget(self.label)
        self.setLayout(layout)
