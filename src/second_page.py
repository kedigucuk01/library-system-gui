from utils import *

class AddBook(QMainWindow):
	def __init__(self, parent=None):
		super(AddBook, self).__init__(parent)

		self.setupUI()

	def setupUI(self):
		self.setCentralWidget(self.layout())

		self.setWindowTitle("Kitap Ekle")
		self.setWindowIcon(QIcon("icons/inventory.png"))
		self.setMinimumSize(400, 400)
		self.setStyleSheet(open("Styles.qss", "r").read())

		self.show()

	def layout(self):
		self.widget = QWidget()

		self.layoutG = QGridLayout()
		self.layoutV = QVBoxLayout()

		self.add_item()

		self.layoutG.addWidget(self.num, 0, 0)
		self.layoutG.addWidget(self.book_name, 0, 3)
		self.layoutG.addWidget(self.writer, 1, 0)
		self.layoutG.addWidget(self.publisher, 1, 3)
		self.layoutG.addWidget(self.book_type, 2, 0)
		self.layoutG.addWidget(self.language, 2, 3)

		self.layoutV.addLayout(self.layoutG)
		self.layoutV.addWidget(QLabel("Basım Yılı: "))
		self.layoutV.addWidget(self.release_date)
		self.layoutV.addWidget(self.addButton)

		self.widget.setLayout(self.layoutV)

		return self.widget


	def add_item(self):

		self.addButton = QPushButton()

		self.book_name = QLineEdit()
		self.writer = QLineEdit()
		self.publisher = QLineEdit()
		self.book_type = QLineEdit()
		self.num = QLineEdit()
		self.language = QLineEdit()
		self.release_date = QComboBox()

		self.book_name.setPlaceholderText("Kitap Adı")
		self.writer.setPlaceholderText("Kıtabın Yazarı")
		self.publisher.setPlaceholderText("Yayınevi")
		self.book_type.setPlaceholderText("Kitap Türü")
		self.language.setPlaceholderText("Dil")
		self.num.setPlaceholderText("No.")

		self.year_list = range(1899, 2023)
		self.release_date.addItems([str(x) for x in self.year_list])

		self.addButton.setText("Kitap Ekle")
