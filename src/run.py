from utils import *
from account import *

class Running(QMainWindow):
	def __init__(self, parent=None):
		super(Running, self).__init__(parent)

		self.setupUI()

	def setupUI(self):
		self.setCentralWidget(self.layout())
		self.setStyleSheet(open("Styles.qss", "r").read())
		self.setWindowTitle("Kütüphane Otomasyon Sistemi")

		self.setMinimumSize(610, 552)
		self.setMaximumSize(800, 552)

		self.show()

	def buttons(self):
		self.layoutVButton = QVBoxLayout()

		self.signInButton = QPushButton("Kayıt Ol ", self)
		self.haveAccountButton = QPushButton("""Giriş Yap""", self)

		self.signInButton.setCursor(QCursor(Qt.PointingHandCursor))
		self.haveAccountButton.setCursor(QCursor(Qt.PointingHandCursor))

		self.haveAccountButton.clicked.connect(self.open_login)
		self.signInButton.clicked.connect(self.open_sign_in)

		self.layoutVButton.addWidget(self.signInButton)
		self.layoutVButton.addWidget(self.haveAccountButton)

		self.layoutVButton.setAlignment(Qt.AlignTop | Qt.AlignCenter)

	def label(self):
		self.welcomeMsg = """
		Kütüphane Otomasyon Sistemi'ne hoş geldiniz.
		    Lütfen yapmak istediğiniz işlemi seçin
		"""

		self.welcomeLabel = QLabel(self.welcomeMsg, self)

		self.welcomeLabel.setAlignment(Qt.AlignCenter | Qt.AlignTop)

	def open_login(self):
		self.login = EntryAccount()
		self.login.setup()
		self.close()

	def open_sign_in(self):
		self.signin = Tabs()
		self.signin.setupUI()
		self.close()

	def layout(self):
		self.buttons()
		self.label()

		self.widget = QWidget()
		self.layoutV = QVBoxLayout()

		self.layoutV.addWidget(self.welcomeLabel)
		self.layoutV.addLayout(self.layoutVButton)

		self.widget.setLayout(self.layoutV)
		
		return self.widget

		

def run_main():
	import sys
	application = QApplication(sys.argv)
	window = Running()
	sys.exit(application.exec_())

if __name__ == "__main__":
	run_main()