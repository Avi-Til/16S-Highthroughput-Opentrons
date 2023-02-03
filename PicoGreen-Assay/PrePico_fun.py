import csv
import PrePico_var as var
import math
from itertools import chain


# Summarizes the calculated variables
def summarize():
    # Display the summary
    print("Sample Information:")
    print("\tSamples: ", len(var.unique_plate_well_pairs))
    print("\tSource plates: ", len(var.unique_plate))
    print("Quantification Information:")
    print("\tReplicates: ", var.reps)
    print("\tStandards: ", len(var.std_conc))
    print("\tPico Quantification Wells: ", var.num_quant_wells)
    print("\tPico Standard Wells: ", var.num_std_wells)
    print("\tTotal Reaction Wells: ", var.num_std_wells + var.num_quant_wells)
    print("\tPico Plates: ", var.num_pico_plates)
    print("\tDNA Sample volume: ", var.well_sample_vol)
    print("Reagents Information:")
    print("\tOverhead percentage: ", round(((var.overhead - 1) * 100), 2))
    print("\tPico Stock Reagent: ", var.pico_stock_vol, "ul")
    print("\tTE Buffer for dilution: ", var.dilution_buffer_vol, "ml")
    print("\tTE Buffer for Pico Reagent: ", var.reagent_buffer_vol, "ml")
    print("\tStock TE Buffer for dilution: ", var.dilution_stock_vol, "ml")
    print("\tStock TE Buffer for Pico Reagent Preparation: ", var.reagent_stock_vol, "ml")
    return


# Checks for duplicates in CSV
def readCSV():
    try:
        duplicate = False
        # Open the CSV file and read its contents
        with open(var.file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Check for duplicate Plate-WellID pairs
                if (row['PlateID'], row['WellID']) in var.unique_plate_well_pairs:
                    print(f"Duplicate Detected: {row['PlateID']}-{row['WellID']}")
                    duplicate = True
                else:
                    # Add the current PlateID-SampleID pair to the set of unique PlateID-SampleIDs
                    var.unique_plate_well_pairs.append([row['PlateID'], row['WellID']])
                    if (row['PlateID']) not in var.unique_plate:
                        var.unique_plate.append(row['PlateID'])
            file.close()
        if duplicate:
            raise Exception("Fix duplicates before proceeding")
    except Exception as error:
        print(error)
        exit()
    except:
        print("Error in reading CSV")
        exit()
    return


# Displays the Instructions
# If you make any changes here, you will need to make changes in the PicoPlating.py script too
def instructions():
    try:
        deck = ["Tip Rack 300ul", "24xMicrocentrifuge Tube Rack", "Tip Rack 20ul", "6x15ml & 4x50ml Tube Rack",
                platename(
                    5), platename(6), platename(7), platename(8), platename(9), "Tip Rack 20ul", "Tip Rack 20ul"]
        reagents = [["Dilution Buffer", "6x15ml & 4x50ml Tube Rack", "B4", var.dilution_buffer_vol, "ml", "atleast"],
                    ["Reagent Buffer", "6x15ml & 4x50ml Tube Rack", "A4", var.reagent_buffer_vol, "ml", "exactly"],
                    ["PicoGreen Reagent Stock", "24xMicrocentrifuge Tube Rack", "A1", var.pico_stock_vol, "ul",
                     "atleast"],
                    ["DNA Standard Working", "24xMicrocentrifuge Tube Rack", "A2", "no", "", "empty tube"],
                    ["Nuclease Free Water/Molecular Biology Grade Water", "24xMicrocentrifuge Tube Rack", "B1",
                     var.std_nfw_vol, "ul", "atleast"],
                    ["DNA Standard Stock", "24xMicrocentrifuge Tube Rack", "B2", var.std_stock_vol, "ul", "atleast"]]
        with open("Instructions.txt", "w") as file:

            file.writelines("Reagent Preparation:\n")
            file.writelines(
                f"\t1. Dilution Buffer: To a 50ml tube add {var.dilution_stock_vol}ml of {var.TE_stock_conc}x TE Stock Buffer and make up to {var.dilution_buffer_vol}ml with water.\n")
            file.writelines(
                f"\t2. Pico Reagent Buffer: To a 50ml tube add {var.reagent_stock_vol}ml of {var.TE_stock_conc}x TE Stock Buffer and make up to {var.reagent_buffer_vol}ml with water.\n")
            file.writelines("Setup the deck as shown below:\n")
            for i, str in enumerate(deck):
                file.writelines(f"\tDeck {i + 1}: {str}\n")
            file.writelines(
                f"Ensuring sufficient quantities of reagent are present, place the reagents in the following positions:\n")
            for i, element in enumerate(reagents):
                file.writelines(
                    f"\t{i + 1}. {element[0]}: Slot {element[2]} of {element[1]} with {element[5]} {element[3]}{element[4]} reagent in it\n")
    except:
        print("Error in writing instructions file")
        exit()
    return


def platename(decknum):
    try:
        return ("Extraction Plate: " +
                var.source_map[[deckindex[1] for deckindex in var.source_map].index(decknum - 5)][0])
    except ValueError:
        return ("PicoPlate" if decknum - 5 in var.pico_plates else "Empty")


# Check variables for any errors
def CSVcheck():
    try:
        if not var.unique_plate_well_pairs:
            raise Exception("CSV is Empty")
    except Exception as error:
        print(error)
        exit()
    except:
        print("Error in CSV Check")
        exit()
    return


def constcheck():
    try:
        for i in chain.from_iterable(
                [[var.num_wells_plate], [var.overhead], [var.TE_stock_conc], [var.pico_stock_conc], [var.reps],
                 [var.std_stock_conc], [var.std_work_conc], [var.well_sample_vol], [var.well_dnasol_vol],
                 [var.well_pico_vol]]):
            if i <= 0:
                raise Exception("Error in constants")
    except Exception as error:
        print(error)
        exit()
    except:
        print("Error in constant check")
        exit()
    return


def calccheck():
    try:
        for i in chain.from_iterable(
                [[var.std_stock_vol], [var.std_nfw_vol], [var.num_quant_wells], [var.num_pico_plates],
                 [var.num_std_wells],
                 [var.dilution_buffer_vol], [var.reagent_buffer_vol], [var.pico_stock_vol], [var.reagent_stock_vol],
                 [var.dilution_stock_vol]]):
            if i <= 0:
                raise Exception("Error in calculated variables - Zero or less")
        for i in chain.from_iterable(
                [var.std_dna_vol, var.std_TE_vol, var.TE_well_list20, var.TE_well_vol20, var.TE_well_list300,
                 var.TE_well_vol300, var.std_well_list20, var.std_well_vol20, var.std_well_list300,
                 var.std_well_vol300, [var.extra_buffer]]):
            if i < 0:
                raise Exception("Error in calculated variables - Less than zero")
    except Exception as error:
        print(error)
        exit()
    except:
        print("Error in calculated variable check")
        exit()
    return


# Write variables to Opentrons script
def writeOT():
    try:
        with open("PicoPlating_Template.py", "r") as template:
            contents = template.readlines()
            for num, line in enumerate(contents, 1):
                if "# Inserted variables" in line:
                    break
            contents.insert(num, f"    source_plates = {var.source_plates}\n")
            contents.insert(num, f"    pico_plates = {var.pico_plates}\n")
            contents.insert(num, f"    TE_well_vol20 = {var.TE_well_vol20}\n")
            contents.insert(num, f"    TE_well_list20 = {var.TE_well_list20}\n")
            contents.insert(num, f"    TE_well_vol300 = {var.TE_well_vol300}\n")
            contents.insert(num, f"    TE_well_list300 = {var.TE_well_list300}\n")
            contents.insert(num, f"    std_well_vol20 = {var.std_well_vol20}\n")
            contents.insert(num, f"    std_well_list20 = {var.std_well_list20}\n")
            contents.insert(num, f"    std_well_vol300 = {var.std_well_vol300}\n")
            contents.insert(num, f"    std_well_list300 = {var.std_well_list300}\n")
            contents.insert(num, f"    source_list = {var.source_list}\n")
            contents.insert(num, f"    well_sample_vol = {var.well_sample_vol}\n")
            contents.insert(num, f"    pico_stock_vol = {var.pico_stock_vol}\n")
            contents.insert(num, f"    std_stock_vol = {var.std_stock_vol}\n")
            contents.insert(num, f"    std_nfw_vol = {var.std_nfw_vol}\n")
            contents.insert(num, f"    well_pico_vol = {var.well_pico_vol}\n")
            contents.insert(num, f"    well_TE_vol = {var.well_dnasol_vol-var.well_sample_vol}\n")
            contents.insert(num, f"    extra_buffer = {var.extra_buffer}\n")
            contents.insert(num, f"    skip_pico_prep = {var.skip_pico_prep}\n")
            contents.insert(num, f"    skip_std_prep = {var.skip_std_prep}\n")
            contents.insert(num, f"    pico_every_plate = {var.pico_every_plate}\n")
            with open("PicoPlating_OT2.py", "w") as file:
                file.seek(0)
                file.writelines(contents)
                file.close()
            template.close()
    except:
        print("Error in writing OT script")
        exit()
    return


# Arrange source and pico plates optimally
# Numbers correspond to index in PicoPlating.well_plates list
def plate_setup():
    try:
        if len(var.unique_plate) == 1 and var.num_pico_plates == 1:
            var.source_plates = [3]
            var.pico_plates = [2]
        elif len(var.unique_plate) == 1 and var.num_pico_plates == 2:
            var.source_plates = [3]
            var.pico_plates = [2, 4]
        elif len(var.unique_plate) == 1 and var.num_pico_plates == 3:
            var.source_plates = [3]
            var.pico_plates = [0, 2, 4]
        elif len(var.unique_plate) == 2 and var.num_pico_plates == 1:
            var.source_plates = [2, 4]
            var.pico_plates = [3]
        elif len(var.unique_plate) == 2 and var.num_pico_plates == 2:
            var.source_plates = [1, 3]
            var.pico_plates = [0, 4]
        elif len(var.unique_plate) == 2 and var.num_pico_plates == 3:
            var.source_plates = [1, 3]
            var.pico_plates = [0, 2, 4]
        elif len(var.unique_plate) == 3 and var.num_pico_plates == 1:
            var.source_plates = [0, 2, 4]
            var.pico_plates = [3]
        elif len(var.unique_plate) == 3 and var.num_pico_plates == 2:
            var.source_plates = [0, 2, 4]
            var.pico_plates = [1, 3]
        elif len(var.unique_plate) == 4 and var.num_pico_plates == 1:
            var.source_plates = [0, 1, 2, 4]
            var.pico_plates = [3]
        elif len(var.unique_plate) == 0 or var.num_pico_plates <= 0:
            raise Exception("Number of plates error")
        else:
            raise Exception("More plates than deck can hold")
    except Exception as error:
        print(error)
        exit()
    except:
        print("Error in setting up plates")
        exit()
    for i in range(len(var.source_plates)):
        var.source_map.append([var.unique_plate[i], var.source_plates[i]])
    return


# Creates the list informing the sample location, and the replicates location
def sources():
    try:
        deck_map = 0
        counter = (var.num_wells_plate / var.reps) - (len(var.std_conc))
        plate_index = -1
        for [plateID, wellID] in var.unique_plate_well_pairs:
            for [plate, deck] in var.source_map:
                if plateID == plate:
                    deck_map = deck
                    break
            if counter == (var.num_wells_plate / var.reps) - (len(var.std_conc)):
                counter = 0
                plate_index += 1
            replicate_list = []
            for i in range(var.reps):
                replicate_list.append((math.floor(counter / 8) * 8 * var.reps) + (counter % 8) + (i * 8))
            counter += 1
            var.source_list.append([deck_map, wellID, var.pico_plates[plate_index], replicate_list])
    except:
        print("Error in creating sources list")
        exit()
    return


# For increasing speed and accuracy, this splits the list of standards into those that need P20 and ones that need P300
def create_list(volume_list):
    well_list20 = []
    well_vol20 = []
    well_list300 = []
    well_vol300 = []
    well_list20_total = []
    well_vol20_total = []
    well_list300_total = []
    well_vol300_total = []
    try:
        for i in range(len(volume_list)):
            if volume_list[i] <= 20:
                well_list20.append(i)
                well_vol20.append(volume_list[i])
            else:
                well_list300.append(i)
                well_vol300.append(volume_list[i])
        for i in range(1, var.reps + 1):
            well_list20_total.extend([(c + 8 * (12 - i)) for c in well_list20])
            well_vol20_total.extend(well_vol20)
            well_list300_total.extend([(c + 8 * (12 - i)) for c in well_list300])
            well_vol300_total.extend(well_vol300)
    except:
        print("Error in splitting standards list")
        exit()
    return [well_list20_total, well_vol20_total, well_list300_total, well_vol300_total]
