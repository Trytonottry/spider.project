# -*- coding: utf-8 -*-
"""
Created on Sun Mar  9 12:37:36 2025

@author: Semyon
"""

import exifread
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QFileDialog
from PyQt5.QtGui import QPixmap

class Plugin:
    def __init__(self):
        self.name = "Metadata Extractor"
        self.widget = MetadataTab()

class MetadataTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        
        self.image_label = QLabel("Выберите изображение")
        layout.addWidget(self.image_label)
        
        self.load_button = QPushButton("Загрузить изображение")
        self.load_button.clicked.connect(self.load_image)
        layout.addWidget(self.load_button)
        
        self.metadata_text = QTextEdit()
        self.metadata_text.setReadOnly(True)
        layout.addWidget(self.metadata_text)
        
        self.setLayout(layout)

    def load_image(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Выбрать изображение", "", "Images (*.jpg *.jpeg *.png);;All Files (*)", options=options)
        
        if file_path:
            pixmap = QPixmap(file_path)
            self.image_label.setPixmap(pixmap.scaled(200, 200))
            self.extract_metadata(file_path)
    
    def extract_metadata(self, file_path):
        with open(file_path, 'rb') as f:
            tags = exifread.process_file(f)
            
        metadata_str = "\n".join([f"{tag}: {tags[tag]}" for tag in tags])
        self.metadata_text.setText(metadata_str)
