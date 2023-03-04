from utils import *
from second_page import *

class LibrarySystemUser(QMainWindow):
	def __init__(self, parent=None):
		super(LibrarySystemUser, self).__init__(parent)

	
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
		self.filter()

		self.layoutG = QGridLayout()

		self.layoutG.addWidget(self.addItemButton, 1, 0)
		self.layoutG.addWidget(self.removeItemButton, 2, 0)
		self.layoutG.addWidget(self.label, 1, 1)
		self.layoutG.addLayout(self.layoutV, 3, 0)
		self.layoutG.addWidget(self.inventoryList, 4, 0)

		self.widget = QWidget()
		self.widget.setLayout(self.layoutG)
		self.setCentralWidget(self.widget)


		self.show()
	
	def buttons(self):
		self.addItemButton = QPushButton()
		self.removeItemButton = QPushButton()

		self.addItemButton.setText("Kitap Al")
		self.removeItemButton.setText("Aldığım Kitaplar")

		self.addItemButton.clicked.connect(self.give_book)
		self.removeItemButton.clicked.connect(self.open_gave_book)

	def filter(self):
		self.layoutV = QHBoxLayout()

		self.searchNo = QPushButton()
		self.searchBookname = QPushButton()
		self.searchWriter = QPushButton()
		self.searchPublisher = QPushButton()
		self.searchType = QPushButton()
		self.search = QLineEdit()

		self.searchNo.setText("No.")
		self.searchBookname.setText("Kitap Adı")
		self.searchWriter.setText("Yazar")
		self.searchPublisher.setText("Yayınevi")
		self.searchType.setText("Tür")

		self.searchNo.clicked.connect(lambda: self.search_engine("number", self.search.text()))
		self.searchBookname.clicked.connect(lambda: self.search_engine("book_name", self.search.text()))
		self.searchWriter.clicked.connect(lambda: self.search_engine("writer_name", self.search.text()))
		self.searchPublisher.clicked.connect(lambda: self.search_engine("book_type", self.search.text()))
		self.searchType.clicked.connect(lambda: self.search_engine("publisher", self.search.text()))

		self.layoutV.addWidget(self.search)
		self.layoutV.addWidget(self.searchNo)
		self.layoutV.addWidget(self.searchBookname)
		self.layoutV.addWidget(self.searchWriter)
		self.layoutV.addWidget(self.searchPublisher)
		self.layoutV.addWidget(self.searchType)

	def give_book(self):
		self.currentrow = self.inventoryList.currentRow()
		self.book = self.inventoryList.item(self.currentrow, 1).text()
		self.idnumber = self.inventoryList.item(self.currentrow, 0).text()

		params = (self.book, self.account, self.datetime.toString(), "7", self.idnumber)

		if self.message_box(self.book) == QMessageBox.Yes:
			curs.execute("INSERT INTO gave_books VALUES(?, ?, ?, ?, 0, 0, 0, ?)", params)
			conn.commit()

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

	def message_box(self, book):
		self.givebookMsg = QMessageBox()

		self.givebookMsg.setIcon(QMessageBox.Question)
		self.givebookMsg.setWindowTitle("Kitap Al?")
		self.givebookMsg.setText(f"{book} isimli kitabı almak istediğinize emin misiniz?")
		self.givebookMsg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
		self.givebookMsg.setEscapeButton(QMessageBox.No)

		self.yesButton = self.givebookMsg.button(QMessageBox.Yes)
		self.noButton = self.givebookMsg.button(QMessageBox.No)
		
		self.yesButton.setText("Evet")
		self.noButton.setText("Hayır")

		return self.givebookMsg.exec_()

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


	def status_bar(self):
		self.statusBar = QStatusBar()
		self.statusBar.showMessage(f"Hoş Geldiniz! {self.account}")


	def tool_bar(self):
		self.toolBar = self.addToolBar("Kullanıcı Paneli")

		self.costomer_action = QAction(QIcon("icons/plus.png"), "&Kitap Al", self)
		self.costomer_action.setShortcut("CTRL+N")
		self.costomer_action.setStatusTip("Kitap Al")
		self.costomer_action.triggered.connect(self.give_book)

		self.inventory_action = QAction(QIcon("icons/inventory.png"), "&Alınan Kitaplar", self)
		self.inventory_action.setStatusTip("Alınan Kitaplar")
		self.costomer_action.triggered.connect(self.open_gave_book)

		self.sales_action = QAction(QIcon("icons/sales.jpg"), "&Cezalarım", self)
		self.sales_action.setStatusTip("Cezalarım")

		self.toolBar.addAction(self.costomer_action)
		self.toolBar.addAction(self.inventory_action)
		self.toolBar.addAction(self.sales_action)

	def open_gave_book(self):
		self.page = GaveBook()
		self.page.setupUI(self.account)

	def search_engine(self, column, result):
		matching_items = self.inventoryList.findItems(result, Qt.MatchContains)
		if matching_items:
			# We have found something.
			item = matching_items[0]  # Take the first.
			self.inventoryList.setCurrentItem(item)
	def refresh(self):
		pass
		
class GaveBook(QMainWindow):
	def __init__(self, parent=None):
		super(GaveBook, self).__init__(parent)

	def setupUI(self, acc):
		self.acc = acc
		self.setStyleSheet(open("Styles.qss", "r").read())
		self.setWindowTitle("Alınan Kitaplar")
		self.setMinimumSize(350,250)
		self.showMaximized()

		self.gave_book()
		self.load_books()
		self.setCentralWidget(self.gaveBookTable)

		self.show()

	def gave_book(self):
		self.gaveBookTable = QTableWidget()
		self.count = 0

		self.gaveBookTable.setColumnCount(7)
		self.gaveBookTable.setRowCount(self.count)
		self.gaveBookTable.setHorizontalHeaderLabels(["No.", "Kitabın Adı", "Alınma Tarihi", "Son Teslim Tarihi", "Teslim Edildi mi?", "Ceza", "Geciken Süre"])

	def load_books(self):
		curs.execute("""SELECT * FROM gave_books""")
		book_rows = curs.fetchall()

		curs.execute(f"SELECT username FROM accounts WHERE username = {self.acc}")
		account = curs.fetchall()
		print(account)

		for a in book_rows:
			if a[1] == self.acc or str(account[4]):
				self.count += 1
				self.gaveBookTable.setRowCount(self.count)

				self.gaveBookTable.setItem(self.count - 1, 0, QTableWidgetItem(str(a[7])))
				self.gaveBookTable.setItem(self.count - 1, 1, QTableWidgetItem(a[0]))
				self.gaveBookTable.setItem(self.count - 1, 2, QTableWidgetItem(a[2]))
				self.gaveBookTable.setItem(self.count - 1, 3, QTableWidgetItem(a[3]))
				self.gaveBookTable.setItem(self.count - 1, 4, QTableWidgetItem(str(a[4])))
				self.gaveBookTable.setItem(self.count - 1, 5, QTableWidgetItem(str(a[5])))
				self.gaveBookTable.setItem(self.count - 1, 6, QTableWidgetItem(str(a[6])))