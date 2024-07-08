from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(550, 450)  # Fixed size for the window

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        # Source DB Inputs
        self.sourceDbLabel = QtWidgets.QLabel(self.centralwidget)
        self.sourceDbLabel.setText("Source Database Details")
        self.gridLayout.addWidget(self.sourceDbLabel, 0, 0, 1, 2)

        self.sourceDbNameLabel = QtWidgets.QLabel(self.centralwidget)
        self.sourceDbNameLabel.setText("Database Name:")
        self.gridLayout.addWidget(self.sourceDbNameLabel, 1, 0)
        self.sourceDbNameInput = QtWidgets.QLineEdit(self.centralwidget)
        self.gridLayout.addWidget(self.sourceDbNameInput, 1, 1)

        self.sourceDbUserLabel = QtWidgets.QLabel(self.centralwidget)
        self.sourceDbUserLabel.setText("User:")
        self.gridLayout.addWidget(self.sourceDbUserLabel, 2, 0)
        self.sourceDbUserInput = QtWidgets.QLineEdit(self.centralwidget)
        self.gridLayout.addWidget(self.sourceDbUserInput, 2, 1)

        self.sourceDbPassLabel = QtWidgets.QLabel(self.centralwidget)
        self.sourceDbPassLabel.setText("Password:")
        self.gridLayout.addWidget(self.sourceDbPassLabel, 3, 0)
        self.sourceDbPassInput = QtWidgets.QLineEdit(self.centralwidget)
        self.sourceDbPassInput.setEchoMode(QtWidgets.QLineEdit.Password)
        self.gridLayout.addWidget(self.sourceDbPassInput, 3, 1)

        self.sourceDbHostLabel = QtWidgets.QLabel(self.centralwidget)
        self.sourceDbHostLabel.setText("Host:")
        self.gridLayout.addWidget(self.sourceDbHostLabel, 4, 0)
        self.sourceDbHostInput = QtWidgets.QLineEdit(self.centralwidget)
        self.gridLayout.addWidget(self.sourceDbHostInput, 4, 1)

        self.sourceDbPortLabel = QtWidgets.QLabel(self.centralwidget)
        self.sourceDbPortLabel.setText("Port:")
        self.gridLayout.addWidget(self.sourceDbPortLabel, 5, 0)
        self.sourceDbPortInput = QtWidgets.QLineEdit(self.centralwidget)
        self.gridLayout.addWidget(self.sourceDbPortInput, 5, 1)

        # New DB Inputs
        self.newDbLabel = QtWidgets.QLabel(self.centralwidget)
        self.newDbLabel.setText("New Database Details")
        self.gridLayout.addWidget(self.newDbLabel, 0, 2, 1, 2)

        self.newDbNameLabel = QtWidgets.QLabel(self.centralwidget)
        self.newDbNameLabel.setText("Database Name:")
        self.gridLayout.addWidget(self.newDbNameLabel, 1, 2)
        self.newDbNameInput = QtWidgets.QLineEdit(self.centralwidget)
        self.gridLayout.addWidget(self.newDbNameInput, 1, 3)

        self.newDbUserLabel = QtWidgets.QLabel(self.centralwidget)
        self.newDbUserLabel.setText("User:")
        self.gridLayout.addWidget(self.newDbUserLabel, 2, 2)
        self.newDbUserInput = QtWidgets.QLineEdit(self.centralwidget)
        self.gridLayout.addWidget(self.newDbUserInput, 2, 3)

        self.newDbPassLabel = QtWidgets.QLabel(self.centralwidget)
        self.newDbPassLabel.setText("Password:")
        self.gridLayout.addWidget(self.newDbPassLabel, 3, 2)
        self.newDbPassInput = QtWidgets.QLineEdit(self.centralwidget)
        self.newDbPassInput.setEchoMode(QtWidgets.QLineEdit.Password)
        self.gridLayout.addWidget(self.newDbPassInput, 3, 3)

        self.newDbHostLabel = QtWidgets.QLabel(self.centralwidget)
        self.newDbHostLabel.setText("Host:")
        self.gridLayout.addWidget(self.newDbHostLabel, 4, 2)
        self.newDbHostInput = QtWidgets.QLineEdit(self.centralwidget)
        self.gridLayout.addWidget(self.newDbHostInput, 4, 3)

        self.newDbPortLabel = QtWidgets.QLabel(self.centralwidget)
        self.newDbPortLabel.setText("Port:")
        self.gridLayout.addWidget(self.newDbPortLabel, 5, 2)
        self.newDbPortInput = QtWidgets.QLineEdit(self.centralwidget)
        self.gridLayout.addWidget(self.newDbPortInput, 5, 3)

        # Start Button and Progress Bar
        self.startButton = QtWidgets.QPushButton(self.centralwidget)
        self.startButton.setObjectName("startButton")
        self.gridLayout.addWidget(self.startButton, 6, 0, 1, 4, QtCore.Qt.AlignCenter)

        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout.addWidget(self.progressBar, 7, 0, 1, 4)
        
        # Log Text Area
        self.logTextBox = QtWidgets.QTextEdit(self.centralwidget)
        self.logTextBox.setObjectName("logTextBox")
        self.logTextBox.setReadOnly(True)
        self.gridLayout.addWidget(self.logTextBox, 8, 0, 1, 4)

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Dummy DB Creator"))
        self.startButton.setText(_translate("MainWindow", "Start"))