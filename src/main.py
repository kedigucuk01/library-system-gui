from utils import *
from second_page import *
from user_main import GaveBook

class LibrarySystem(QMainWindow):
	def __init__(self, parent=None):
		super(LibrarySystem, self).__init__(parent)

	
	def setupUI(self, account):
		self.timer = QTimer()
		self.label = QLabel()

		self.account = account

		self.setStyleSheet(open("Styles.qss", "r").read())
		self.setWindowTitle("Kütüphane Otomasyon Sistemi")
		self.setMinimumSize(350,250)
		self.showMaximized()

		self.setFont(QFont("Times New Roman", 20, QFont.Bold))
		self.timer.timeout.connect(self.clock)
		self.timer.start(1000)

		self.buttons()
		self.inventory_list()
		self.tool_bar()
		self.status_bar()
		self.load_books()

		self.layoutG = QGridLayout()

		self.layoutG.addWidget(self.addItemButton, 1, 0)
		self.layoutG.addWidget(self.removeItemButton, 2, 0)
		self.layoutG.addWidget(self.label, 1, 1)
		self.layoutG.addWidget(self.inventoryList, 3, 0)

		self.widget = QWidget()
		self.widget.setLayout(self.layoutG)
		self.setCentralWidget(self.widget)


		self.show()


	def add_row(self):
		self.count += 1
		self.inventoryList.setRowCount(self.count)

		params = (self.add_book.num.text(), self.add_book.book_name.text(), self.add_book.writer.text(),
		self.add_book.publisher.text(), int(self.add_book.release_date.currentText()), self.add_book.book_type.text(), 
		self.add_book.language.text(), self.account)

		self.inventoryList.setItem(self.count - 1, 0, QTableWidgetItem(self.add_book.num.text()))
		self.inventoryList.setItem(self.count - 1, 1, QTableWidgetItem(self.add_book.book_name.text()))
		self.inventoryList.setItem(self.count - 1, 2, QTableWidgetItem(self.add_book.writer.text()))
		self.inventoryList.setItem(self.count - 1, 3, QTableWidgetItem(self.add_book.publisher.text()))
		self.inventoryList.setItem(self.count - 1, 4, QTableWidgetItem(self.add_book.release_date.currentText()))
		self.inventoryList.setItem(self.count - 1, 5, QTableWidgetItem(self.add_book.book_type.text()))
		self.inventoryList.setItem(self.count - 1, 6, QTableWidgetItem(self.add_book.language.text()))
		

		curs.execute("INSERT INTO books VALUES(?, ?, ?, ?, ?, ?, ?, ?, 7, 0, 0, 0)", params)
		conn.commit()


	def buttons(self):
		self.addItemButton = QPushButton()
		self.removeItemButton = QPushButton()

		self.addItemButton.setText("Ürün Ekle")
		self.removeItemButton.setText("Ürün Sil")

		self.removeItemButton.clicked.connect(self.remove_row)
		self.addItemButton.clicked.connect(self.add_item)

	def clock(self):
		self.presenTime = QTime.currentTime()
		self.texTime = self.presenTime.toString('hh:mm:ss')
		now = QDate.currentDate()

		self.datetime = QDateTime.currentDateTime()


		self.label.setText(self.texTime + "\n" + now.toString(Qt.ISODate))

	def inventory_list(self):
		self.inventoryList = QTableWidget()
		self.count = 0

		self.inventoryList.setColumnCount(12)
		self.inventoryList.setRowCount(self.count)
		self.inventoryList.setHorizontalHeaderLabels(["No.", "Kitabın Adı", "Yazarın Adı", "Yayınevi", "Yayım Tarihi", "Kitabın Türü", "Dil", "Son Teslim Tarihi", "Teslim Etti mi?", "Ceza", "Geciken Süre"])

	def remove_row(self):
		self.currentrow = self.inventoryList.currentRow()
		self.id = self.inventoryList.item(self.currentrow, 0).text()

		if self.count > 1 and self.message_box(self.currentrow + 1) == QMessageBox.Yes:
			self.inventoryList.removeRow(self.currentrow)

			curs.execute(f"DELETE FROM books WHERE number = {self.id}")
			conn.commit()

			self.count -= 1


	def load_books(self):
		curs.execute("""SELECT * FROM books""")

		book_rows = curs.fetchall()

		for b in book_rows:
			self.count += 1
			self.inventoryList.setRowCount(self.count)

			self.inventoryList.setItem(self.count - 1, 0, QTableWidgetItem(str(b[0])))
			self.inventoryList.setItem(self.count - 1, 1, QTableWidgetItem(b[1]))
			self.inventoryList.setItem(self.count - 1, 2, QTableWidgetItem(b[2]))
			self.inventoryList.setItem(self.count - 1, 3, QTableWidgetItem(b[3]))
			self.inventoryList.setItem(self.count - 1, 4, QTableWidgetItem(str(b[4])))
			self.inventoryList.setItem(self.count - 1, 5, QTableWidgetItem(b[5]))
			self.inventoryList.setItem(self.count - 1, 6, QTableWidgetItem(b[6]))

	def message_box(self, row):
		self.removeMsgbox = QMessageBox()
		self.removeMsgbox.setIcon(QMessageBox.Question)
		self.removeMsgbox.setWindowTitle("Kitap Sil?")
		self.removeMsgbox.setText(f"{row}.daki kitabı silmek istediğinizden emin misiniz?")
		self.removeMsgbox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
		self.removeMsgbox.setEscapeButton(QMessageBox.No)

		self.yesButton = self.removeMsgbox.button(QMessageBox.Yes)
		self.noButton = self.removeMsgbox.button(QMessageBox.No)

		self.yesButton.setText("Evet")
		self.noButton.setText("Hayır")

		return self.removeMsgbox.exec_()


	def status_bar(self):
		self.statusBar = QStatusBar()
		self.statusBar.showMessage(f"Hoş Geldiniz! {self.account}")


	def tool_bar(self):
		self.toolBar = self.addToolBar("Admin Paneli")

		self.costomer_action = QAction(QIcon("icons/plus.png"), "&Kitap Ekle", self)
		self.costomer_action.setShortcut("CTRL+N")
		self.costomer_action.setStatusTip("Kitap Ekle")
		self.costomer_action.triggered.connect(self.add_item)

		self.remove_action = QAction(QIcon("icons/trash.png"), "&Kitap Sil", self)
		self.remove_action.setShortcut("SHIFT+DEL")
		self.remove_action.setStatusTip("Kitap Sil")
		self.remove_action.triggered.connect(self.remove_row)

		self.inventory_action = QAction(QIcon("icons/inventory.png"), "&Alınan Kitaplar", self)
		self.inventory_action.setStatusTip("Alınan Kitaplar")
		self.inventory_action.triggered.connect(self.open_gave_books)

		self.sales_action = QAction(QIcon("icons/sales.jpg"), "&Sales", self)
		self.sales_action.setStatusTip("Satışlar")

		self.toolBar.addAction(self.costomer_action)
		self.toolBar.addAction(self.remove_action)
		self.toolBar.addAction(self.inventory_action)
		self.toolBar.addAction(self.sales_action)

	def add_item(self):
		self.add_book = AddBook()
		self.add_book.setupUI()

		self.add_book.addButton.clicked.connect(self.add_row)

	def open_gave_books(self):
		self.gavebook = GaveBook()
		self.gavebook.setupUI(self.account)

