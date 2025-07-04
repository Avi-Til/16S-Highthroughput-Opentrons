from PyQt5.QtWidgets import QApplication, QLineEdit, QFileDialog, QVBoxLayout, QComboBox, QFormLayout, QButtonGroup, \
    QLabel, QDialogButtonBox, QRadioButton, QDialog, QPushButton, QMessageBox
from PyQt5 import QtCore
import re, math, csv, pandas, os
from collections import Counter

class AdvancedInputBox(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.reps = QLineEdit()
        self.reps.setText(str(self.parent().reps))
        self.std_concText = QLineEdit()
        self.std_concText.setText(self.parent().std_concText)
        self.std_work_conc = QLineEdit()
        self.std_work_conc.setText(str(self.parent().std_work_conc))
        self.well_sample_vol = QLineEdit()
        self.well_sample_vol.setText(str(self.parent().well_sample_vol))
        self.well_dnasol_vol = QLineEdit()
        self.well_dnasol_vol.setText(str(self.parent().well_dnasol_vol))
        self.well_pico_vol = QLineEdit()
        self.well_pico_vol.setText(str(self.parent().well_pico_vol))
        self.overhead = QLineEdit()
        self.overhead.setText(str(self.parent().overhead))
        self.openAdvancedDialog()

    def openAdvancedDialog(self):
        StdLayout = QVBoxLayout()
        StdLayout.addWidget(QLabel(
            "List of DNA Standards (ng/ul) ('-': Empty wells) (Default: 1, 0.5, 0.2, 0.1, 0.05, 0.02, 0.01, 0) :"))
        StdLayout.addWidget(self.std_concText)
        FormLayout = QFormLayout()
        FormLayout.addRow("Working Concentration of DNA Standard (ng/ul) (Default: 2):", self.std_work_conc)
        FormLayout.addRow("Number of replicates (Default: 2):", self.reps)
        FormLayout.addRow("Volume of Sample per well (ul) (Default: 2):", self.well_sample_vol)
        FormLayout.addRow("Volume of Diluted Sample per well (ul) (Default: 100):", self.well_dnasol_vol)
        FormLayout.addRow("Volume of Pico Working Reagent per well (ul) (Default: 100):", self.well_pico_vol)
        FormLayout.addRow("Overheads (Default: 1.04):", self.overhead)

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
        LabwareLayout.addWidget(QLabel("Choose the appropriate labware for the PicoPlate"))
        self.PicoPlateDropDown = QComboBox()
        self.PicoPlateDropDown.addItems(LabwareList)
        self.PicoPlateDropDown.setCurrentIndex(LabwareList.index(self.parent().PicoLabware))
        LabwareLayout.addWidget(self.PicoPlateDropDown)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Close)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.close)

        layout = QVBoxLayout()
        layout.addLayout(StdLayout)
        layout.addLayout(FormLayout)
        layout.addLayout(LabwareLayout)
        layout.addWidget(buttonBox)

        self.setLayout(layout)

    def getValues(self):
        return int(self.reps.text()), self.std_concText.text(), float(self.std_work_conc.text()), float(
            self.well_sample_vol.text()), float(self.well_dnasol_vol.text()), float(self.well_pico_vol.text()), float(
            self.overhead.text()), self.DNAPlateDropDown.currentText(), self.PicoPlateDropDown.currentText()


class MainInputBox(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.PicoBatchList = []
        self.path = ""
        self.std_conc = []

        self.reps = 2
        self.std_concText = "1, 0.5, 0.2, 0.1, 0.05, 0.02, 0.01, 0"
        # [1.00, 0.4, 0.08, 0.032, 0.0064, 0.0025, 0.0005, 0][1, 0.8, 0.4, 0.3, 0.15, 0.12, 0.06, 0][0.1, 0.08, 0.04, 0.03, 0.015, 0.012, 0.006, 0][0.01, 0.008, 0.004, 0.003, 0.0015, 0.0012, 0.0006]
        self.std_work_conc = 2
        self.well_sample_vol = 2
        self.well_dnasol_vol = 100
        self.well_pico_vol = 100
        self.overhead = 1.04
        self.DNALabware = "eppendorf96wellpcrplatetwin.tecskirted_96_wellplate_150ul"
        self.PicoLabware = "fishersciflatbottomplatepicogreen_96_wellplate_250ul"
        self.createLayout()

    def createLayout(self):

        layout1 = QVBoxLayout()
        layout1.addWidget(QLabel("Select the Pico Batch (Ex. 1,3-5):"))
        self.RunGroup = QButtonGroup(self)
        self.allButton = QRadioButton("All")
        self.listButton = QRadioButton("List")
        self.RunGroup.addButton(self.listButton)
        self.RunGroup.addButton(self.allButton)
        layout1.addWidget(self.allButton)
        layout1.addWidget(self.listButton)
        self.listEdit = QLineEdit()
        layout1.addWidget(self.listEdit)
        layout1.addWidget(QLabel("Select the number of standard curves:"))
        self.StdGroup = QButtonGroup(self)
        self.noneButton = QRadioButton("No standard curve")
        self.onceButton = QRadioButton("Single standard curve for this run")
        self.everyButton = QRadioButton("Separate standard curves for each PicoPlate in this run")
        self.StdGroup.addButton(self.noneButton)
        self.StdGroup.addButton(self.onceButton)
        self.StdGroup.addButton(self.everyButton)
        layout1.addWidget(self.noneButton)
        layout1.addWidget(self.onceButton)
        layout1.addWidget(self.everyButton)
        self.path = QLineEdit()
        layout1.addWidget(QLabel("File Path:"))
        layout1.addWidget(self.path)
        button = QPushButton("Choose File")
        button.clicked.connect(self.ChooseFile)
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

    def showAdvancedDialog(self):
        self.advancedBox = AdvancedInputBox(self)
        self.advancedBox.exec_()
        if self.advancedBox.result() == QDialog.Accepted:
            self.reps, self.std_concText, self.std_work_conc, self.well_sample_vol, self.well_dnasol_vol, self.well_pico_vol, self.overhead, self.DNALabware, self.PicoLabware = self.advancedBox.getValues()

    def ChooseFile(self):
        # Open the file dialog and get the selected file path
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("CSV files (*.csv)")
        file_path = file_dialog.getOpenFileName()[0]
        self.path.setText(file_path)

    def eventFilter(self, watched, event):
        if watched == self.listEdit and event.type() == QtCore.QEvent.MouseButtonPress:
            self.listButton.setChecked(True)
            self.listEdit.setEnabled(True)
        return super().eventFilter(watched, event)

    def PicoBatch_toList(self):
        if self.listButton.isChecked():
            text = self.listEdit.text()
            text = re.sub(r'\s', '', text)
            if re.match(r'^\d+([,-]\d+)*$', text):
                self.PicoBatchList = []
                for part in text.split(','):
                    if '-' in part:
                        start, end = map(int, part.split('-'))
                        self.PicoBatchList.extend(range(start, end + 1))
                    else:
                        self.PicoBatchList.append(int(part))
                return
            elif text:
                self.PicoBatchList = [float('NaN')]
                return
        elif self.allButton.isChecked():
            self.PicoBatchList = [float('Inf')]
            return

    def updateStdCount(self):
        if self.noneButton.isChecked():
            self.num_std_array = 0
        elif self.onceButton.isChecked():
            self.num_std_array = 1
        else:
            self.num_std_array = float('Inf')
        return

    def StdConc_toList(self):
        for conc in self.std_concText.replace(' ', '').split(','):
            if conc == '-':
                self.std_conc.append(math.nan)
            else:
                try:
                    self.std_conc.append(float(conc))
                except:
                    raise ValueError("Non-float entry in standards")
        return

    def iscsv(self):
        try:
            with open(self.path.text(), newline='') as f:
                reader = csv.reader(f)
                next(reader)
        except (csv.Error, FileNotFoundError):
            return False
        return True

    def check_values(self):
        if self.RunGroup.checkedButton() is None or self.StdGroup.checkedButton() is None:
            raise ValueError("Required options are missing")
        else:
            self.PicoBatch_toList()
            self.updateStdCount()
        self.StdConc_toList()
        if self.reps not in range(1, 4):
            raise ValueError("Number of replicates must be between 1 and 4")
        if not 1 < self.overhead <= 1.25:
            raise ValueError("Overhead must be between 1.000 and 1.250")
        if not all([self.reps, self.std_work_conc, self.well_sample_vol,
                    self.well_dnasol_vol, self.well_pico_vol, self.PicoBatchList, self.overhead]):
            raise ValueError("Required parameters are missing")
        if any(math.isnan(i) for i in self.PicoBatchList):
            raise ValueError("PicoBatch list contains invalid input")
        if any(i <= 0 for i in
               [self.std_work_conc, self.well_sample_vol,
                self.well_dnasol_vol, self.well_pico_vol]):
            raise ValueError("Parameters cannot be negative or zero")
        if any(i < 0 for i in self.std_conc):
            raise ValueError("Standards cannot be negative")
        if self.well_pico_vol + self.well_dnasol_vol > 250:
            raise ValueError("Volume of Diluted Sample and Pico Working Reagent should be less than 250ul combined")
        if not self.iscsv():
            raise ValueError("CSV Path is Invalid")

    def accept(self):
        try:
            self.check_values()
        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))
            return
        super(MainInputBox, self).accept()

    def getValues(self):
        return self.reps, self.std_work_conc, self.std_conc, self.well_sample_vol, self.well_dnasol_vol, self.well_pico_vol, self.overhead, self.PicoBatchList, self.path.text(), self.num_std_array, self.DNALabware, self.PicoLabware, self.mailID.text()


def readCSV():
    global width, length, reps, rep_start, std_work_conc, std_conc, well_sample_vol, well_dnasol_vol, well_pico_vol, overhead, file_path, num_std_array, DNALabware, PicoLabware, dataframe, PicoBatchList_str, PicoBatchList, std_dna_vol, std_TE_vol, rep_sets, std_work_vol, dilution_buffer_vol, reagent_vol, num_tips20, num_pico_plates, deck_tips20, deck_picoPlates, deck_samplePlates, DNAPlates, DNAWells, outputdir, deck, mailID
    try:
        dataframe = pandas.read_csv(file_path)
        if not all(i in dataframe.columns.tolist() for i in list(('DNAWell', 'DNAPlate', 'PicoBatch', 'SampleID'))):
            raise Exception("Required Datafields missing in CSV")
        PicoBatchList = list(dataframe['PicoBatch'].unique()) if PicoBatchList == [float('Inf')] else PicoBatchList
        PicoBatchList_str = ",".join(map(str, [int(i) for i in PicoBatchList if not math.isnan(i)]))
        dataframe = dataframe[dataframe['PicoBatch'].isin(PicoBatchList)]
        DNAWells = list(zip(dataframe['DNAPlate'], dataframe['DNAWell']))
        DNAPlates = list(dataframe['DNAPlate'].unique())
        duplicates = [item for item, count in Counter(DNAWells).items() if count > 1]
        if any(duplicates):
            print("Duplicates found:\n")
            print(duplicates)
            raise Exception("Resolve duplicates and retry")
        if not DNAWells:
            raise Exception("CSV is Empty")

    except Exception as error:
        print(error)
        exit()
    except:
        print("Error in parsing CSV")
        exit()
    return


# Calculate variables
def calculate():
    global width, length, reps, rep_start, std_work_conc, std_conc, well_sample_vol, well_dnasol_vol, well_pico_vol, overhead, file_path, num_std_array, DNALabware, PicoLabware, dataframe, PicoBatchList_str, PicoBatchList, std_dna_vol, std_TE_vol, rep_sets, std_work_vol, dilution_buffer_vol, reagent_vol, num_tips20, num_pico_plates, deck_tips20, deck_picoPlates, deck_samplePlates, DNAPlates, DNAWells, outputdir, deck, mailID
    rep_start = []
    length = [24, 12, 6][[384, 96, 24].index(int(PicoLabware.split('_')[1]))]
    width = [16, 8, 4][[384, 96, 24].index(int(PicoLabware.split('_')[1]))]
    for i in range(int(length / reps)):
        rep_start.extend([(x + (width * i * reps)) for x in range(width)])
    if len(std_conc):
        # All concentration are final assay volume basis
        # Volumes of working DNA standard (ul) to be added to each well
        std_dna_vol = [(c * (well_dnasol_vol + well_pico_vol) / std_work_conc) if not math.isnan(c) else 0 for c in
                       std_conc]
        # Volumes of TE buffer (ul) to be added to each standard well
        std_TE_vol = [
            (well_dnasol_vol - (c * (well_dnasol_vol + well_pico_vol) / std_work_conc)) if not math.isnan(c) else 0 for
            c in std_conc]
        if num_std_array == 1:
            rep_sets = len(DNAWells) + len(std_conc)
        elif num_std_array == 0:
            rep_sets = len(DNAWells)
        elif math.isinf(num_std_array):
            rep_sets = len(DNAWells) + (len(std_conc) * math.ceil(len(DNAWells) / (len(rep_start) - len(std_conc))))
            num_std_array = math.ceil(rep_sets / len(rep_start))
        else:
            raise ValueError
        std_work_vol = round(math.ceil(sum(std_dna_vol) * reps * num_std_array * overhead), 3)
    else:
        std_dna_vol = []
        std_TE_vol = []
        num_std_array = 0
        rep_sets = len(DNAWells)
        std_work_vol = 0
    # Calculate the amount of TE buffer needed for dilution
    dilution_buffer_vol = round(math.ceil(((len(DNAWells) * (well_dnasol_vol - well_sample_vol)) + (
            num_std_array * sum(std_TE_vol))) * reps * overhead / 200) * 0.2, 3)

    # Calculate the amount of PicoGreen working reagent needed
    reagent_vol = round(math.ceil(rep_sets * reps * well_pico_vol * overhead / 200) * 0.2, 3)


def check():
    global width, length, reps, rep_start, std_work_conc, std_conc, well_sample_vol, well_dnasol_vol, well_pico_vol, overhead, file_path, num_std_array, DNALabware, PicoLabware, dataframe, PicoBatchList_str, PicoBatchList, std_dna_vol, std_TE_vol, rep_sets, std_work_vol, dilution_buffer_vol, reagent_vol, num_tips20, num_pico_plates, deck_tips20, deck_picoPlates, deck_samplePlates, DNAPlates, DNAWells, outputdir, deck, mailID
    try:
        if any(i <= 0 for i in [dilution_buffer_vol, reagent_vol]):
            raise Exception("Error in calculated variables - Zero or less")
        if any(any(i < 0 for i in lst) for lst in [std_dna_vol, std_TE_vol, std_conc, [std_work_vol]]):
            raise Exception("Error in calculated variables - Less than zero")
        if any(std_TE_vol[i] + std_dna_vol[i] > well_dnasol_vol for i in range(len(std_conc))):
            raise Exception("DNA Standards Working and Concentrations are not compatible")
        if math.isnan(num_std_array) or math.isinf(num_std_array):
            raise Exception("Error in updating Number of Standard Arrays")
    except Exception as error:
        print(error)
        exit()
    except:
        print("Error in calculated variable check")
        exit()
    return


def decksetup():
    global width, length, reps, rep_start, std_work_conc, std_conc, well_sample_vol, well_dnasol_vol, well_pico_vol, overhead, file_path, num_std_array, DNALabware, PicoLabware, dataframe, PicoBatchList_str, PicoBatchList, std_dna_vol, std_TE_vol, rep_sets, std_work_vol, dilution_buffer_vol, reagent_vol, num_tips20, num_pico_plates, deck_tips20, deck_picoPlates, deck_samplePlates, DNAPlates, DNAWells, outputdir, deck, mailID
    num_tips20 = int(math.ceil(rep_sets / 96))
    num_pico_plates = int(math.ceil(rep_sets / len(rep_start)))
    if not 0 < num_tips20 + num_pico_plates + len(DNAPlates) <= 8:
        raise ValueError
    deck_tips20 = list(zip(range(9, 9 - num_tips20, -1), ["Tip Rack 20ul"] * num_tips20))[::-1]
    deck_picoPlates = list(zip(range(9 - num_tips20, 9 - num_tips20 - num_pico_plates, -1),
                               [f"PicoPlate{i}" for i in range(int(num_pico_plates), 0, -1)]))[::-1]
    deck_samplePlates = list(
        zip(range(9 - num_tips20 - num_pico_plates, 9 - num_tips20 - num_pico_plates - len(DNAPlates), -1),
            [samplePlate for samplePlate in DNAPlates[::-1]]))[::-1]


def writeDF():
    global width, length, reps, rep_start, std_work_conc, std_conc, well_sample_vol, well_dnasol_vol, well_pico_vol, overhead, file_path, num_std_array, DNALabware, PicoLabware, dataframe, PicoBatchList_str, PicoBatchList, std_dna_vol, std_TE_vol, rep_sets, std_work_vol, dilution_buffer_vol, reagent_vol, num_tips20, num_pico_plates, deck_tips20, deck_picoPlates, deck_samplePlates, DNAPlates, DNAWells, outputdir, deck, mailID
    currentStdArray = 0
    currentPicoPlateIndex = -1
    currentRepSet = 0
    for sample in DNAWells:
        if currentRepSet % len(rep_start) == 0:
            currentPicoPlateIndex = currentPicoPlateIndex + 1

            currentRepSet = 0
            if currentStdArray < num_std_array:
                for i, conc in enumerate(std_conc):
                    dataframe = pandas.concat([dataframe, pandas.DataFrame([{'SampleID': f"Standard-{conc}",
                                                                             'PicoPlate': str(
                                                                                 deck_picoPlates[currentPicoPlateIndex][
                                                                                     1]), 'PicoWell': str(
                            [chr(((rep_start[currentRepSet] + (8 * k))% width) + 65) + str(((rep_start[currentRepSet] + (8 * k)) // width) + 1) for k in range(reps)])}])], ignore_index=True)
                    currentRepSet = currentRepSet + 1
                currentStdArray = currentStdArray + 1
        dataframe.loc[
            (dataframe['DNAPlate'] == sample[0]) & (dataframe['DNAWell'] == sample[1]), ['PicoPlate', 'PicoWell']] = [
            str(deck_picoPlates[currentPicoPlateIndex][1]),
            str([chr(((rep_start[currentRepSet] + (8 * k))% width) + 65) + str(((rep_start[currentRepSet] + (8 * k)) // width) + 1) for k in range(reps)])]
        currentRepSet = currentRepSet + 1


    dataframe.to_csv(
        f"{outputdir}/{os.path.splitext(os.path.basename(file_path))[0]}_PicoBatch{PicoBatchList_str}.Map.csv",
        index=False)


# Displays the Instructions
def instructions():
    global width, length, reps, rep_start, std_work_conc, std_conc, well_sample_vol, well_dnasol_vol, well_pico_vol, overhead, file_path, num_std_array, DNALabware, PicoLabware, dataframe, PicoBatchList_str, PicoBatchList, std_dna_vol, std_TE_vol, rep_sets, std_work_vol, dilution_buffer_vol, reagent_vol, num_tips20, num_pico_plates, deck_tips20, deck_picoPlates, deck_samplePlates, DNAPlates, DNAWells, outputdir, deck, mailID
    try:
        deck = []
        deck.extend(["Tip Rack 300ul", "6x15ml & 4x50ml Tube Rack"])
        deck.extend([j[1] for i in [deck_tips20[::-1], deck_picoPlates[::-1], deck_samplePlates[::-1]] for j in i])
        deck.extend(["Empty" for i in range(10 - len(deck))])
        deck.extend(["24xMicrocentrifuge Tube Rack"])
        deck.reverse()
        reagents = [["Working PicoGreen Reagent", "6x15ml & 4x50ml Tube Rack", "A4", reagent_vol, "ml"],
                    ["Dilution Buffer", "6x15ml & 4x50ml Tube Rack", "B4", dilution_buffer_vol, "ml"],
                    ["DNA Standard Working", "24xMicrocentrifuge Tube Rack", "A1", std_work_vol, "ul"]]
        with open(
                f"{outputdir}/{os.path.splitext(os.path.basename(file_path))[0]}_PicoBatch{PicoBatchList_str}.OT2DeckSetup.txt",
                "w") as file:
            file.writelines(
                "Run Information:\n\tSamples: {}\n\tSample plates: {}\n\tPico Plates: {}\nParameters:\n\tReplicates: {}\n\tDNA Standards Final Concentrations: {}ug/ml\n\tNumber of Standard Arrays: {}\nVolume Information:\n\tSample per well: {}ul\n\tOverhead percentage: {}%\n\tDilution buffer: {}ml\n\tPico Working Reagent: {}ml\n\tDNA Standard Working: {}ul\n\tSample Labware: {}\n\tPico Labware: {}\n".format(
                    len(DNAWells), len(DNAPlates), num_pico_plates, reps, std_conc, num_std_array, well_sample_vol,
                    round(((overhead - 1) * 100), 3), dilution_buffer_vol, reagent_vol, std_work_vol, DNALabware, PicoLabware))
            file.writelines("Setup the deck as shown below:\n")
            for i, str in enumerate(deck):
                file.writelines(f"\tDeck {i + 1}: {str}\n")
            file.writelines(
                f"Reagent preperation steps for quantification using the Quant-iT™ PicoGreen™ reagent/kit (P11496, P7589, P11495, P7581):\n")
            file.writelines(
                f"1. Prepare {dilution_buffer_vol + reagent_vol}ml of working TE buffer by diluting {(dilution_buffer_vol + reagent_vol) * 1000 / 20}ul of 20X TE buffer provided.\n"
                f"2. Add {reagent_vol * 1000 / 200}ul of 200X PicoGreen reagent to a new tube, and transfer {reagent_vol * 0.995}ml of the previously prepared buffer.\n"
                f"3. Add {std_work_vol / 50}ul of 100ug/ml DNA Standard Solution to a new microcentrifuge tube, and add {std_work_vol * 0.98}ul of Nuclease Free Water to it to make the 2ug/ml Working DNA Standard solution.")

            file.writelines(
                f"Place the reagents in the following positions:\n")
            for i, element in enumerate(reagents):
                file.writelines(
                    f"\t{i + 1}. {element[0]}: Position {element[2]} of {element[1]} with atleast {element[3]}{element[4]} reagent in it\n")
    except Exception as error:
        print(error)
        exit()
    return


def writeOT():
    global width, length, reps, rep_start, std_work_conc, std_conc, well_sample_vol, well_dnasol_vol, well_pico_vol, overhead, file_path, num_std_array, DNALabware, PicoLabware, dataframe, PicoBatchList_str, PicoBatchList, std_dna_vol, std_TE_vol, rep_sets, std_work_vol, dilution_buffer_vol, reagent_vol, num_tips20, num_pico_plates, deck_tips20, deck_picoPlates, deck_samplePlates, DNAPlates, DNAWells, outputdir, deck, mailID
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "dependencies\OT2PicoRun_Template.py"),
              "r") as template:
        contents = template.readlines()
        for num, line in enumerate(contents, 1):
            if "# Metadata" in line:
                break
        contents.insert(num,
                        f"metadata = {{\n    'protocolName': 'PicoPlate-{os.path.splitext(os.path.basename(file_path))[0]}_PicoBatch{PicoBatchList_str}',\n    'author': 'Generated by PrePico; CC: Arval Viji Elango',\n    'apiLevel': '2.13'\n}}")
        for num, line in enumerate(contents, 1):
            if "# Variables" in line:
                break
        contents.insert(num, f"    deck_samplePlates = {deck_samplePlates}\n")
        contents.insert(num, f"    deck_picoPlates = {deck_picoPlates}\n")
        contents.insert(num, f"    DNAWells = {DNAWells}\n")
        contents.insert(num, f"    std_dna_vol = {std_dna_vol}\n")
        contents.insert(num, f"    std_TE_vol = {std_TE_vol}\n")
        contents.insert(num, f"    well_sample_vol = {well_sample_vol}\n")
        contents.insert(num, f"    well_pico_vol = {well_pico_vol}\n")
        contents.insert(num, f"    well_TE_vol = {well_dnasol_vol - well_sample_vol}\n")
        contents.insert(num, f"    num_std_array = {num_std_array}\n")
        contents.insert(num, f"    reps = {reps}\n")
        contents.insert(num, f"    PicoPlateType = {int(PicoLabware.split('_')[1])}\n")
        if len(mailID) == 0:
            contents.insert(num, f"    emailID = \"{mailID}\"\n")
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
        for j, layout in enumerate((deck_picoPlates)):
            if j > 0:
                stringList += ", "
            stringList += f"protocol.load_labware('{PicoLabware}', {layout[0]})"
        contents.insert(num, f"    picoPlates=[{stringList}]\n")
        stringList = ""
        for j, layout in enumerate((deck_tips20)):
            if j > 0:
                stringList += ", "
            stringList += f"protocol.load_labware('opentrons_96_tiprack_20ul', {layout[0]})"
        contents.insert(num, f"    tips20=[{stringList}]\n")

        with open(
                f"{outputdir}/PicoPlating_{os.path.splitext(os.path.basename(file_path))[0]}_PicoBatch{PicoBatchList_str}.OT2Run.py",
                "w") as file:
            file.seek(0)
            file.writelines(contents)
            file.close()
        template.close()
    return


if __name__ == '__main__':
    global width, length, reps, rep_start, std_work_conc, std_conc, well_sample_vol, well_dnasol_vol, well_pico_vol, overhead, file_path, num_std_array, DNALabware, PicoLabware, dataframe, PicoBatchList_str, PicoBatchList, std_dna_vol, std_TE_vol, rep_sets, std_work_vol, dilution_buffer_vol, reagent_vol, num_tips20, num_pico_plates, deck_tips20, deck_picoPlates, deck_samplePlates, DNAPlates, DNAWells, outputdir, deck, mailID
    app = QApplication([])
    mainDialog = MainInputBox()
    if mainDialog.exec_():
        reps, std_work_conc, std_conc, well_sample_vol, well_dnasol_vol, well_pico_vol, overhead, PicoBatchList, file_path, num_std_array, DNALabware, PicoLabware, mailID = mainDialog.getValues()

    outputdir = f"{os.path.split(file_path)[0]}/PicoPrepOutput"
    if not os.path.exists(outputdir):
        os.makedirs(outputdir)

    readCSV()
    calculate()
    check()
    decksetup()
    writeDF()
    instructions()
    writeOT()
    print("Successfully generated outputs")
