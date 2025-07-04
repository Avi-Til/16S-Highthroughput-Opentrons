from scipy import stats
import matplotlib.pyplot, os, time, numpy, pandas, sys, traceback
from PyQt5.QtWidgets import QApplication, QLineEdit, QFileDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QButtonGroup, QLabel, QDialogButtonBox, QRadioButton, QDialog, QPushButton, QMessageBox
from PyQt5 import QtCore

class FileButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__("Choose File", parent)
        self.text = text
        self.clicked.connect(self.on_click)

    def on_click(self):
        if self.text == "ExternalStd":
            self.parent().externalStd.setChecked(True)
            self.parent().filepaths['ExternalStd'].setEnabled(True)
        fileName, _ = QFileDialog.getOpenFileName(self,"Choose File", "","All Files (*)")
        self.parent().filepaths[self.text].setText(fileName)

class MainBox(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.buttons = {}
        self.filepaths = {}
        self.reg_stats = pandas.DataFrame(columns=["PicoPlate", "Slope", "Intercept", "R value", "P value", "Standard Error"])
        self.plots = {}
        self.outputdir = ""
        self.dilutionFactor = QLineEdit()
        self.dilutionFactor.setText(str(100))
        self.createLayout()

    def createLayout(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Import Mapping CSV from PicoPrep"))
        self.filepaths['Postpico'] = QLineEdit()
        layout.addWidget(self.filepaths['Postpico'])
        self.buttons['Postpico'] = layout.addWidget(FileButton("Postpico", self))
        layout.addWidget(QLabel("Import CSV from PlateReader"))
        self.filepaths['Readings'] = QLineEdit()
        layout.addWidget(self.filepaths['Readings'])
        self.buttons['Readings'] = layout.addWidget(FileButton("Readings", self))
        layout.addWidget(QLabel("Choose Standards"))
        self.StdGroup = QButtonGroup(self)
        self.internalStd = QRadioButton("Use standards from within assay")
        self.externalStd = QRadioButton("Choose a CSV file containing the standard assay values to use:")
        self.StdGroup.addButton(self.internalStd)
        self.StdGroup.addButton(self.externalStd)
        layout.addWidget(self.internalStd)
        layout.addWidget(self.externalStd)
        self.filepaths['ExternalStd'] = QLineEdit()
        layout.addWidget(self.filepaths['ExternalStd'])
        self.buttons['ExternalStd'] = layout.addWidget(FileButton("ExternalStd", self))
        self.filepaths['ExternalStd'].installEventFilter(self)
        self.StdGroup.buttonClicked.connect(lambda checked: self.filepaths['ExternalStd'].setEnabled(True if self.externalStd.isChecked() else False))
        layout.addWidget(QLabel("Enter the sample dilution factor: (Default: 100)"))
        layout.addWidget(self.dilutionFactor)

        sublayout = QDialogButtonBox()
        PlotButton = QPushButton("Step 1: Plot Standards")
        sublayout.addButton(PlotButton, QDialogButtonBox.ActionRole)
        PlotButton.clicked.connect(self.Std_onClick)
        InferButton = QPushButton("Step 2: Infer Concentrations")
        sublayout.addButton(InferButton, QDialogButtonBox.ActionRole)
        InferButton.clicked.connect(self.Infer_onClick)
        layout.addWidget(sublayout)
        self.setLayout(layout)

    def eventFilter(self, watched, event):
        if watched == self.filepaths['ExternalStd'] and event.type() == QtCore.QEvent.MouseButtonPress:
            self.externalStd.setChecked(True)
            self.filepaths['ExternalStd'].setEnabled(True)
        return super().eventFilter(watched, event)

    def Std_onClick(self):
        self.outputdir = f"{os.path.dirname(self.filepaths['Postpico'].text())}/PostPicoOutput"
        if not os.path.exists(self.outputdir):
            os.makedirs(self.outputdir)
        self.long_df = pandas.DataFrame(columns=['SampleID', 'PicoPlate', 'PicoWell', 'Fluorescence', 'Replicate'])
        self.excel_df = pandas.read_csv(self.filepaths['Readings'].text())
        self.excel_df['Well'] = self.excel_df['Well'].replace(r'0(\d)', r'\1', regex=True)
        for index, row in pandas.read_csv(self.filepaths['Postpico'].text()).iterrows():
            pico_wells = eval(row['PicoWell'])
            for i, well in enumerate(pico_wells):
                fluorescence = self.excel_df.loc[self.excel_df['Well'] == well, self.excel_df.filter(like='Counts').columns[0]].iloc[0]
                self.long_df = pandas.concat([self.long_df, pandas.DataFrame({'SampleID': [row['SampleID']], 'PicoPlate': [row['PicoPlate']], 'PicoWell': [well], 'Fluorescence': [fluorescence], 'Replicate': [i + 1]})], ignore_index=True)
        if self.internalStd.isChecked():
            self.standards = self.long_df[self.long_df['SampleID'].str.contains('Standard')]
            self.standards.to_csv(f"{self.outputdir}//{os.path.splitext(os.path.basename(self.filepaths['Postpico'].text()))[0]}_Standards.csv", index=False)
        if self.externalStd.isChecked():
            self.standards = pandas.read_csv(self.filepaths['ExternalStd'].text())
            self.standards['PicoPlate'] = "ExternalStd"
        for plate in self.standards['PicoPlate'].unique():
            self.plots[plate] = matplotlib.pyplot.figure()
            platestd = self.standards[self.standards['PicoPlate'] == plate]
            # Plot a linear regression standard curve for the standard and their various concentrations
            x = platestd['SampleID'].str.extract('(\d+\.\d+)').astype(float).values.flatten()
            y = platestd['Fluorescence'].astype(float).tolist()
            regressout = stats.linregress(x,y)
            plateregress = [regressout.slope, regressout.intercept, regressout.rvalue, regressout.pvalue, regressout.stderr]
            self.reg_stats.loc[len(self.reg_stats)] = [plate] + plateregress
            matplotlib.pyplot.plot(x, y, 'o', label='original data')
            matplotlib.pyplot.plot(x, plateregress[1] + plateregress[0] * x, 'r', label='fitted line')
            matplotlib.pyplot.legend()
            matplotlib.pyplot.savefig(f"{self.outputdir}/{os.path.splitext(os.path.basename(self.filepaths['Postpico'].text()))[0]}_{plate}_Plot.png")
        self.reg_stats.to_csv(f"{self.outputdir}/{os.path.splitext(os.path.basename(self.filepaths['Postpico'].text()))[0]}_RegressionStats.csv", index=False)
        QMessageBox.information(None, "Success!", "Your Standard Plots have been saved. If the plots are acceptable, proceed to infering concentrations, else provide new concentration curve data and replot curves.")

    def Infer_onClick(self):

        for plate in self.long_df['PicoPlate'].unique():
            standardSet = plate if self.internalStd.isChecked() else 'ExternalStd'
            # Using this standard curve, create a new column in the long dataformat to infer the DNA concentration in the samples
            self.long_df.loc[self.long_df['PicoPlate']==plate, 'DNAConc'] = (float(self.dilutionFactor.text()) * (self.long_df.loc[self.long_df['PicoPlate']==plate, 'Fluorescence'] - self.reg_stats.loc[self.reg_stats['PicoPlate'] == standardSet, 'Intercept'].iloc[0]) / self.reg_stats.loc[self.reg_stats['PicoPlate'] == standardSet, 'Slope'].iloc[0])
        # Collapse the dataframe into a wide format by the sampleIDs
        self.wide_df = self.long_df.pivot_table(index='SampleID', columns='Replicate',
                                      values=['PicoWell', 'Fluorescence', 'DNAConc'], aggfunc=lambda x: x)
        print(self.wide_df)
        self.wide_df.columns = [f'{x}_{y}' for x, y in self.wide_df.columns]
        self.wide_df.reset_index(inplace=True)
        print(self.wide_df)
        self.wide_df['AvgDNAConc'] = self.wide_df[
            [col for col in self.wide_df.columns if col.startswith('DNAConc')]].mean(axis=1)
        self.wide_df = pandas.merge(self.wide_df, pandas.read_csv(self.filepaths['Postpico'].text()), on='SampleID')
        self.long_df.to_csv(f"{self.outputdir}/{os.path.splitext(os.path.basename(self.filepaths['Postpico'].text()))[0]}.LoncConc.csv", index=False)
        self.wide_df.to_csv(f"{self.outputdir}/{os.path.splitext(os.path.basename(self.filepaths['Postpico'].text()))[0]}.WideConc.csv", index=False)
        df = self.wide_df.drop(self.wide_df.filter(regex='DNAConc_|Fluorescence_|PicoWell_').columns, axis=1)
        df[~df['SampleID'].str.contains('Standard')].to_csv(f"{self.outputdir}/{os.path.splitext(os.path.basename(self.filepaths['Postpico'].text()))[0]}.InferedConc.csv", index=False)
        QMessageBox.information(None, "Success!", "Your DNA Concentrations have been infered.")

def handle_exception(exc_type, exc_value, exc_traceback):
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    error_dialog = QMessageBox()
    error_dialog.setWindowTitle("Error")
    error_dialog.setText(f"An error occurred:\n{exc_value}\n{tb}")
    error_dialog.exec_()

if __name__ == '__main__':
    app = QApplication([])
    sys.excepthook = handle_exception
    mainDialog = MainBox()
    mainDialog.exec_()