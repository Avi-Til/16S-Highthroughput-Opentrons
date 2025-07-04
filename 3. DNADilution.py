from PyQt5.QtWidgets import QApplication, QLineEdit, QFileDialog, QVBoxLayout, QComboBox, QFormLayout, QButtonGroup, \
    QLabel, QDialogButtonBox, QRadioButton, QDialog, QPushButton, QMessageBox
from PyQt5 import QtCore
import re, math, csv, pandas, os, numpy
from collections import defaultdict


class AdvancedInputBox(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.DilutedVol = QLineEdit()
        self.DilutedVol.setText(str(self.parent().DilutedVol))
        self.CritVol = QLineEdit()
        self.CritVol.setText(str(self.parent().CritVol))
        self.overhead = QLineEdit()
        self.overhead.setText(str(self.parent().overhead))
        self.PCRamount = QLineEdit()
        self.PCRamount.setText(str(self.parent().PCRamount))
        self.openAdvancedDialog()

    def openAdvancedDialog(self):
        FormLayout = QFormLayout()
        FormLayout.addRow("Volume of diluted sample to prepare (ul) (Default: 20):", self.DilutedVol)
        FormLayout.addRow("Critical PCR sample pipetting volume (ul) (Default: 5):", self.CritVol)
        FormLayout.addRow("Amount of DNA per PCR reaction (ng) (Default: 5):", self.PCRamount)
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
        LabwareLayout.addWidget(QLabel("Choose the appropriate labware for the DNA Samples"))
        self.DNAPlateDropDown = QComboBox()
        self.DNAPlateDropDown.addItems(LabwareList)
        self.DNAPlateDropDown.setCurrentIndex(LabwareList.index(self.parent().DNALabware))
        LabwareLayout.addWidget(self.DNAPlateDropDown)
        LabwareLayout.addWidget(QLabel("Choose the appropriate labware for the DilutionPlate"))
        self.DilutionPlateDropDown = QComboBox()
        self.DilutionPlateDropDown.addItems(LabwareList)
        self.DilutionPlateDropDown.setCurrentIndex(LabwareList.index(self.parent().DilutionLabware))
        LabwareLayout.addWidget(self.DilutionPlateDropDown)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Close)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.close)

        layout = QVBoxLayout()
        layout.addLayout(FormLayout)
        layout.addLayout(LabwareLayout)
        layout.addWidget(buttonBox)

        self.setLayout(layout)

    def getValues(self):
        return float(self.DilutedVol.text()), float(self.overhead.text()), float(
            self.PCRamount.text()), self.DNAPlateDropDown.currentText(), self.DilutionPlateDropDown.currentText(), float(
            self.CritVol.text())


class MainBox(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.DilutedVol = 20
        self.overhead = 1.04
        self.PCRamount = 5
        self.CritVol = 5
        self.DNALabware = "eppendorf96wellpcrplatetwin.tecskirted_96_wellplate_150ul"
        self.DilutionLabware = "eppendorf96wellpcrplatetwin.tecskirted_96_wellplate_150ul"
        self.createLayout()

    def createLayout(self):
        layout1 = QVBoxLayout()
        layout1.addWidget(QLabel("Select the Dilution Batch (Ex. 1,3-5):"))
        self.RunGroup = QButtonGroup(self)
        self.allButton = QRadioButton("All")
        self.listButton = QRadioButton("List")
        self.RunGroup.addButton(self.listButton)
        self.RunGroup.addButton(self.allButton)
        layout1.addWidget(self.allButton)
        layout1.addWidget(self.listButton)
        self.listEdit = QLineEdit()
        layout1.addWidget(self.listEdit)
        self.filepath = QLineEdit()
        layout1.addWidget(QLabel("File Path:"))
        layout1.addWidget(self.filepath)
        button = QPushButton("Choose File")
        button.clicked.connect(self.choose_file)
        layout1.addWidget(button)
        self.mailID = QLineEdit()
        layout1.addWidget(QLabel("Enter email to notify on run completion:"))
        layout1.addWidget(self.mailID)

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
            self.DilutedVol, self.overhead, self.PCRamount, self.DNALabware, self.DilutionLabware, self.CritVol = self.advancedBox.getValues()

    def choose_file(self):
        # Open the file dialog and get the selected file path
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("CSV files (*.csv)")
        self.filepath.setText(file_dialog.getOpenFileName()[0])

    def dilutionBatch_toList(self):
        if self.listButton.isChecked():
            text = self.listEdit.text()
            text = re.sub(r'\s', '', text)
            if re.match(r'^\d+([,-]\d+)*$', text):
                self.DilutionBatchList = []
                for part in text.split(','):
                    if '-' in part:
                        start, end = map(int, part.split('-'))
                        self.DilutionBatchList.extend(range(start, end + 1))
                    else:
                        self.DilutionBatchList.append(int(part))
                return
            elif text:
                self.DilutionBatchList = [float('NaN')]
                return
        elif self.allButton.isChecked():
            self.DilutionBatchList = [float('Inf')]
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
            self.dilutionBatch_toList()

        if not 1 < self.overhead <= 1.25:
            raise ValueError("Overhead must be between 1.000 and 1.250")
        if not all([self.DilutedVol, self.PCRamount, self.DilutionBatchList, self.overhead]):
            raise ValueError("Required parameters are missing")
        if any(math.isnan(i) for i in self.DilutionBatchList):
            raise ValueError("DilutionBatch list contains invalid input")
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
        return self.PCRamount, self.DilutedVol, self.DilutionBatchList, self.overhead, self.DNALabware, self.DilutionLabware, self.filepath.text(), self.mailID.text(), self.CritVol


class HighConcHandlerBox(QDialog):
    def __init__(self, num_ConcExceed, num_samples, parent=None):
        super().__init__(parent)
        self.num_ConcExceed = num_ConcExceed
        self.num_Samples = num_samples
        self.initUI()

    def initUI(self):
        self.openAdvancedDialog()

    def openAdvancedDialog(self):
        LabwareList = ["Skip samples that require multi-step dilution", "eppendorf96wellpcrplatetwin.tecskirted_96_wellplate_150ul",
                       "fishersciflatbottomplatepicogreen_96_wellplate_250ul",
                       "nest_96_wellplate_100ul_pcr_full_skirt", "nest_96_wellplate_200ul_flat",
                       "biorad_96_wellplate_200ul_pcr", "armadillo_96_wellplate_200ul_pcr_full_skirt",
                       "opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap",
                       "opentrons_24_tuberack_eppendorf_2ml_safelock_snapcap",
                       "opentrons_24_tuberack_nest_0.5ml_screwcap",
                       "opentrons_24_tuberack_nest_1.5ml_screwcap",
                       "opentrons_24_tuberack_nest_2ml_screwcap",
                       "appliedbiosystemsmicroamp_384_wellplate_40ul", "biorad_384_wellplate_50ul"]
        HighConcHandlerLayout = QVBoxLayout()
        HighConcHandlerLayout.addWidget(QLabel(f"{self.num_ConcExceed} out of {self.num_Samples} samples, require a multi-step dilution. Choose labware to perform the intermediate dilution, or skip these samples."))
        self.IntermediatePlateDropDown = QComboBox()
        self.IntermediatePlateDropDown.addItems(LabwareList)
        self.IntermediatePlateDropDown.setCurrentIndex(0)
        HighConcHandlerLayout.addWidget(self.IntermediatePlateDropDown)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Close)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.close)

        layout = QVBoxLayout()
        layout.addLayout(HighConcHandlerLayout)
        layout.addWidget(buttonBox)

        self.setLayout(layout)

    def getValue(self):
        return '' if self.IntermediatePlateDropDown.currentText() == "Skip samples that require multi-step dilution" else self.IntermediatePlateDropDown.currentText()


def readCSV():
    global IntermediateLabware, intermediatePlates, deck_intermediatePlates, DilutionLabware, DNALabware, DilutionBatchList, dataframe, dil_l, dil_w, dilutionWellMap, NFWaterVol, outputdir, filepath, DilutedVol, PCRamount, overhead, num_tips20, samplePlates, dilutionPlates, deck_tips20, deck_samplePlates, deck_dilutionPlates, DilutionBatchList_str
    dataframe = pandas.read_csv(filepath, converters=defaultdict(lambda i: str))
    if not all(i in dataframe.columns.tolist() for i in
               list(('DNAWell', 'DNAPlate', 'DilutionBatch', 'SampleID', 'AvgDNAConc'))):
        raise Exception("Required Datafields missing in CSV")
    DilutionBatchList = list(dataframe['DilutionBatch'].unique()) if DilutionBatchList == [
        float('Inf')] else DilutionBatchList
    DilutionBatchList_str = ",".join(map(str, [int(i) for i in DilutionBatchList if not math.isnan(i)]))
    dataframe = dataframe[dataframe['DilutionBatch'].isin(DilutionBatchList)]
    dataframe = dataframe[~dataframe['SampleID'].astype(str).str.contains("Standard")]

MaxLabwareVol = (lambda s: next(
        (float(match.group(1)) * (1000 if match.group(2) == 'ml' else 1) for substring in s.split('_') if
         (match := re.fullmatch(r'(\d+(?:\.\d+)?)\s*(ml|ul)', substring))), None))

def calculateDF():
    global app, IntermediateLabware, MaxLabwareVol, intermediatePlates, deck_intermediatePlates, DilutionLabware, DNALabware, DilutionBatchList, dataframe, dil_l, dil_w, dilutionWellMap, NFWaterVol, outputdir, filepath, DilutedVol, PCRamount, overhead, num_tips20, samplePlates, dilutionPlates, deck_tips20, deck_samplePlates, deck_dilutionPlates, DilutionBatchList_str
    MaxLabwareVol = (lambda s: next(
        (float(match.group(1)) * (1000 if match.group(2) == 'ml' else 1) for substring in s.split('_') if
         (match := re.fullmatch(r'(\d+(?:\.\d+)?)\s*(ml|ul)', substring))), None))
    CriticalLowConc = PCRamount / DilutedVol
    CriticalHighConc = PCRamount / CritVol
    dil_l = [24, 12, 6][[384, 96, 24].index(int(DilutionLabware.split('_')[1]))]
    dil_w = [16, 8, 4][[384, 96, 24].index(int(DilutionLabware.split('_')[1]))]
    IntermediateLabware = ''
    if (num_ConcExceed := len(dataframe[dataframe['AvgDNAConc'] / CriticalHighConc > MaxLabwareVol(DilutionLabware) / 2])):
        highConcHandler = HighConcHandlerBox(num_ConcExceed, len(dataframe))
        if highConcHandler.exec_():
            IntermediateLabware = highConcHandler.getValue()
    if IntermediateLabware:
        MaxIntermediateWellVol = MaxLabwareVol(IntermediateLabware)
        int_l = [24, 12, 6][[384, 96, 24].index(int(IntermediateLabware.split('_')[1]))]
        int_w = [16, 8, 4][[384, 96, 24].index(int(IntermediateLabware.split('_')[1]))]

    def dilutionCalc(DNAConc, MaxWellVol):
        dilutionFactor = DNAConc / CriticalHighConc
        dilutionDNAVol = max(2, math.ceil(10 * DilutedVol / dilutionFactor) / 10)
        dilutionWaterVol = min(MaxWellVol - dilutionDNAVol,
                               math.ceil(10 * (dilutionFactor - 1) * dilutionDNAVol) / 10)
        dilutionFactor = (dilutionDNAVol + dilutionWaterVol) / dilutionDNAVol
        dilutedDNAConc = DNAConc / dilutionFactor
        return dilutionFactor, dilutionDNAVol, dilutionWaterVol, dilutedDNAConc

    dilutionWellMap = pandas.DataFrame(
        columns=['SourcePlate', 'SourceWell', 'SourceVol', 'WaterVol', 'DestinationPlate', 'DestinationWell'])
    dataframe = dataframe.assign(DilutionFactor=1, DilutedDNAConc='', DilutionPlate='', DilutionWell='')
    currentDilutionPlate, currentDilutionWell, currentIntermediatePlate, currentIntermediateWell = 0, 0, 0, 0
    for index, _ in dataframe.iterrows():
        if float(dataframe.loc[index, 'AvgDNAConc']) > CriticalHighConc:
            currentSourcePlate, currentSourceWell = dataframe.loc[index, 'DNAPlate'], dataframe.loc[index, 'DNAWell']
            dilutionFactor, dilutionDNAVol, dilutionWaterVol, dilutedDNAConc = dilutionCalc(
                float(dataframe.loc[index, 'AvgDNAConc']), MaxLabwareVol(DilutionLabware))
            while dilutedDNAConc > CriticalHighConc:
                if IntermediateLabware:
                    dilutionFactor, dilutionDNAVol, dilutionWaterVol, dilutedDNAConc = dilutionCalc(
                        float(dataframe.loc[index, 'AvgDNAConc'] if dataframe.loc[index, 'DilutionFactor'] == 1 else dilutedDNAConc), MaxIntermediateWellVol)
                    if currentIntermediateWell % (int_l * int_w) == 0:
                        currentIntermediatePlate += 1
                        currentIntermediateWell = 0
                    currentDestinationPlate = f"IntermediatePlate{currentIntermediatePlate}"
                    currentDestinationWell = chr((currentIntermediateWell % int_w) + 65) + str(
                        (currentIntermediateWell // int_w) + 1)
                    dataframe.loc[index, 'DilutionFactor'] = dataframe.loc[index, 'DilutionFactor'] * dilutionFactor
                    dilutionWellMap = pandas.concat([dilutionWellMap, pandas.DataFrame(
                        {'SourcePlate': [currentSourcePlate], 'SourceWell': [currentSourceWell],
                         'SourceVol': [dilutionDNAVol],
                         'WaterVol': [dilutionWaterVol], 'DestinationPlate': [currentDestinationPlate],
                         'DestinationWell': [currentDestinationWell]})])
                    currentSourcePlate = currentDestinationPlate
                    currentSourceWell = currentDestinationWell
                    dilutionFactor, dilutionDNAVol, dilutionWaterVol, dilutedDNAConc = dilutionCalc(dilutedDNAConc, MaxLabwareVol(DilutionLabware))
                    currentIntermediateWell += 1
                else:
                    dilutedDNAConc, dilutionDNAVol, dilutionWaterVol, dilutionFactor = float('NaN'), float('NaN'), float('NaN'), (float(dataframe.loc[index, 'AvgDNAConc'])/CriticalHighConc)
                    #MOD1: The previous line assigns NaN values to concentrations which are too high to be diluted without IntermediatePlate. If NaN is assigned, the dilutionPlate skips over it without leaving an empty well. When assigned 0 like below, it leaves an empty well instead
                    #dilutedDNAConc, dilutionDNAVol, dilutionWaterVol, dilutionFactor = float(0), float(0), float(0), (float(dataframe.loc[index, 'AvgDNAConc']) / CriticalHighConc)
                    break
            if currentDilutionWell % (dil_l * dil_w) == 0:
                currentDilutionPlate += 1
                currentDilutionWell = 0
            currentDestinationPlate = f"DilutionPlate{currentDilutionPlate}"
            currentDestinationWell = chr((currentDilutionWell % dil_w) + 65) + str((currentDilutionWell // dil_w) + 1)
            dataframe.loc[index, ['DilutionPlate', 'DilutionWell', 'DilutedDNAConc']] = [currentDestinationPlate,
                                                                                         currentDestinationWell,
                                                                                         dilutedDNAConc]
            dataframe.loc[index, 'DilutionFactor'] = dataframe.loc[index, 'DilutionFactor'] * dilutionFactor
            dilutionWellMap = pandas.concat([dilutionWellMap, pandas.DataFrame(
                {'SourcePlate': [currentSourcePlate], 'SourceWell': [currentSourceWell], 'SourceVol': [dilutionDNAVol],
                 'WaterVol': [dilutionWaterVol], 'DestinationPlate': [currentDestinationPlate],
                 'DestinationWell': [currentDestinationWell]})]) if not math.isnan(dilutionDNAVol) else dilutionWellMap
            # MOD1: The commented bit of conditional code skips a well in the dilutionPlate if there is a well with DNA too high to be diluted. When it is commented, it will instead leave an empty well.
            currentDilutionWell += 1
        elif float(dataframe.loc[index, 'AvgDNAConc']) <= CriticalHighConc:
            dataframe.loc[index, 'DilutionFactor'] = 0
            #MOD2
            currentSourcePlate, currentSourceWell = dataframe.loc[index, 'DNAPlate'], dataframe.loc[index, 'DNAWell']
            dilutionFactor, dilutionDNAVol, dilutionWaterVol, dilutedDNAConc = float(0), float(DilutedVol), float(0), float(dataframe.loc[index, 'AvgDNAConc'])
            if currentDilutionWell % (dil_l * dil_w) == 0:
                currentDilutionPlate += 1
                currentDilutionWell = 0
            currentDestinationPlate = f"DilutionPlate{currentDilutionPlate}"
            currentDestinationWell = chr((currentDilutionWell % dil_w) + 65) + str((currentDilutionWell // dil_w) + 1)
            dataframe.loc[index, ['DilutionPlate', 'DilutionWell', 'DilutedDNAConc']] = [currentDestinationPlate,
                                                                                         currentDestinationWell,
                                                                                         dilutedDNAConc]
            dilutionWellMap = pandas.concat([dilutionWellMap, pandas.DataFrame(
                {'SourcePlate': [currentSourcePlate], 'SourceWell': [currentSourceWell], 'SourceVol': [dilutionDNAVol],
                 'WaterVol': [dilutionWaterVol], 'DestinationPlate': [currentDestinationPlate],
                 'DestinationWell': [currentDestinationWell]})])
            currentDilutionWell += 1
            #MOD2: If this code block is enabled instead of the other MOD2 code block, the wells that do not need dilution will be skipped instead of transfering complete required volume.
    if (len(dilutionWellMap)==len(dataframe)) and (sum(dilutionWellMap['WaterVol'])==0):
        QMessageBox.information(None, 'No Dilutions required', 'No dilutions are required for the given parameters and DNA Concentrations. Proceed to the next step.')
        quit()
    outputdir = f"{os.path.split(filepath)[0]}/DNADilutionOutput"
    if not os.path.exists(outputdir):
        os.makedirs(outputdir)
    NFWaterVol = math.ceil(sum(dilutionWellMap['WaterVol']) * overhead / 100) / 10
    dataframe.to_csv(f"{outputdir}/{os.path.splitext(os.path.basename(filepath))[0]}_DilutionBatch{DilutionBatchList_str}.Map.csv",
                     index=False)
    dilutionWellMap.to_csv(f"{outputdir}/{os.path.splitext(os.path.basename(filepath))[0]}_DilutionBatch{DilutionBatchList_str}.Steps.csv",
                           index=False)


def deckSetup():
    global IntermediateLabware, intermediatePlates, deck_intermediatePlates, DilutionLabware, DNALabware, DilutionBatchList, dataframe, dil_l, dil_w, dilutionWellMap, NFWaterVol, outputdir, filepath, DilutedVol, PCRamount, overhead, num_tips20, samplePlates, dilutionPlates, deck_tips20, deck_samplePlates, deck_dilutionPlates, DilutionBatchList_str
    num_tips20 = int(math.ceil(len(dilutionWellMap['SourceWell']) / 96))
    dilutionWellMap['SourcePlate'] = dilutionWellMap['SourcePlate'].astype(str)
    samplePlates = dilutionWellMap[~dilutionWellMap['SourcePlate'].str.contains('IntermediatePlate')][
        'SourcePlate'].unique()
    intermediatePlates = dilutionWellMap[dilutionWellMap['DestinationPlate'].str.contains('IntermediatePlate')]['DestinationPlate'].unique()
    dilutionPlates = dilutionWellMap[dilutionWellMap['DestinationPlate'].str.contains('DilutionPlate')]['DestinationPlate'].unique()
    if not 0 < num_tips20 + len(samplePlates) + len(dilutionPlates) + len(intermediatePlates) <= 9:
        print("Not enough deck spaces to perform this run. Split into different Dilution Batches or change Intermediate Labware and Retry")
        raise ValueError
    deck_tips20 = list(zip(range(9, 9 - num_tips20, -1), ["Tip Rack 20ul"] * num_tips20))[::-1]
    deck_dilutionPlates = list(zip(range(9 - num_tips20, 9 - num_tips20 - len(dilutionPlates), -1),
                                   dilutionPlates[::-1]))[::-1]
    deck_intermediatePlates = list(zip(range(9 - num_tips20 - len(dilutionPlates), 9 - num_tips20 - len(dilutionPlates) - len(intermediatePlates), -1), intermediatePlates[::-1]))[::-1]
    deck_samplePlates = list(
        zip(range(9 - num_tips20 - len(dilutionPlates)- len(intermediatePlates), 9 - num_tips20 - len(dilutionPlates) - len(intermediatePlates) - len(samplePlates), -1),
            samplePlates[::-1]))[::-1]


def instructions():
    global IntermediateLabware, MaxLabwareVol, intermediatePlates, deck_intermediatePlates, DilutionLabware, DNALabware, DilutionBatchList, dataframe, dil_l, dil_w, dilutionWellMap, NFWaterVol, outputdir, filepath, DilutedVol, PCRamount, overhead, num_tips20, samplePlates, dilutionPlates, deck_tips20, deck_samplePlates, deck_dilutionPlates, DilutionBatchList_str
    deck = []
    deck.extend(["Tip Rack 300ul", "6x15ml & 4x50ml Tube Rack"])
    deck.extend([j[1] for i in [deck_tips20[::-1], deck_dilutionPlates[::-1], deck_intermediatePlates[::-1], deck_samplePlates[::-1]] for j in i])
    deck.extend(["Empty" for i in range(11 - len(deck))])
    deck.reverse()
    with open(
            f"{outputdir}/{os.path.splitext(os.path.basename(filepath))[0]}_DilutionBatch{DilutionBatchList_str}.OT2DeckSetup.txt",
            "w") as file:
        file.writelines(
            "Run Information:\n\tSamples requiring dilution: {}\n\tSamples below required concentration: {}\n\tSamples requiring multi-step dilution: {}\n\tSkip multi-step dilution: {}\n\tDilution Steps: {}\n\tSample plates: {}\n\tIntermediate Plates: {}\n\tDilution Plates: {}\n\tOverhead: {}%\n\tNuclease Free Water: {}ml\n\tSample Labware: {}\n\tDilution Labware: {}\n\tIntermediate Labware: {}\n".format(
                len(dataframe[dataframe['DilutionFactor'] > 1]), len(dataframe[dataframe['DilutionFactor'] < 1]), len(dataframe[dataframe['DilutionFactor'] > MaxLabwareVol(DilutionLabware) / 2]), (not IntermediateLabware), len(dilutionWellMap), len(samplePlates),
                len(intermediatePlates), len(dilutionPlates), round(((overhead - 1) * 100), 3), NFWaterVol, DNALabware, DilutionLabware, IntermediateLabware))
        file.writelines("Setup the deck as shown below:\n")
        for i, str in enumerate(deck):
            file.writelines(f"\tDeck {i + 1}: {str}\n")
        file.writelines(
            f"Place {NFWaterVol}ml Nuclease Free Water in a 50ml tube in position A4 of the tube rack.\n")


def writeOT():
    global IntermediateLabware, intermediatePlates, deck_intermediatePlates, DilutionLabware, DNALabware, DilutionBatchList, dataframe, dil_l, dil_w, dilutionWellMap, NFWaterVol, outputdir, filepath, DilutedVol, PCRamount, overhead, num_tips20, samplePlates, dilutionPlates, deck_tips20, deck_samplePlates, deck_dilutionPlates, DilutionBatchList_str
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "dependencies\OT2DilutionRun_Template.py"),
              "r") as template:
        contents = template.readlines()
        for num, line in enumerate(contents, 1):
            if "# Metadata" in line:
                break
        contents.insert(num,
                        f"metadata = {{\n    'protocolName': 'DilutionPlate-{os.path.splitext(os.path.basename(filepath))[0]}_DilutionBatch{DilutionBatchList_str}',\n    'author': 'Generated by DNADilution.py; CC: Arval Viji Elango',\n    'apiLevel': '2.13'\n}}")
        for num, line in enumerate(contents, 1):
            if "# Variables" in line:
                break
        contents.insert(num, f"    deck_samplePlates = {deck_samplePlates}\n")
        contents.insert(num, f"    deck_intermediatePlates = {deck_intermediatePlates}\n")
        contents.insert(num, f"    deck_dilutionPlates = {deck_dilutionPlates}\n")
        contents.insert(num, f"    dilutionWellMap_dict = {dilutionWellMap.to_dict('list')}\n")
        if not len(mailID) == 0:
            contents.insert(num, f"    emailID = '{mailID}'\n")
        for num, line in enumerate(contents, 1):
            if "# Labware" in line:
                break
        stringList = ""
        for j, layout in enumerate((deck_samplePlates)):
            if j > 0:
                stringList += ", "
            stringList += f"protocol.load_labware('{DNALabware}', {layout[0]})"
        contents.insert(num, f"    samplePlates=[{stringList}]\n")
        stringList = ""
        for j, layout in enumerate((deck_intermediatePlates)):
            if j > 0:
                stringList += ", "
            stringList += f"protocol.load_labware('{IntermediateLabware}', {layout[0]})"
        contents.insert(num, f"    intermediatePlates=[{stringList}]\n")
        stringList = ""
        for j, layout in enumerate((deck_dilutionPlates)):
            if j > 0:
                stringList += ", "
            stringList += f"protocol.load_labware('{DilutionLabware}', {layout[0]})"
        contents.insert(num, f"    dilutionPlates=[{stringList}]\n")
        stringList = ""
        for j, layout in enumerate((deck_tips20)):
            if j > 0:
                stringList += ", "
            stringList += f"protocol.load_labware('opentrons_96_tiprack_20ul', {layout[0]})"
        contents.insert(num, f"    tips20=[{stringList}]\n")
        for num, line in enumerate(contents, 1):
            if "# Completion Mail" in line:
                break
        with open(
                f"{outputdir}/DilutionPlating_{os.path.splitext(os.path.basename(filepath))[0]}_DilutionBatch{DilutionBatchList_str}.OT2Run.py",
                "w") as file:
            file.seek(0)
            file.writelines(contents)
            file.close()
        template.close()
    return


if __name__ == '__main__':
    global app, IntermediateLabware, intermediatePlates, deck_intermediatePlates, DilutionLabware, DNALabware, DilutionBatchList, dataframe, dil_l, dil_w, dilutionWellMap, NFWaterVol, outputdir, filepath, DilutedVol, PCRamount, overhead, num_tips20, samplePlates, dilutionPlates, deck_tips20, deck_samplePlates, deck_dilutionPlates, DilutionBatchList_str
    app = QApplication([])
    mainDialog = MainBox()
    if mainDialog.exec_():
        PCRamount, DilutedVol, DilutionBatchList, overhead, DNALabware, DilutionLabware, filepath, mailID, CritVol = mainDialog.getValues()

    readCSV()
    calculateDF()
    deckSetup()
    instructions()
    writeOT()
    QMessageBox.information(None, 'Finish', 'Program has completed running.')
    quit()