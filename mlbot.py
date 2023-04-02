##########This project was created by using a guided tutorial that was created by Smitha Kolan on Youtube. ############
#### Video used: https://www.youtube.com/watch?v=ugCiun8owMA&t=1713s ######

##This project is a ML advice bot created in Python that connects to OpenAI's ChatGPT API


import Constants    #API Key
import sys
import openai       #Import OpenAI API
#PyQt5 allows Python to be used as an alternative application development languge to C++
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QTextEdit
)

openai.api_key = Constants.API_KEY  #Import the API key

class MainWindow(QWidget):

    #Initializes UI
    def __init__(self):
        super().__init__()      #Lets you avoid referring to the base class explicitly
        self.init_ui()

    #Create widgets for UI- Button, text space, label, etc.
    def init_ui(self):
       self.logo_label = QLabel()
       self.logo_pixmap = QPixmap('robot.png'). scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
       self.logo_label.setPixmap(self.logo_pixmap)  #Set image as logo

        #Ask question - question, answer field, answer field placeholdertext
       self.input_label = QLabel('Ask a question:')
       self.input_field = QLineEdit()
       self.input_field.setPlaceholderText('Type here...')

       #Answer section AI will display reply
       self.answer_label = QLabel('Answer:')
       self.answer_field = QTextEdit()
       self.answer_field.setReadOnly(True)      #Can't edit the AI's reply

       #Submit button
       self.submit_button = QPushButton('Submit')
       self.submit_button.setStyleSheet(
           """
           QPushButton {
                background-color: #4CAF50;
                border: none;
                color: white;
                padding: 15px 32px;
                font-size: 18px;
                font-weight: bold;
                border-radius: 10px;
                }
           QPushButton: hover {
                background-color: #3e8e41;
                }
           """
       )

       #Popular Question section
       self.popular_questions_group = QGroupBox('Popular Questions')    #Title
       self.popular_questions_layout = QVBoxLayout()                    #Box that holds questions

       #Questions we want to include
       self.popular_questions = ["What is Machine Learning?", "What is the definition of Pi?", "What are popular machine learning algorithms?"]
       self.question_buttons = []

       #Create a layout
       layout = QVBoxLayout()
       layout.setContentsMargins(20, 20, 20, 20)
       layout.setSpacing(20)
       layout.setAlignment(Qt.AlignCenter)

       #Add Logo
       layout.addWidget(self.logo_label, alignment=Qt.AlignCenter)

       #Actually adding Input Field and Submit Button to interface
       input_layout = QHBoxLayout()
       input_layout.addWidget(self.input_label)
       input_layout.addWidget(self.input_field)
       input_layout.addWidget(self.submit_button)
       layout.addLayout(input_layout)

       #Add Answer Field to interface
       layout.addWidget(self.answer_label)
       layout.addWidget(self.answer_field)


       #Add the popular questions
       for question in self.popular_questions:
           button = QPushButton(question)
           button.setStyleSheet(
                """
                QPushButton {
                    background-color: #FFFFFF;
                    border: 2px solid #00AEFF;
                    color: #00AEFF;
                    padding: 10px 20px;
                    font-size: 18px;
                    font-weight: bold;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #00AEFF;
                    color: #FFFFFF;
                    }"""
           )
           #Logic for when button is clicked
           #When the question button is clicked the text that was entered will be declared a question
           button.clicked.connect(lambda _, q=question: self.input_field.setText(q))
           self.popular_questions_layout.addWidget(button)
           self.question_buttons.append(button)
       self.popular_questions_group.setLayout(self.popular_questions_layout)
       layout.addWidget(self.popular_questions_group)

       #Set the layout
       self.setLayout(layout)

       #Set the windows properties
       self.setWindowTitle('Machine Learning Question Bot')
       self.setGeometry(200, 200, 600, 600)

       #Connect the submit button to the function which queries OpenAI's API
       self.submit_button.clicked.connect(self.get_answer)

       #Communicate and push our query to OpenAI's API and get the response as well
    def get_answer(self):
        question = self.input_field.text()

        completion = openai.ChatCompletion.create(
#3 types of user roles: user, assistant and system. System defines a type of behavior you want the bot to act as,
#user has you acting as yourself and you're giving certain prompts, assistant role asks the bot to memorize certain things and keep it in memory
#for the next questions you give it
            model = "gpt-3.5-turbo",
            messages = [{"role": "user", "content": "You are a machine learning engineering expert. Answer the following question in a concise way or with bullet points."},
                        {"role": "user", "content": f'{question}'}],
            max_tokens = 1024,
            n = 1,
            stop = None,
            temperature = 0.7
        )
        #Helps extract the exact answer we're looking for from the API's response
        answer = completion.choices[0].message.content

        self.answer_field.setText(answer)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())



