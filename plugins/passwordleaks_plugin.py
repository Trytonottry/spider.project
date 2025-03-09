# -*- coding: utf-8 -*-
"""
Created on Sun Mar  9 12:42:20 2025

@author: Semyon
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class Plugin:
    def __init__(self):
        self.name = "Password Leak Checker"
        self.widget = PasswordLeaksTab()

class PasswordLeaksTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.label = QLabel("Проверка утечек паролей")
        layout.addWidget(self.label)
        self.setLayout(layout)
