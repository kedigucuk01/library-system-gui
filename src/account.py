from utils import *
from main import *
from user_main import *

class Tabs(QDialog):
	def __init__(self, parent=None):
		super(Tabs, self).__init__(parent)
	
	def setupUI(self):
		self.setStyleSheet(open("Styles.qss", "r").read())
		self.setWindowTitle("Kayıt ol")

		self.setMinimumSize(610, 552)
		self.setMaximumSize(800, 552)

		layoutV = QVBoxLayout()
		tab = QTabWidget()

		tab.addTab(CreateAccountUser(), "Kullanıcı Kayıt")
		tab.addTab(CreateAccountAdmin(), "Admin Kayıt")

		layoutV.addWidget(tab)
		self.setLayout(layoutV)

		self.show()

	
class CreateAccountAdmin(QWidget):
	def __init__(self, parent=None):
		super(CreateAccountAdmin, self).__init__(parent)

		self.setupUI()

	def buttons(self):
		self.layoutVButton = QVBoxLayout()

		self.signInButton = QPushButton("Kayıt Ol", self)
		self.haveAccountButton = QPushButton("""Zaten bir hesabınız var mı?\nGiriş yapın""", self)
		self.haveAccountButton.setObjectName("text")

		self.signInButton.setCursor(QCursor(Qt.PointingHandCursor))
		self.haveAccountButton.setCursor(QCursor(Qt.PointingHandCursor))

		self.haveAccountButton.clicked.connect(self.open_login)
		self.signInButton.clicked.connect(self.sign)

		self.layoutVButton.addWidget(self.signInButton)
		self.layoutVButton.addWidget(self.haveAccountButton)

		self.layoutVButton.setAlignment(Qt.AlignTop | Qt.AlignCenter)


	def label(self):
		self.accountLabel = QLabel("Hesap Oluşturun", self)
		self.accountLabel.setAlignment(Qt.AlignCenter | Qt.AlignTop)

		self.lowCharError = QLabel("Şifreniz 6 karakterden küçük olamaz.")
		self.lowCharError.setObjectName("err")


	def line_edit(self):
		self.layoutVLine = QVBoxLayout()
		self.layoutHLine = QHBoxLayout()

		self.enterName = QLineEdit()
		self.enterSurname = QLineEdit()
		self.enterUsername = QLineEdit()
		self.enterPass = QLineEdit()
		self.enterCode = QLineEdit()

		self.enterName.setPlaceholderText("Adınız")
		self.enterSurname.setPlaceholderText("Soyadınız")
		self.enterUsername.setPlaceholderText("Kullanıcı adı")
		self.enterPass.setPlaceholderText("Şifre")
		self.enterCode.setPlaceholderText("Admin Kayıt Kodu")
		self.enterPass.setEchoMode(QLineEdit.Password)
		self.enterCode.setEchoMode(QLineEdit.Password)


		self.layoutHLine.addWidget(self.enterName)
		self.layoutHLine.addWidget(self.enterSurname)

		self.layoutVLine.addLayout(self.layoutHLine)
		self.layoutVLine.addWidget(self.enterUsername)
		self.layoutVLine.addWidget(self.enterPass)
		self.layoutVLine.addWidget(self.enterCode)

		self.layoutVLine.setAlignment(Qt.AlignHCenter | Qt.AlignBottom)


	def setupUI(self):
		self.adminCode = open("database/styles.qss", "r").read()

		self.line_edit()
		self.label()
		self.buttons()

		self.widget = QWidget()
		self.layoutV = QVBoxLayout()


		self.layoutV.addWidget(self.accountLabel)
		self.layoutV.addLayout(self.layoutVLine)
		self.layoutV.addLayout(self.layoutVButton)

		self.setLayout(self.layoutV)

		return self.widget


	def open_login(self):
		self.login = EntryAccount()
		self.login.setup()
		self.close()
		Tabs().close()


	def sign(self):
		if len(self.enterPass.text()) <= 5:self.get_error(self.enterPass, "Şifreniz 6 karakterden küçük olamaz.")
		if self.enterPass.text() in " ": self.get_error(self.enterPass, "Şifrenizde boşluk bulunamaz.")
		if self.enterUsername.text() in " ": self.get_error(self.enterUsername, "Kullanıcı adınızda boşluk bulunamaz.")
		if self.enterCode.text() != self.adminCode:self.get_error(self.enterCode, "Lütfen admin kodunuzu doğru giriniz.")

		else:
			params = self.enterName.text(), self.enterSurname.text(), self.enterUsername.text(), self.enterPass.text()
			curs.execute("INSERT INTO accounts VALUES (?, ?, ?, ?, 1)", params)
			conn.commit()

			self.main = LibrarySystem()
			self.main.setupUI(self.enterUsername.text())
			Tabs().close()

	def get_error(self, line, error):
		line.setStyleSheet("border-color: red;")
		err_msg = QLabel(error)
		err_msg.setObjectName("err")
		self.layoutV.addWidget(QLabel(err_msg))


class CreateAccountUser(QWidget):
	def __init__(self, parent=None):
		super(CreateAccountUser, self).__init__(parent)

		self.setupUI()

	def buttons(self):
		self.layoutVButton = QVBoxLayout()

		self.signInButton = QPushButton("Kayıt Ol", self)
		self.haveAccountButton = QPushButton("""Zaten bir hesabınız var mı?\nGiriş yapın""", self)
		self.haveAccountButton.setObjectName("text")

		self.signInButton.setCursor(QCursor(Qt.PointingHandCursor))
		self.haveAccountButton.setCursor(QCursor(Qt.PointingHandCursor))

		self.haveAccountButton.clicked.connect(self.open_login)
		self.signInButton.clicked.connect(self.sign)

		self.signInButton.setShortcut("enter")

		self.layoutVButton.addWidget(self.signInButton)
		self.layoutVButton.addWidget(self.haveAccountButton)

		self.layoutVButton.setAlignment(Qt.AlignTop | Qt.AlignCenter)


	def label(self):
		self.accountLabel = QLabel("Hesap Oluşturun", self)
		self.accountLabel.setAlignment(Qt.AlignCenter | Qt.AlignTop)

		self.lowCharError = QLabel("Şifreniz 6 karakterden küçük olamaz.")
		self.lowCharError.setObjectName("err")


	def line_edit(self):
		self.layoutVLine = QVBoxLayout()
		self.layoutHLine = QHBoxLayout()

		self.enterName = QLineEdit()
		self.enterSurname = QLineEdit()
		self.enterUsername = QLineEdit()
		self.enterPass = QLineEdit()

		self.enterName.setPlaceholderText("Adınız")
		self.enterSurname.setPlaceholderText("Soyadınız")
		self.enterUsername.setPlaceholderText("Kullanıcı adı")
		self.enterPass.setPlaceholderText("Şifre")
		self.enterPass.setEchoMode(QLineEdit.Password)

		self.layoutHLine.addWidget(self.enterName)
		self.layoutHLine.addWidget(self.enterSurname)

		self.layoutVLine.addLayout(self.layoutHLine)
		self.layoutVLine.addWidget(self.enterUsername)
		self.layoutVLine.addWidget(self.enterPass)

		self.layoutVLine.setAlignment(Qt.AlignHCenter | Qt.AlignBottom)

	def setupUI(self):
		self.line_edit()
		self.label()
		self.buttons()

		self.widget = QWidget()
		self.layoutV = QVBoxLayout()


		self.layoutV.addWidget(self.accountLabel)
		self.layoutV.addLayout(self.layoutVLine)
		self.layoutV.addLayout(self.layoutVButton)

		self.setLayout(self.layoutV)

		return self.widget


	def sign(self):
		if len(self.enterPass.text()) <= 5:self.get_error(self.enterPass, "Şifreniz 6 karakterden küçük olamaz.")
		if self.enterPass.text() in " ": self.get_error(self.enterPass, "Şifrenizde boşluk bulunamaz.")
		if self.enterUsername.text() in " ": self.get_error(self.enterUsername, "Kullanıcı adınızda boşluk bulunamaz.")

		else:
			params = self.enterName.text(), self.enterSurname.text(), self.enterUsername.text(), self.enterPass.text()
			curs.execute("INSERT INTO accounts VALUES (?, ?, ?, ?, 0)", params)
			conn.commit()

			self.main = LibrarySystem()
			self.main.setupUI(self.enterUsername.text())
			Tabs().close()
			

	def open_login(self):
		self.login = EntryAccount()
		self.login.setup()
		Tabs().close() #FIXME
	
	def get_error(self, line, error):
		line.setStyleSheet("border-color: red;")
		err_msg = QLabel(error)
		err_msg.setObjectName("err")
		self.layoutV.addWidget(QLabel(err_msg))



class EntryAccount(QMainWindow):
	def __init__(self, parent=None):
		super(EntryAccount, self).__init__(parent)

	def button(self):
		self.layoutVButton = QVBoxLayout()

		self.logInButton = QPushButton("Giriş Yap", self)
		self.dontHaveAccountButton = QPushButton("""Bir hesabınız yok mu?\nHemen kayıt olun!""", self)
		self.dontHaveAccountButton.setObjectName("text")

		self.logInButton.setCursor(QCursor(Qt.PointingHandCursor))
		self.dontHaveAccountButton.setCursor(QCursor(Qt.PointingHandCursor))

		self.layoutVButton.addWidget(self.logInButton)
		self.layoutVButton.addWidget(self.dontHaveAccountButton)

		self.dontHaveAccountButton.clicked.connect(self.open_sign_in)
		self.logInButton.clicked.connect(self.login)

		self.layoutVButton.setAlignment(Qt.AlignTop | Qt.AlignCenter)


	def labels(self):
		self.accountLabel = QLabel("Hesabınıza Giriş Yapın", self)
		self.accountLabel.setAlignment(Qt.AlignCenter | Qt.AlignTop)


	def line_edit(self):
		self.layoutVLine = QVBoxLayout()

		self.enterUsername = QLineEdit()
		self.enterPass = QLineEdit()

		self.enterUsername.setPlaceholderText("Kullanıcı Adı")
		self.enterPass.setPlaceholderText("Şifre")
		self.enterPass.setEchoMode(QLineEdit.Password)

		self.layoutVLine.addWidget(self.enterUsername)
		self.layoutVLine.addWidget(self.enterPass)

		self.layoutVLine.setAlignment(Qt.AlignHCenter | Qt.AlignBottom)


	def setup(self):
		self.setCentralWidget(self.layouts())

		self.setStyleSheet(open("Styles.qss", "r").read())
		self.setWindowTitle("Giriş Yap")

		self.setMinimumSize(610, 552)
		self.setMaximumSize(800, 552)

		self.show()
		

	def layouts(self):
		self.line_edit()
		self.labels()
		self.button()

		self.widget = QWidget()
		self.layoutV = QVBoxLayout()


		self.layoutV.addWidget(self.accountLabel)
		self.layoutV.addLayout(self.layoutVLine)
		self.layoutV.addLayout(self.layoutVButton)

		self.widget.setLayout(self.layoutV)


		return self.widget

	def login(self):
		curs.execute(f"SELECT * FROM accounts WHERE username = '{self.enterUsername.text()}' AND pass = '{self.enterPass.text()}'")
		acc = curs.fetchone()

		if acc:
	
			if acc[4]:self.main = LibrarySystem()
			if not acc[4]:self.main = LibrarySystemUser()

			self.main.setupUI(self.enterUsername.text())
			self.close()

	def open_sign_in(self):
		self.signin = Tabs()
		self.signin.setupUI()
		self.close()