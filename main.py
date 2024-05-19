# essentials
import sys
import pandas as pd

# GUI
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QTextEdit, QPushButton, QVBoxLayout, 
    QFileDialog, QMessageBox, QHBoxLayout, QCheckBox
)
from PyQt5.QtCore import QMimeData

# tensor (loading model, padding tokenized integer sequences)
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

# file libraries
import pickle
from docx import Document
import pdfplumber

# matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


class PlainTextEdit(QTextEdit):
    def insertFromMimeData(self, source: QMimeData):
        self.insertPlainText(source.text())

class FakeNewsClassifier(QWidget):
    def __init__(self):
        super().__init__()
        self.fake_count = 0
        self.real_count = 0
        self.history = []
        self.dark_mode = False
        self.initUI()

        # loading the saved model, change filepath if you saved the classifier somewhere else or under a different name
        self.model = load_model('fakenewsdetector.h5')

        # loading the tokenizer (important, or model will be much less accurate)
        with open('tokenizer.pickle', 'rb') as handle:
            self.tokenizer = pickle.load(handle)

    def initUI(self):

        # building GUI and initializing
        self.setWindowTitle('IntegriNews AI - Fake News Classifier')
        self.setGeometry(100, 100, 600, 800)

        main_layout = QVBoxLayout()

        title_label = QLabel('<h1 style="text-align: center;">IntegriNews AI</h1>')
        main_layout.addWidget(title_label)

        subtitle_label = QLabel('<h2 style="text-align: center;">Fake News Classifier</h2>')
        main_layout.addWidget(subtitle_label)

        top_layout = QHBoxLayout()

        article_title_label = QLabel('Article Title:')
        top_layout.addWidget(article_title_label)

        self.title_input = QLineEdit()
        top_layout.addWidget(self.title_input)

        dark_mode_checkbox = QCheckBox('Dark Mode')
        dark_mode_checkbox.stateChanged.connect(self.toggle_dark_mode)
        top_layout.addWidget(dark_mode_checkbox)

        main_layout.addLayout(top_layout)

        text_label = QLabel('Article Text:')
        main_layout.addWidget(text_label)

        self.text_input = PlainTextEdit()
        main_layout.addWidget(self.text_input)

        classify_button = QPushButton('Classify')
        classify_button.clicked.connect(self.classify)
        main_layout.addWidget(classify_button)

        upload_button = QPushButton('Upload File')
        upload_button.clicked.connect(self.upload_file)
        main_layout.addWidget(upload_button)

        export_button = QPushButton('Export Results')
        export_button.clicked.connect(self.export_results)
        main_layout.addWidget(export_button)

        self.result_label = QLabel('')
        main_layout.addWidget(self.result_label)

        self.canvas = FigureCanvas(Figure())
        main_layout.addWidget(self.canvas)

        self.setLayout(main_layout)

        self.update_plot()

    def toggle_dark_mode(self, state):
        if state == 2:  
            self.setStyleSheet("background-color: #2E2E2E; color: #FFFFFF;")
            self.dark_mode = True
        else:  
            self.setStyleSheet("")
            self.dark_mode = False
        self.update_plot()

    def upload_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File", "", 
                        "All Files (*);;PDF Files (*.pdf);;Word Files (*.docx);;Text Files (*.txt)", options=options)
        if file_path:
            text = self.extract_text_from_file(file_path)
            if text:
                self.text_input.setPlainText(text)

    def extract_text_from_file(self, file_path):
        text = ''
        try:
            if file_path.endswith('.pdf'):
                with pdfplumber.open(file_path) as pdf:
                    for page in pdf.pages:
                        text += page.extract_text()
            elif file_path.endswith('.docx'):
                doc = Document(file_path)
                for para in doc.paragraphs:
                    text += para.text + ' '
            elif file_path.endswith('.txt'):
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to extract text from file: {e}")
        return text

    def classify(self):
        title = self.title_input.text().strip()
        text = self.text_input.toPlainText().strip()

        if not title or not text:
            QMessageBox.warning(self, "Input Error", "Please provide both a title and text for the article.")
            return

        # tokenizing input data (model is trained on tokenized integer sequences)
        X_seq = self.tokenizer.texts_to_sequences([title + ' ' + text])
        X_pad = pad_sequences(X_seq, maxlen=1000, padding='post')

        # result is from 0 - 1, higher result value = the more confident the model is that the article is fake
        prediction = self.model.predict(X_pad)[0][0]
        if prediction > 0.8:
            result = "Highly Likely to be Fake News ({:.2f}% probability)".format(prediction * 100)
            self.fake_count += 1
        elif prediction > 0.6:
            result = "Likely to be Fake News ({:.2f}% probability)".format(prediction * 100)
            self.fake_count += 1
        elif prediction > 0.4:
            result = "Possibly Fake News ({:.2f}% probability)".format(prediction * 100)
            self.fake_count += 1
        elif prediction > 0.2:
            result = "Potentially Real News ({:.2f}% probability)".format((1 - prediction) * 100)
            self.real_count += 1
        else:
            result = "Highly Likely to be Real News ({:.2f}% probability)".format((1 - prediction) * 100)
            self.real_count += 1
        
        self.history.append({'title': title, 'text': text, 'result': result, 'probability': prediction})
        self.result_label.setText(f'Classification Result: {result}')
        self.update_plot()

    def update_plot(self):
        self.canvas.figure.clear()
        ax = self.canvas.figure.add_subplot(111)
        
        if self.fake_count == 0 and self.real_count == 0:
            sizes = [50, 50]
            labels = ['Real News', 'Fake News']
        else:
            sizes = [self.real_count, self.fake_count]
            labels = ['Real News', 'Fake News']
        
        colors = ['#66b3ff','#ff9999']
        wedges, texts, autotexts = ax.pie(sizes, colors=colors, autopct='%1.1f%%', startangle=90, wedgeprops=dict(width=0.3, edgecolor='w'))

        ax.set_title("Classification Ratio")

        ax.legend(wedges, labels, title="Categories", loc="center left", bbox_to_anchor=(0.8, 0, 0.5, 1))

        plt.setp(autotexts, size=10, weight="bold", color="black")

        ax.axis('equal')
        self.canvas.draw()

    def export_results(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", 
                        "CSV Files (*.csv);;All Files (*)", options=options)
        if file_path:
            try:
                df = pd.DataFrame(self.history)
                df.to_csv(file_path, index=False)
                QMessageBox.information(self, "Success", "Results exported successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to export results: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    classifier = FakeNewsClassifier()
    classifier.show()
    sys.exit(app.exec_())
