#Gerekli modüllerin import edilmesi
from PyQt5.QtWidgets import (QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QTableWidget, 
QTableWidgetItem, QAction, QApplication, QGridLayout, QMainWindow, QMessageBox, QLabel, QToolBar, QDialog, QStatusBar, QComboBox, QTabWidget)
from PyQt5.QtGui import QIcon, QFont, QImage, QCursor
from PyQt5.QtCore import QTimer, QTime, Qt, QDate, QDateTime
from configparser import ConfigParser
import sqlite3

#sqlite3 üzerinden database oluşturma
conn = sqlite3.connect("database/info.db")
curs = conn.cursor()

#Database veri tablolarının oluşturulması
curs.execute("CREATE TABLE IF NOT EXISTS accounts (name TEXT, surname TEXT, username TEXT, pass TEXT, isAdmin BOOL)" )
curs.execute("""CREATE TABLE IF NOT EXISTS books 
(number TEXT, book_name TEXT, writer_name TEXT, publisher TEXT, release_date INT, book_type TEXT, language TEXT, 
receiver_name TEXT, deadline INT, isDeliver BOOL, punish INT, delay_time INT)""") 
curs.execute("""CREATE TABLE IF NOT EXISTS gave_books(book_name TEXT, receiver_name TEXT, 
receive_date TEXT, deadline TEXT, isDeliver BOOL, punish INT, delay_time INT)""")
conn.commit()