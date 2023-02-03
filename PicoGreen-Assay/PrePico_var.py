import math
import PrePico_fun as fun

# Declare global variables
global num_wells_plate, overhead, TE_stock_conc, pico_stock_conc, reps, std_stock_conc, std_work_conc, std_conc, well_sample_vol, well_dnasol_vol, well_pico_vol, file_path, unique_plate, unique_plate_well_pairs, source_map, source_list, std_dna_vol, std_TE_vol, std_stock_vol, std_nfw_vol, num_quant_wells, num_pico_plates, num_std_wells, dilution_buffer_vol, reagent_buffer_vol, pico_stock_vol, reagent_stock_vol, dilution_stock_vol, TE_well_list20, TE_well_vol20, TE_well_list300, TE_well_vol300, std_well_list20, std_well_vol20, std_well_list300, std_well_vol300, source_plates, pico_plates, extra_buffer, skip_pico_prep, skip_std_prep, pico_every_plate


# Initialized variables
def init():
    global num_wells_plate, overhead, TE_stock_conc, pico_stock_conc, reps, std_stock_conc, std_work_conc, std_conc, well_sample_vol, well_dnasol_vol, well_pico_vol, file_path, unique_plate, unique_plate_well_pairs, source_map, source_list, skip_pico_prep, skip_std_prep, pico_every_plate

    skip_pico_prep = False
    skip_std_prep = False
    pico_every_plate = True

    # Number of wells in plate
    # DO NOT CHANGE. Variable provisioned for future versions of 384 well plate.
    num_wells_plate = 96

    # Overhead to be used for all volume calculations
    overhead = 1.04

    # Strength of stock TE buffer (xTimes)
    TE_stock_conc = 20

    # Strength of stock PicoGreen Reagent (xTimes)
    pico_stock_conc = 200

    # Number of replicates for each sample
    # Choose one of the following: 1, 2, 3, 4
    reps = 2

    # Concentration of stock DNA standard (ug/ml)
    std_stock_conc = 100

    # Concentration of working DNA standard (ug/ml)
    std_work_conc = 2

    # Concentration of DNA standards (ug/ml) in the PicoPlate after adding PicoGreen working reagent
    # Negative values are treated as empty, while 0 are treated as blanks
    std_conc = [0.75, 0.50, 0.25, 0.10, 0.05, 0.01, 0, -1]

    # Volume of sample (ul) to be added in each well
    well_sample_vol = 2

    # Volume of final DNA Solution (ul) in each well after adding TE buffer
    well_dnasol_vol = 100

    # Volume of PicoGreen working reagent to be added to the DNA Solution in each well
    well_pico_vol = 100

    # Ask for user input to CSV file path
    file_path = input("Enter the CSV file path: ")

    # Intitialize those variables that will be self-referenced
    unique_plate = []
    unique_plate_well_pairs = []
    source_map = []
    source_list = []


# Calculated variables
def calculate():
    global num_wells_plate, overhead, TE_stock_conc, pico_stock_conc, reps, std_stock_conc, std_work_conc, std_conc, well_sample_vol, well_dnasol_vol, well_pico_vol, std_dna_vol, std_TE_vol, std_stock_vol, std_nfw_vol, num_quant_wells, num_pico_plates, num_std_wells, dilution_buffer_vol, reagent_buffer_vol, pico_stock_vol, reagent_stock_vol, dilution_stock_vol, TE_well_list20, TE_well_vol20, TE_well_list300, TE_well_vol300, std_well_list20, std_well_vol20, std_well_list300, std_well_vol300, extra_buffer

    # Volumes of working DNA standard (ul) to be added to each well
    std_dna_vol = [(c * (well_dnasol_vol + well_pico_vol) / std_work_conc) if c >= 0 else 0 for c in std_conc]
    # std_dna_vol = [c * (well_dnasol_vol) / std_work_conc for c in std_conc]

    # Volumes of TE buffer (ul) to be added to each standard well
    std_TE_vol = [(well_dnasol_vol - (c * (well_dnasol_vol + well_pico_vol) / std_work_conc)) if c >= 0 else 0 for c in
                  std_conc]

    # Volume of stock DNA standard (ul) to be diluted to create the working standard
    # Rounded to the nearest 0.1ul after multiplying for replicates and adding overhead
    std_stock_vol = round((overhead * reps * sum(std_dna_vol) * std_work_conc / std_stock_conc), 1)

    # Amount of water to add to stock DNA standard to make working
    std_nfw_vol = std_stock_vol * ((std_stock_conc / std_work_conc) - 1)

    # Calculate the number of PicoGreen quantification wells
    num_quant_wells = reps * len(unique_plate_well_pairs)

    # Calculate the number of reaction plates
    num_pico_plates = math.ceil((num_quant_wells + (len(std_conc) * reps)) / num_wells_plate)

    # Calculate the number of DNA standard wells
    num_std_wells = num_pico_plates * len(std_conc) * reps

    # Calculate the amount of TE buffer needed for dilution after adding overhead and rounded to the nearest 1mL
    dilution_buffer_vol = math.ceil(
        ((num_quant_wells * (well_dnasol_vol - well_sample_vol)) + sum(std_TE_vol)) * overhead / 1000)

    # Calculate the amount of TE buffer needed for PicoGreen working reagent preparation after adding overhead and rounded to the
    reagent_buffer_vol = (num_std_wells + num_quant_wells) * well_pico_vol * overhead

    # Rounds reagents stock volumes and recalculates the working volumes for the rounded stocks
    pico_stock_vol = round(reagent_buffer_vol / pico_stock_conc, 1)
    reagent_buffer_vol = pico_stock_vol * pico_stock_conc
    extra_buffer = (math.ceil(reagent_buffer_vol / 1000) * 1000) - reagent_buffer_vol
    reagent_buffer_vol = round((reagent_buffer_vol + extra_buffer) / 1000)
    reagent_stock_vol = reagent_buffer_vol / TE_stock_conc
    dilution_stock_vol = dilution_buffer_vol / TE_stock_conc

    # Calculates the optimal pipetting for DNA standards
    [TE_well_list20, TE_well_vol20, TE_well_list300, TE_well_vol300] = fun.create_list(std_TE_vol)
    [std_well_list20, std_well_vol20, std_well_list300, std_well_vol300] = fun.create_list(std_dna_vol)

    myvars = globals()
    for buff in ["std", "TE"]:
        for vol in ["20", "300"]:
            removeindex = []
            for index, element in reversed(list(enumerate(myvars[f"{buff}_well_vol{vol}"]))):
                if element == 0:
                    myvars[f"{buff}_well_vol{vol}"].pop(index)
                    myvars[f"{buff}_well_list{vol}"].pop(index)
    return
