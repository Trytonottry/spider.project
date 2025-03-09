# -*- coding: utf-8 -*-
"""
Created on Sun Mar  9 12:43:17 2025

@author: Semyon
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class Plugin:
    def __init__(self):
        self.name = "Fake Profile Detector"
        self.widget = FakeProfileTab()

class FakeProfileTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.label = QLabel("Анализ фейковых профилей")
        layout.addWidget(self.label)
        self.setLayout(layout)
