# -*- coding: utf-8 -*-
"""
Created on Sun Mar  9 12:39:03 2025

@author: Semyon
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class Plugin:
    def __init__(self):
        self.name = "Geolocation Finder"
        self.widget = GeoLocationTab()

class GeoLocationTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.label = QLabel("Геолокация по фото")
        layout.addWidget(self.label)
        self.setLayout(layout)
