import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
import io

class App(QWidget):
	def __init__(self):
		super().__init__()
		self.setGeometry(100,100,600,400)
		self.setWindowTitle('BLINDLE: PDF to Text Converter')

		self.ui_components()

	def ui_components(self):

		self.textEditor = QTextEdit()
		self.textEditor.setReadOnly(True)

		self.display = QLineEdit()
		self.display.setReadOnly(True)

		self.display2 = QLineEdit()
		self.display2.setReadOnly(True)

		button = QPushButton('Select PDF File', self)
		button.setFont(QFont('Arial', 15))
		button.clicked.connect(self.get_pdf_file)

		button2 = QPushButton('Location of TXT File', self)
		button2.setFont(QFont('Arial', 15))
		button2.clicked.connect(self.set_pdf_file)

		hlayout = QHBoxLayout()
		hlayout.addWidget(button)
		hlayout.addWidget(self.display)

		vlayout = QVBoxLayout(self)
		vlayout.addLayout(hlayout)
		vlayout.addWidget(self.textEditor)
		vlayout.setAlignment(Qt.AlignTop)

		hlayout2 = QHBoxLayout()
		hlayout2.addWidget(button2)
		hlayout2.addWidget(self.display2)
		vlayout.addLayout(hlayout2)

		self.setLayout(vlayout)
		

	def get_pdf_file(self):
		dialog = QFileDialog()
		dialog.setFileMode(QFileDialog.AnyFile)
		dialog.setFilter(QDir.Files)

		if dialog.exec_():
			file_name = dialog.selectedFiles()

			if file_name[0].endswith('.pdf'):
				inFile = open(file_name[0], 'rb')
				resMgr = PDFResourceManager()
				retData = io.StringIO()
				txtConverter = TextConverter(resMgr, retData, laparams=LAParams())
				interpreter = PDFPageInterpreter(resMgr, txtConverter)

				for page in PDFPage.get_pages(inFile):
					interpreter.process_page(page)

				txt = retData.getvalue().upper()

				outFile = file_name[0].split('.pdf')[0] + '.txt'
				with open(outFile, 'w') as f:
					f.write(txt)

				self.display.setText(str(file_name[0]))
				self.textEditor.setPlainText(txt)
			else:
				pass

	def set_pdf_file(self):
		file_path = self.display.text()
		output = file_path.replace('.pdf', '.txt')
		self.display2.setText(output)


if __name__ == '__main__':
	app = QApplication(sys.argv)

	demo = App()
	demo.show()

	sys.exit(app.exec_())