from PyQt5.QtWidgets import QApplication, QLineEdit, QFileDialog, QVBoxLayout, QComboBox, QFormLayout, QButtonGroup, \
    QLabel, QDialogButtonBox, QRadioButton, QDialog, QPushButton, QMessageBox, QCheckBox
from PyQt5 import QtCore
import re, math, csv, pandas, os, numpy

class LabwareWindow(QDialog):
    def __init__(self, ChooseLabwareList, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Choose Sample Labwares")
        self.ChooseLabwareList = ChooseLabwareList
        self.initUI()

    def initUI(self):
        self.PlateSet=[]
        LabwareList = ["eppendorf96wellpcrplatetwin.tecskirted_96_wellplate_150ul",
                       "fishersciflatbottomplatepicogreen_96_wellplate_250ul",
                       "nest_96_wellplate_100ul_pcr_full_skirt", "nest_96_wellplate_200ul_flat",
                       "biorad_96_wellplate_200ul_pcr", "armadillo_96_wellplate_200ul_pcr_full_skirt",
                       "opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap",
                       "opentrons_24_tuberack_eppendorf_2ml_safelock_snapcap",
                       "opentrons_24_tuberack_nest_0.5ml_screwcap",
                       "opentrons_24_tuberack_nest_1.5ml_screwcap",
                       "opentrons_24_tuberack_nest_2ml_screwcap",
                       "appliedbiosystemsmicroamp_384_wellplate_40ul", "biorad_384_wellplate_50ul"]
        LabwareLayout = QVBoxLayout()
        LabwareLayout.addWidget(QLabel(f"Choose the corresponding source labware"))
        for i, name in enumerate(self.ChooseLabwareList):
            label = QLabel(self)
            label.setText(name)
            PlateDropDown = QComboBox()
            PlateDropDown.addItems(LabwareList)
            PlateDropDown.setCurrentIndex(0)
            LabwareLayout.addWidget(label)
            LabwareLayout.addWidget(PlateDropDown)
            self.PlateSet.append(PlateDropDown)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Close)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.close)

        layout = QVBoxLayout()
        layout.addLayout(LabwareLayout)
        layout.addWidget(buttonBox)
        self.setLayout(layout)

    def getValue(self):
        return [plate.currentText() for plate in self.PlateSet]

class AdvancedInputBox(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.PCRmmVol = QLineEdit()
        self.PCRmmVol.setText(str(self.parent().PCRmmVol))
        self.PCRSampleVol = QLineEdit()
        self.PCRSampleVol.setText(str(self.parent().PCRSampleVol))
        self.CritVol = QLineEdit()
        self.CritVol.setText(str(self.parent().CritVol))
        self.overhead = QLineEdit()
        self.overhead.setText(str(self.parent().overhead))
        self.PCRamount = QLineEdit()
        self.PCRamount.setText(str(self.parent().PCRamount))
        self.PCRPrimerVol = QLineEdit()
        self.PCRPrimerVol.setText(str(self.parent().PCRPrimerVol))
        self.PCRmmTubeVol = QLineEdit()
        self.PCRmmTubeVol.setText(str(self.parent().PCRmmTubeVol))
        self.PrimerStart = QLineEdit()
        self.PrimerStart.setText(str(self.parent().PrimerStart))
        self.openAdvancedDialog()

    def openAdvancedDialog(self):
        FormLayout = QFormLayout()
        FormLayout.addRow("Volume of Primer per PCR reaction (ul) (Default: 5):", self.PCRPrimerVol)
        FormLayout.addRow("Volume of MasterMix per PCR reaction (ul) (Default: 26):", self.PCRmmVol)
        FormLayout.addRow("Volume of MasterMix stock per tube (ul) (Default: 1285):", self.PCRmmTubeVol)
        FormLayout.addRow("Maximum Volume of sample per PCR reaction (ul) (Default: 19):", self.PCRSampleVol)
        FormLayout.addRow("Critical sample pipetting volume (ul) (Default: 5):", self.CritVol)
        FormLayout.addRow("Amount of DNA per PCR reaction (ng) (Default: 5):", self.PCRamount)
        FormLayout.addRow("Start index of Primers from Primer File (Default: 0):", self.PrimerStart)
        FormLayout.addRow("Overheads ratio (Default: 1.04):", self.overhead)
        LabwareList = ["eppendorf96wellpcrplatetwin.tecskirted_96_wellplate_150ul",
                       "fishersciflatbottomplatepicogreen_96_wellplate_250ul",
                       "nest_96_wellplate_100ul_pcr_full_skirt", "nest_96_wellplate_200ul_flat",
                       "biorad_96_wellplate_200ul_pcr", "armadillo_96_wellplate_200ul_pcr_full_skirt",
                       "opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap",
                       "opentrons_24_tuberack_eppendorf_2ml_safelock_snapcap",
                       "opentrons_24_tuberack_nest_0.5ml_screwcap",
                       "opentrons_24_tuberack_nest_1.5ml_screwcap",
                       "opentrons_24_tuberack_nest_2ml_screwcap",
                       "appliedbiosystemsmicroamp_384_wellplate_40ul", "biorad_384_wellplate_50ul"]
        LabwareLayout = QVBoxLayout()
        LabwareLayout.addWidget(QLabel("Choose the appropriate labware for the PCRPlate"))
        self.PCRPlateDropDown = QComboBox()
        self.PCRPlateDropDown.addItems(LabwareList)
        self.PCRPlateDropDown.setCurrentIndex(LabwareList.index(self.parent().PCRLabware))
        LabwareLayout.addWidget(self.PCRPlateDropDown)
        LabwareLayout.addWidget(QLabel("Choose the appropriate labware for the PrimerPlate"))
        self.PrimerPlateDropDown = QComboBox()
        self.PrimerPlateDropDown.addItems(LabwareList)
        self.PrimerPlateDropDown.setCurrentIndex(LabwareList.index(self.parent().PrimerLabware))
        LabwareLayout.addWidget(self.PrimerPlateDropDown)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Close)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.close)

        layout = QVBoxLayout()
        layout.addLayout(FormLayout)
        layout.addLayout(LabwareLayout)
        layout.addWidget(buttonBox)

        self.setLayout(layout)

    def getValues(self):
        return float(self.PCRmmVol.text()), float(self.PCRSampleVol.text()), float(self.overhead.text()), float(
            self.PCRamount.text()), self.PCRPlateDropDown.currentText(), self.PrimerPlateDropDown.currentText(), float(
            self.CritVol.text()), float(self.PCRPrimerVol.text()), float(self.PCRmmTubeVol.text()), int(self.PrimerStart.text())


class MainBox(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.PCRmmVol = 26
        self.PCRSampleVol = 19
        self.overhead = 1.04
        self.PCRamount = 5
        self.CritVol = 5
        self.PCRPrimerVol = 5
        self.PCRmmTubeVol = 1285
        self.PrimerStart = 0
        self.PCRLabware = "biorad_96_wellplate_200ul_pcr"
        self.PrimerLabware = "eppendorf96wellpcrplatetwin.tecskirted_96_wellplate_150ul"
        self.createLayout()

    def createLayout(self):
        layout1 = QVBoxLayout()
        layout1.addWidget(QLabel("Select the PCR Batch (Ex. 1,3-5):"))
        self.RunGroup = QButtonGroup(self)
        self.allButton = QRadioButton("All")
        self.listButton = QRadioButton("List")
        self.RepeatButton = QRadioButton("Repeat")
        self.RunGroup.addButton(self.listButton)
        self.RunGroup.addButton(self.allButton)
        layout1.addWidget(self.allButton)
        layout1.addWidget(self.listButton)
        self.listEdit = QLineEdit()
        layout1.addWidget(self.listEdit)
        self.filepath = QLineEdit()
        layout1.addWidget(QLabel("Choose Sample Map (DilutionMap/Infered) File:"))
        layout1.addWidget(self.filepath)
        button1 = QPushButton("Choose File")
        button1.clicked.connect(lambda: self.filepath.setText(self.choose_file()))
        layout1.addWidget(button1)
        self.primerpath = QLineEdit()
        layout1.addWidget(QLabel("Choose Primer File:"))
        layout1.addWidget(self.primerpath)
        self.primerpath.setText(os.path.join(os.path.dirname(os.path.abspath(__file__)), "dependencies\\16S_Kozich_Barcodes.csv"))
        button2 = QPushButton("Choose File")
        button2.clicked.connect(lambda: self.primerpath.setText(self.choose_file()))
        layout1.addWidget(button2)
        self.mailID = QLineEdit()
        layout1.addWidget(QLabel("Enter email to notify on run completion:"))
        layout1.addWidget(self.mailID)
        self.checkbox = QCheckBox("Only previously failed PCR reactions")
        layout1.addWidget(self.checkbox)

        self.listEdit.installEventFilter(self)
        self.RunGroup.buttonClicked.connect(
            lambda checked: self.listEdit.setEnabled(True if checked.text() == "List" else False))

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        advancedButton = QPushButton("Advanced Options")
        button_box.addButton(advancedButton, QDialogButtonBox.ActionRole)
        advancedButton.clicked.connect(self.showAdvancedDialog)

        main_layout = QVBoxLayout()
        main_layout.addLayout(layout1)
        main_layout.addWidget(button_box)

        self.setLayout(main_layout)

    def eventFilter(self, watched, event):
        if watched == self.listEdit and event.type() == QtCore.QEvent.MouseButtonPress:
            self.listButton.setChecked(True)
            self.listEdit.setEnabled(True)
        return super().eventFilter(watched, event)

    def showAdvancedDialog(self):
        self.advancedBox = AdvancedInputBox(self)
        self.advancedBox.exec_()
        if self.advancedBox.result() == QDialog.Accepted:
            self.PCRmmVol, self.PCRSampleVol, self.overhead, self.PCRamount, self.PCRLabware, self.PrimerLabware, self.CritVol, self.PCRPrimerVol, self.PCRmmTubeVol, self.PrimerStart = self.advancedBox.getValues()

    def choose_file(self):
        # Open the file dialog and get the selected file path
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("CSV files (*.csv)")
        return file_dialog.getOpenFileName()[0]

    def PCRBatch_toList(self):
        if self.listButton.isChecked():
            text = self.listEdit.text()
            text = re.sub(r'\s', '', text)
            if re.match(r'^\d+([,-]\d+)*$', text):
                self.PCRBatchList = []
                for part in text.split(','):
                    if '-' in part:
                        start, end = map(int, part.split('-'))
                        self.PCRBatchList.extend(range(start, end + 1))
                    else:
                        self.PCRBatchList.append(int(part))
                return
            elif text:
                self.PCRBatchList = [float('NaN')]
                return
        elif self.allButton.isChecked():
            self.PCRBatchList = [float('Inf')]
            return

    def iscsv(self):
        try:
            with open(self.filepath.text(), newline='') as f:
                reader = csv.reader(f)
                next(reader)
        except (csv.Error, FileNotFoundError):
            return False
        return True

    def check_values(self):
        if self.RunGroup.checkedButton() is None:
            raise ValueError("Required options are missing")
        else:
            self.PCRBatch_toList()
        if self.checkbox.isChecked():
            self.PCRBatchList = [-x for x in self.PCRBatchList]
        if not 1 < self.overhead <= 1.25:
            raise ValueError("Overhead must be between 1.000 and 1.250")
        if not all([self.PCRmmVol, self.PCRSampleVol, self.PCRamount, self.PCRBatchList, self.overhead]):
            raise ValueError("Required parameters are missing")
        if any(math.isnan(i) for i in self.PCRBatchList):
            raise ValueError("PCRBatch list contains invalid input")
        if not self.iscsv():
            raise ValueError("CSV Path is Invalid")

    def accept(self):
        try:
            self.check_values()
        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))
            return
        super(MainBox, self).accept()

    def getValues(self):
        return self.PCRmmVol, self.PCRamount, self.PCRSampleVol, self.PCRBatchList, self.overhead, self.PCRLabware, self.PrimerLabware, self.filepath.text(), self.mailID.text(), self.CritVol, self.primerpath.text(), self.PCRPrimerVol, self.PCRmmTubeVol, self.PrimerStart


def readCSV():
    global dataframe_csv, repeatPCR, primerpath, primer_df, PCRLabware, DNALabware, PCRBatchList, dataframe, length, width, PCRWellMap, NFWaterVol, outputdir, filepath, PCRSampleVol, PCRamount, overhead, num_tips20, samplePlates, PCRPlates, deck_tips20, deck_samplePlates, deck_PCRPlates, PCRBatchList_str
    dataframe_csv = pandas.read_csv(filepath)
    primer_df = pandas.read_csv(primerpath)
    repeatPCR = False
    if not all(i in dataframe_csv.columns.tolist() for i in
               list(('SampleID', 'PCRBatch'))):
        raise Exception("Required Datafields missing in CSV")
    if not all(i in primer_df.columns.tolist() for i in
               list(('domain', 'plate', 'well_ID', 'target', 'barcode_ID', 'primerNumber', 'fwd_barcode', 'rev_barcode', 'fwd.rC_barcode', 'rev.rC_barcode', 'rev.rC_fwd'))):
        raise Exception("Required Datafields missing in Primer Data")
    if any(x < 0 for x in PCRBatchList):
        repeatPCR = True
        PCRBatchList = [-x for x in PCRBatchList]
        if not 'PCRResults' in dataframe_csv.columns:
            raise Exception("PCRResult column must be present in the data")
    PCRBatchList = list(dataframe_csv['PCRBatch'].unique()) if list(map(abs, PCRBatchList)) == [
        float('Inf')] else PCRBatchList
    PCRBatchList_str = ",".join(map(str, [int(i) for i in PCRBatchList if not math.isnan(i)]))
    dataframe_csv = dataframe_csv[dataframe_csv['PCRBatch'].isin(PCRBatchList)]
    dataframe_csv = dataframe_csv[~dataframe_csv['SampleID'].astype(str).str.contains("Standard")]
    dataframe = dataframe_csv[dataframe_csv['PCRResult']=='Fail'] if repeatPCR else dataframe_csv


def calculateDF():
    global repeatPCR, PrimerStart, Below_MinVol, Above_MaxVol, app, primerpath, primer_df, PCRLabware, DNALabware, PCRBatchList, dataframe, length, width, PCRWellMap, NFWaterVol, outputdir, filepath, PCRSampleVol, PCRamount, overhead, num_tips20, samplePlates, PCRPlates, deck_tips20, deck_samplePlates, deck_PCRPlates, PCRBatchList_str
    length = [24, 12, 6][[384, 96, 24].index(int(PCRLabware.split('_')[1]))]
    width = [16, 8, 4][[384, 96, 24].index(int(PCRLabware.split('_')[1]))]
    dataframe['SourcePlate'] = numpy.where(dataframe['DilutionPlate'] != '', dataframe['DilutionPlate'], dataframe['DNAPlate'])
    dataframe['SourceWell'] = numpy.where(dataframe['DilutionWell'] != '', dataframe['DilutionWell'], dataframe['DNAWell'])
    dataframe['SourceConc'] = numpy.where(dataframe['DilutedDNAConc'] != '', dataframe['DilutedDNAConc'], dataframe['AvgDNAConc'])
    dataframe['SourceVol'] = (PCRamount / dataframe['SourceConc']).round(1)
    dataframe['WaterVol'] = PCRSampleVol - dataframe['SourceVol']
    if len(primer_df) < len(dataframe):
        QMessageBox.information(None, 'Insufficient primers', 'Number of primers less than number of samples')
        quit()
    if len(dataframe) > int(PCRLabware.split('_')[1]):
        QMessageBox.information(None, 'Number of Samples Exceeded', 'This program is limited to process only 1 PCR plate at a time. Split into multiple PCRBatches and retry.')
        quit()
    currentPCRPlate = max([int(re.search(r'\d+', value).group()) for value in dataframe['PCRPlate'].unique()]) if 'PCRPlate' in dataframe.columns else 0
    currentPCRWell = 0
    for index, _ in (dataframe[dataframe['SourceVol'] >= CritVol].iterrows()):
        if currentPCRWell % (length * width) == 0:
            currentPCRPlate += 1
            currentPCRWell = 0
        dataframe.loc[index, ['PCRPlate', 'PCRWell']] = [f"PCRPlate-{PCRBatchList_str}-{currentPCRPlate}",
                                                              chr((currentPCRWell % width) + 65) + str(
                                                                  (currentPCRWell // width) + 1)]
        currentPCRWell += 1
    if not repeatPCR:
        primer_df = primer_df.iloc[PrimerStart:PrimerStart+len(dataframe)]
        dataframe.reset_index(inplace=True)
        primer_df.reset_index(inplace=True)
        dataframe = dataframe.merge(primer_df, left_index=True, right_index=True)
        dataframe = dataframe.rename(columns={primer_col: df_col for df_col, primer_col in zip(['PrimerPlate', 'PrimerWell', 'PrimerID', 'F', 'R', 'F-revC', 'R-revC', 'R-revC.F'], ['plate', 'well_ID', 'ref_paper_ID', 'fwd_barcode', 'rev_barcode', 'fwd_revC_barcode', 'rev_revC_barcode', 'revC_fwd'])})
        #dataframe = dataframe.assign(**{df_col: primer_df[primer_col] for df_col, primer_col in zip(['PrimerPlate', 'PrimerWell', 'PrimerID', 'F', 'R', 'F-revC', 'R-revC', 'R-revC.F'], ['plate', 'well_ID', 'ref_paper_ID', 'fwd_barcode', 'rev_barcode', 'fwd_revC_barcode', 'rev_revC_barcode', 'revC_fwd'])})
        dataframe['PrimerPlate'] = dataframe['PrimerPlate'].apply(lambda x: f'PrimerPlate{x}')
    Below_MinVol = len(dataframe[dataframe['SourceVol'] < CritVol])
    Above_MaxVol = len(dataframe[dataframe['SourceVol'] > PCRSampleVol])
    dataframe.loc[dataframe['SourceVol'] > PCRSampleVol, 'WaterVol'] = 0
    dataframe.loc[dataframe['SourceVol'] > PCRSampleVol, 'SourceVol'] = PCRSampleVol
    PCRWellMap = dataframe[['SourcePlate', 'SourceWell', 'SourceVol', 'WaterVol', 'PCRPlate', 'PCRWell', 'PrimerPlate', 'PrimerWell']].copy()
    dataframe = dataframe.drop(['SourcePlate', 'SourceWell', 'WaterVol', 'SourceConc'], axis=1)
    NFWaterVol = math.ceil(sum(PCRWellMap['WaterVol']) * overhead / 10 ) * 10
    dataframe.to_csv(f"{outputdir}/{os.path.splitext(os.path.basename(filepath))[0]}_PCRBatch{PCRBatchList_str}.Map.csv",
                     index=False)
    PCRWellMap.to_csv(f"{outputdir}/{os.path.splitext(os.path.basename(filepath))[0]}_PCRBatch{PCRBatchList_str}.Steps.csv",
                     index=False)

def deckSetup():
    global PCRLabware, DNALabware, PCRBatchList, dataframe, length, width, PCRWellMap, NFWaterVol, outputdir, filepath, PCRSampleVol, PCRamount, overhead, num_tips20, samplePlates, PCRPlates, primerPlates, deck_primerPlates, deck_tips20, deck_samplePlates, deck_PCRPlates, PCRBatchList_str
    num_tips20 = int(math.ceil(len(PCRWellMap) * 2 / 96))
    samplePlates = PCRWellMap['SourcePlate'].unique()
    PCRPlates = PCRWellMap['PCRPlate'].unique()
    primerPlates = PCRWellMap['PrimerPlate'].unique()
    if not 0 < num_tips20 + len(samplePlates) + len(PCRPlates) + len(primerPlates) <= 9:
        print("Not enough deck spaces to perform this run. Split into different Runs and Retry")
        raise ValueError
    currentDeck = 9
    deck_tips20 = list(zip(range(currentDeck, currentDeck := currentDeck - num_tips20, -1), ["Tip Rack 20ul"] * num_tips20))[::-1]
    deck_PCRPlates = list(zip(range(currentDeck, currentDeck := currentDeck - len(PCRPlates), -1),
                                   PCRPlates[::-1]))[::-1]
    deck_samplePlates = list(
        zip(range(currentDeck, currentDeck := currentDeck - len(samplePlates) , -1),
            samplePlates[::-1]))[::-1]
    deck_primerPlates = list(
        zip(range(currentDeck, currentDeck := currentDeck - len(primerPlates), -1),
            primerPlates[::-1]))[::-1]

    if any(samplePlates):
        LabwareChooser = LabwareWindow(samplePlates)
        if LabwareChooser.exec_():
            DNALabware = LabwareChooser.getValue()

def instructions():
    global PCRmmTubeVol, app, Below_MinVol, Above_MaxVol, PCRLabware, DNALabware, PrimerLabware, PCRBatchList, dataframe, length, width, PCRWellMap, NFWaterVol, outputdir, filepath, PCRSampleVol, PCRamount, overhead, num_tips20, samplePlates, PCRPlates, primerPlates, deck_primerPlates, deck_tips20, deck_samplePlates, deck_PCRPlates, PCRBatchList_str
    deck = []
    deck.extend(["Tip Rack 300ul", "Microcentrifuge Tube Rack"])
    deck.extend([j[1] for i in [deck_tips20[::-1], [(i[0], str(i[1])+f" (Labware: {PCRLabware})") for i in deck_PCRPlates[::-1]], [(i[0], str(i[1])+f" (Labware: {j})") for (i, j) in zip(deck_samplePlates[::-1], DNALabware[::-1])], [(i[0], str(i[1])+f" (Labware: {PrimerLabware})") for i in deck_primerPlates[::-1]]] for j in i])
    deck.extend(["Empty" for i in range(11 - len(deck))])
    deck.reverse()
    with open(
            f"{outputdir}/{os.path.splitext(os.path.basename(filepath))[0]}_PCRBatch{PCRBatchList_str}.OT2DeckSetup.txt",
            "w") as file:
        file.writelines(
            "Sample Information:\n\tSamples/Reactions: {}\n\tLow DNA samples (Capped at maximum sample volume): {}\n\tExcessive DNA samples (Skipped): {}\nPlate Information:\n\tSample plates: {}\n\tPrimer Plates: {}\n\tPCR Plates: {}\nPCR Information:\n\tMastermix Volume: {}\n\tPrimer Volume: {}\n\tMaximum Sample Volume: {}\n\tMinimum Sample Volume: {}\n\tOverhead: {}%\n\tTotal Nuclease Free Water: {}ml\n".format(
                len(PCRWellMap), Above_MaxVol, Below_MinVol, len(samplePlates), len(primerPlates), len(PCRPlates), PCRmmVol, PCRPrimerVol, PCRSampleVol, CritVol, round(((overhead - 1) * 100), 3), NFWaterVol))
        file.writelines("Setup the deck as shown below:\n")
        for i, str_1 in enumerate(deck):
            file.writelines(f"\tDeck {i + 1}: {str_1}\n")
        file.writelines(
            f"Place {NFWaterVol}ml Nuclease Free Water in a 2ml microcentrifuge tube in position D6 of the tube rack.\n")
        i=1
        file.writelines(
            f"Place atleast {min(len(PCRWellMap)*PCRmmVol*overhead, math.floor(PCRmmTubeVol))}ul of PicoGreen suplemented NEB Q5 HotStart 2x PCR MasterMix in position D{i} of the tube rack.\n")
        rem = len(PCRWellMap)
        while rem := (rem - min(rem, math.floor(PCRmmTubeVol/PCRmmVol))):
            i += 1
            file.writelines(f"Additionally place atleast {min((len(PCRWellMap)-math.floor(PCRmmTubeVol/PCRmmVol))*PCRmmVol*overhead, math.floor(PCRmmTubeVol))}ul of PicoGreen suplemented NEB Q5 HotStart 2x PCR MasterMix in position D{i} of the tube rack.\n")
            if i == 6:
                QMessageBox.information(None, 'Number of MasterMix Tubes Exceeded', 'Volume of Mastermix needed is too high.')
                quit()



def writeOT():
    global PCRLabware, DNALabware, PCRBatchList, dataframe, length, width, PCRWellMap, NFWaterVol, outputdir, filepath, PCRSampleVol, PCRamount, overhead, num_tips20, samplePlates, PCRPlates, deck_tips20, deck_samplePlates, deck_PCRPlates, PCRBatchList_str
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "dependencies\OT2PCRRun_Template.py"),
              "r") as template:
        contents = template.readlines()
        for num, line in enumerate(contents, 1):
            if "# Metadata" in line:
                break
        contents.insert(num,
                        f"metadata = {{\n    'protocolName': 'PCRPlate-{os.path.splitext(os.path.basename(filepath))[0]}_PCRBatch{PCRBatchList_str}',\n    'author': 'Generated by DNADilution.py; CC: Arval Viji Elango',\n    'apiLevel': '2.13'\n}}")
        for num, line in enumerate(contents, 1):
            if "# Variables" in line:
                break
        contents.insert(num, f"    deck_samplePlates = {deck_samplePlates}\n")
        contents.insert(num, f"    deck_PCRPlates = {deck_PCRPlates}\n")
        contents.insert(num, f"    deck_primerPlates = {deck_primerPlates}\n")
        contents.insert(num, f"    PCRWellMap_dict = {PCRWellMap.to_dict('list')}\n")
        contents.insert(num, f"    PCRPrimerVol = {PCRPrimerVol}\n")
        contents.insert(num, f"    PCRmmVol = {PCRmmVol}\n")
        contents.insert(num, f"    PCRmmTubeVol = {PCRmmTubeVol}\n")
        if not len(mailID) == 0:
            contents.insert(num, f"    emailID = '{mailID}'\n")
        for num, line in enumerate(contents, 1):
            if "# Labware" in line:
                break
        stringList = ""
        for j, layout in enumerate((deck_samplePlates)):
            if j > 0:
                stringList += ", "
            stringList += f"protocol.load_labware('{DNALabware[j]}', {layout[0]})"
        contents.insert(num, f"    samplePlates=[{stringList}]\n")
        stringList = ""
        for j, layout in enumerate((deck_PCRPlates)):
            if j > 0:
                stringList += ", "
            stringList += f"protocol.load_labware('{PCRLabware}', {layout[0]})"
        contents.insert(num, f"    PCRPlates=[{stringList}]\n")
        stringList = ""
        for j, layout in enumerate((deck_tips20)):
            if j > 0:
                stringList += ", "
            stringList += f"protocol.load_labware('opentrons_96_tiprack_20ul', {layout[0]})"
        contents.insert(num, f"    tips20=[{stringList}]\n")
        stringList = ""
        for j, layout in enumerate((deck_primerPlates)):
            if j > 0:
                stringList += ", "
            stringList += f"protocol.load_labware('{PrimerLabware}', {layout[0]})"
        contents.insert(num, f"    primerPlates=[{stringList}]\n")
        for num, line in enumerate(contents, 1):
            if "# Completion Mail" in line:
                break
        with open(
                f"{outputdir}/DilutionPlating_{os.path.splitext(os.path.basename(filepath))[0]}_PCRBatch{PCRBatchList_str}.OT2Run.py",
                "w") as file:
            file.seek(0)
            file.writelines(contents)
            file.close()
        template.close()
    return


if __name__ == '__main__':
    global PrimerStart, PCRmmTubeVol, app, primerpath, primer_df, PCRLabware, DNALabware, PrimerLabware, PCRBatchList, dataframe, length, width, PCRWellMap, NFWaterVol, outputdir, filepath, PCRSampleVol, PCRamount, overhead, num_tips20, samplePlates, PCRPlates, deck_tips20, deck_samplePlates, deck_PCRPlates, PCRBatchList_str
    app = QApplication([])
    mainDialog = MainBox()
    if mainDialog.exec_():
        PCRmmVol, PCRamount, PCRSampleVol, PCRBatchList, overhead, PCRLabware, PrimerLabware, filepath, mailID, CritVol, primerpath, PCRPrimerVol, PCRmmTubeVol, PrimerStart = mainDialog.getValues()

    outputdir = f"{os.path.split(filepath)[0]}/PCROutput"
    if not os.path.exists(outputdir):
        os.makedirs(outputdir)

    readCSV()
    calculateDF()
    deckSetup()
    instructions()
    writeOT()
    QMessageBox.information(None, 'Finish', 'Program has completed running')
    quit()
