# -*- coding: utf-8 -*-
"""
Created on Sun Mar  9 12:44:06 2025

@author: Semyon
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class Plugin:
    def __init__(self):
        self.name = "Face Recognition"
        self.widget = FaceRecognitionTab()

class FaceRecognitionTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.label = QLabel("Распознавание лиц")
        layout.addWidget(self.label)
        self.setLayout(layout)
