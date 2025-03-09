# -*- coding: utf-8 -*-
"""
Created on Sun Mar  9 12:41:22 2025

@author: Semyon
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class Plugin:
    def __init__(self):
        self.name = "Social Media Checker"
        self.widget = SocialMediaTab()

class SocialMediaTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.label = QLabel("Проверка профиля в соцсетях")
        layout.addWidget(self.label)
        self.setLayout(layout)
