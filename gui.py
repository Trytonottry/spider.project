# -*- coding: utf-8 -*-
"""
Created on Sat Mar  8 12:09:56 2025

@author: Semyon
"""

# gui.py

import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QTextEdit, QTabWidget,
    QFileDialog, QCheckBox, QLabel, QGroupBox, QScrollArea, QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSignal, QThread
from logger import logger
from database import save_to_db, load_external_data
from search import search_clearnet, search_darknet
from image_search import search_by_photo
from dadata import clean_phone
from export import export_to_json, export_to_csv, export_to_excel
from plugins.shodan_plugin import search_shodan
from plugins.haveibeenpwned_plugin import check_pwned

class Worker(QThread):
    """Класс для выполнения задач в отдельном потоке."""
    finished = pyqtSignal(str)

    def __init__(self, task, *args, **kwargs):
        super().__init__()
        self.task = task
        self.args = args
        self.kwargs = kwargs

    def run(self):
        """Выполняет задачу и отправляет результат."""
        try:
            result = self.task(*self.args, **self.kwargs)
            self.finished.emit(result)
        except Exception as e:
            self.finished.emit(f"Ошибка: {str(e)}")

class SpiderApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        """Инициализация интерфейса."""
        self.setWindowTitle('Паук')
        self.setGeometry(100, 100, 800, 600)

        # Основной layout
        main_layout = QVBoxLayout()

        # Вкладки
        self.tabs = QTabWidget()

        # Вкладка для поиска по всем модулям
        self.unified_search_tab = QWidget()
        self.setup_unified_search_tab()
        self.tabs.addTab(self.unified_search_tab, "Поиск по всем модулям")

        # Вкладка для загрузки внешних данных
        self.load_data_tab = QWidget()
        self.setup_load_data_tab()
        self.tabs.addTab(self.load_data_tab, "Загрузка данных")

        # Вкладка для управления плагинами
        self.plugins_tab = QWidget()
        self.setup_plugins_tab()
        self.tabs.addTab(self.plugins_tab, "Плагины")

        # Добавляем вкладки в основной layout
        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)

        # Применяем стили
        self.setStyleSheet("""
            QWidget {
                font-size: 14px;
            }
            QPushButton {
                padding: 5px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QTextEdit {
                background-color: #f9f9f9;
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
            }
            QLineEdit {
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            QTabWidget::pane {
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 10px;
            }
        """)

    def setup_unified_search_tab(self):
        """Настройка вкладки для поиска по всем модулям."""
        layout = QVBoxLayout()

        # Строка ввода
        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("Введите запрос...")

        # Чекбоксы для выбора модулей
        self.modules_group = QGroupBox("Выберите модули для поиска")
        modules_layout = QVBoxLayout()

        self.clearnet_checkbox = QCheckBox("Поиск в клирнете", self)
        self.clearnet_checkbox.setChecked(True)
        self.darknet_checkbox = QCheckBox("Поиск в даркнете", self)
        self.photo_checkbox = QCheckBox("Поиск по фото", self)
        self.phone_checkbox = QCheckBox("Поиск по телефону", self)
        self.shodan_checkbox = QCheckBox("Shodan (поиск устройств)", self)
        self.pwned_checkbox = QCheckBox("Have I Been Pwned (проверка email)", self)

        modules_layout.addWidget(self.clearnet_checkbox)
        modules_layout.addWidget(self.darknet_checkbox)
        modules_layout.addWidget(self.photo_checkbox)
        modules_layout.addWidget(self.phone_checkbox)
        modules_layout.addWidget(self.shodan_checkbox)
        modules_layout.addWidget(self.pwned_checkbox)
        self.modules_group.setLayout(modules_layout)

        # Кнопка для загрузки фото
        self.photo_button = QPushButton('Прикрепить фото', self)
        self.photo_button.clicked.connect(self.on_attach_photo)

        # Кнопка "Поиск по всем модулям"
        self.search_button = QPushButton('Поиск по всем модулям', self)
        self.search_button.clicked.connect(self.on_unified_search)

        # Окно вывода информации
        self.output = QTextEdit(self)
        self.output.setReadOnly(True)

        # Добавляем элементы в layout
        layout.addWidget(self.search_input)
        layout.addWidget(self.modules_group)
        layout.addWidget(self.photo_button)
        layout.addWidget(self.search_button)
        layout.addWidget(self.output)

        self.unified_search_tab.setLayout(layout)

    def setup_load_data_tab(self):
        """Настройка вкладки для загрузки внешних данных."""
        layout = QVBoxLayout()

        # Кнопка для загрузки данных
        self.load_data_button = QPushButton('Загрузить данные', self)
        self.load_data_button.clicked.connect(self.on_load_data)

        # Окно вывода информации
        self.load_data_output = QTextEdit(self)
        self.load_data_output.setReadOnly(True)

        # Добавляем элементы в layout
        layout.addWidget(self.load_data_button)
        layout.addWidget(self.load_data_output)

        self.load_data_tab.setLayout(layout)

    def setup_plugins_tab(self):
        """Настройка вкладки для управления плагинами."""
        layout = QVBoxLayout()

        # Чекбоксы для плагинов
        self.shodan_checkbox_plugins = QCheckBox("Shodan (поиск устройств)", self)
        self.pwned_checkbox_plugins = QCheckBox("Have I Been Pwned (проверка email)", self)

        # Добавляем элементы в layout
        layout.addWidget(self.shodan_checkbox_plugins)
        layout.addWidget(self.pwned_checkbox_plugins)

        self.plugins_tab.setLayout(layout)

    def on_unified_search(self):
        """Обработка поиска по всем модулям."""
        query = self.search_input.text()
        self.output.clear()

        if not query:
            QMessageBox.warning(self, "Ошибка", "Введите запрос для поиска.")
            return

        # Запуск поиска в отдельном потоке
        self.worker = Worker(self.perform_unified_search, query)
        self.worker.finished.connect(self.on_search_finished)
        self.worker.start()

    def perform_unified_search(self, query):
        """Выполняет поиск по всем активным модулям."""
        results = []

        if self.clearnet_checkbox.isChecked():
            clearnet_results = search_clearnet(query)
            results.append("Результаты поиска в клирнете:\n" + "\n".join(clearnet_results))

        if self.darknet_checkbox.isChecked():
            darknet_results = search_darknet(query)
            results.append("Результаты поиска в даркнете:\n" + "\n".join(darknet_results))

        if self.photo_checkbox.isChecked() and hasattr(self, 'photo_path'):
            photo_results = search_by_photo(self.photo_path)
            results.append("Результаты поиска по фото:\n" + str(photo_results))

        if self.phone_checkbox.isChecked():
            phone_result = clean_phone(query)
            if "error" in phone_result:
                results.append(f"Ошибка при поиске по телефону: {phone_result['error']}")
            else:
                results.append("Результаты поиска по телефону:\n" + str(phone_result))

        if self.shodan_checkbox.isChecked():
            shodan_results = search_shodan(query)
            results.append("Результаты Shodan:\n" + str(shodan_results))

        if self.pwned_checkbox.isChecked():
            pwned_results = check_pwned(query)
            results.append("Результаты Have I Been Pwned:\n" + str(pwned_results))

        return "\n".join(results) if results else "Ничего не найдено."

    def on_search_finished(self, result):
        """Обработка завершения поиска."""
        self.output.append(result)
        save_to_db('osint.db', self.search_input.text(), result)
        QMessageBox.information(self, "Уведомление", "Поиск завершён!")

    def on_attach_photo(self):
        """Прикрепление фото для поиска."""
        self.photo_path, _ = QFileDialog.getOpenFileName(self, "Выберите фото", "", "Images (*.png *.jpg *.jpeg)")
        if self.photo_path:
            self.output.append(f"Фото прикреплено: {os.path.basename(self.photo_path)}")

    def on_load_data(self):
        """Обработка загрузки внешних данных."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл", "", "CSV (*.csv);;Excel (*.xlsx)")
        if file_path:
            try:
                load_external_data('osint.db', file_path)
                self.load_data_output.setText(f"Данные из файла {file_path} успешно загружены.")
                logger.info(f"Данные из файла {file_path} загружены.")
            except Exception as e:
                self.load_data_output.setText(f"Ошибка: {str(e)}")
                logger.error(f"Ошибка при загрузке данных: {e}")

def run_gui():
    """Запуск графического интерфейса."""
    app = QApplication([])
    window = SpiderApp()
    window.show()
    app.exec_()