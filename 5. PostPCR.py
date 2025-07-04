from PyQt5.QtWidgets import QDialog, QApplication, QLineEdit, QFileDialog, QVBoxLayout, QHBoxLayout, QFormLayout, \
    QButtonGroup, QLabel, QDialogButtonBox, QRadioButton, QDialog, QPushButton, QMessageBox
import pandas, os

class MainDialogBox(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.PCRout = QLineEdit()
        self.PCRmap = QLineEdit()
        self.thresholdCq = QLineEdit()
        self.thresholdCq.setText(str(25))
        self.openMainBox()

    def openMainBox(self):
        layout1 = QVBoxLayout()
        layout1.addWidget(QLabel("Import PCR Mapping File: "))
        layout1.addWidget(self.PCRmap)
        button = QPushButton("Choose File")
        button.clicked.connect(lambda: self.PCRmap.setText(self.choose_file()))
        layout1.addWidget(button)
        layout1.addWidget(QLabel("Import qPCR Output File: "))
        layout1.addWidget(self.PCRout)
        print(self.PCRmap.text())
        button = QPushButton("Choose File")
        layout1.addWidget(button)
        button.clicked.connect(lambda: self.PCRout.setText(self.choose_file()))
        layout1.addWidget(QLabel("Choose threshold : "))
        layout1.addWidget(self.thresholdCq)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        main_layout = QVBoxLayout()
        main_layout.addLayout(layout1)
        main_layout.addWidget(button_box)

        self.setLayout(main_layout)

    def choose_file(self):
        # Open the file dialog and get the selected file path
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("CSV files (*.csv)")
        return file_dialog.getOpenFileName()[0]


    def accept(self):
        dataframe = pandas.read_csv(self.PCRmap.text())
        Cq_data = pandas.read_csv(self.PCRout.text())
        dataframe['PCRWell'] = dataframe['PCRWell'].apply(lambda x: x[0] + x[1:].zfill(2))
        dataframe = pandas.merge(dataframe, Cq_data[['Cq', 'Well']], left_on='PCRWell', right_on='Well')
        dataframe['PCRResult'] = dataframe['Cq'].apply(lambda x: 'Fail' if x != x or x > float(self.thresholdCq.text()) else 'Success')
        print(f"{os.path.splitext(self.PCRout.text())[0]}\/{os.path.splitext(os.path.basename(self.PCRmap.text()))[0]}.PostPCR.csv")
        dataframe.to_csv(f"{os.path.split(self.PCRout.text())[0]}/{os.path.splitext(os.path.basename(self.PCRmap.text()))[0]}.PostPCR.csv", index=False)
        super(MainDialogBox, self).accept()

if __name__ == '__main__':
    app = QApplication([])
    mainDialog = MainDialogBox()
    mainDialog.exec_()
    QMessageBox.information(None, 'Finish', 'Program has completed running')
