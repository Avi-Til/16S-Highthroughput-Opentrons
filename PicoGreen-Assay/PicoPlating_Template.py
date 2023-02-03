from opentrons import protocol_api

metadata = {
    'protocolName': 'PicoPlating',
    'author': 'Arval Viji Elango',
    'description': '01.25.2023',
    'apiLevel': '2.13'
}


def run(protocol: protocol_api.ProtocolContext):
    # Inserted variables
    pico_every_plate = True
    skip_std_prep = False
    skip_pico_prep = False
    extra_buffer = 40.0
    well_pico_vol = 100
    std_nfw_vol = 338.1
    std_stock_vol = 6.9
    pico_stock_vol = 99.8
    well_sample_vol = 2
    source_list = [[3, 'A1', 2, [0, 8]], [3, 'B1', 2, [1, 9]], [3, 'C1', 2, [2, 10]], [3, 'D1', 2, [3, 11]], [3, 'E1', 2, [4, 12]], [3, 'F1', 2, [5, 13]], [3, 'G1', 2, [6, 14]], [3, 'H1', 2, [7, 15]], [3, 'A2', 2, [16, 24]], [3, 'B2', 2, [17, 25]], [3, 'C2', 2, [18, 26]], [3, 'D2', 2, [19, 27]], [3, 'E2', 2, [20, 28]], [3, 'F2', 2, [21, 29]], [3, 'G2', 2, [22, 30]], [3, 'H2', 2, [23, 31]], [3, 'A3', 2, [32, 40]], [3, 'B3', 2, [33, 41]], [3, 'C3', 2, [34, 42]], [3, 'D3', 2, [35, 43]], [3, 'E3', 2, [36, 44]], [3, 'F3', 2, [37, 45]], [3, 'G3', 2, [38, 46]], [3, 'H3', 2, [39, 47]], [3, 'A4', 2, [48, 56]], [3, 'B4', 2, [49, 57]], [3, 'C4', 2, [50, 58]], [3, 'D4', 2, [51, 59]], [3, 'E4', 2, [52, 60]], [3, 'F4', 2, [53, 61]], [3, 'G4', 2, [54, 62]], [3, 'H4', 2, [55, 63]], [3, 'A5', 2, [64, 72]], [3, 'B5', 2, [65, 73]], [3, 'C5', 2, [66, 74]], [3, 'D5', 2, [67, 75]], [3, 'E5', 2, [68, 76]], [3, 'F5', 2, [69, 77]], [3, 'G5', 2, [70, 78]], [3, 'H5', 2, [71, 79]], [3, 'A6', 4, [0, 8]], [3, 'B6', 4, [1, 9]], [3, 'C6', 4, [2, 10]], [3, 'D6', 4, [3, 11]], [3, 'E6', 4, [4, 12]], [3, 'F6', 4, [5, 13]], [3, 'G6', 4, [6, 14]], [3, 'H6', 4, [7, 15]], [3, 'A7', 4, [16, 24]], [3, 'B7', 4, [17, 25]], [3, 'C7', 4, [18, 26]], [3, 'D7', 4, [19, 27]], [3, 'E7', 4, [20, 28]], [3, 'F7', 4, [21, 29]], [3, 'G7', 4, [22, 30]], [3, 'H7', 4, [23, 31]], [3, 'A8', 4, [32, 40]], [3, 'B8', 4, [33, 41]], [3, 'C8', 4, [34, 42]], [3, 'D8', 4, [35, 43]], [3, 'E8', 4, [36, 44]], [3, 'F8', 4, [37, 45]], [3, 'G8', 4, [38, 46]], [3, 'H8', 4, [39, 47]], [3, 'A9', 4, [48, 56]], [3, 'B9', 4, [49, 57]], [3, 'C9', 4, [50, 58]], [3, 'D9', 4, [51, 59]], [3, 'E9', 4, [52, 60]], [3, 'F9', 4, [53, 61]], [3, 'G9', 4, [54, 62]], [3, 'H9', 4, [55, 63]], [3, 'A10', 4, [64, 72]], [3, 'B10', 4, [65, 73]], [3, 'C10', 4, [66, 74]], [3, 'D10', 4, [67, 75]], [3, 'E10', 4, [68, 76]], [3, 'F10', 4, [69, 77]], [3, 'G10', 4, [70, 78]], [3, 'H10', 4, [71, 79]]]
    std_well_list300 = [88, 89, 90, 80, 81, 82]
    std_well_vol300 = [75.0, 50.0, 25.0, 75.0, 50.0, 25.0]
    std_well_list20 = [91, 92, 93, 83, 84, 85]
    std_well_vol20 = [10.0, 5.0, 1.0, 10.0, 5.0, 1.0]
    TE_well_list300 = [88, 89, 90, 91, 92, 93, 94, 80, 81, 82, 83, 84, 85, 86]
    TE_well_vol300 = [25.0, 50.0, 75.0, 90.0, 95.0, 99.0, 100.0, 25.0, 50.0, 75.0, 90.0, 95.0, 99.0, 100.0]
    TE_well_list20 = []
    TE_well_vol20 = []
    pico_plates = [2, 4]
    source_plates = [3]

    # Labware
    tips300 = [protocol.load_labware('opentrons_96_tiprack_300ul', 1)]
    tips20 = [protocol.load_labware('opentrons_96_tiprack_20ul', 11),
              protocol.load_labware('opentrons_96_tiprack_20ul', 10),
              protocol.load_labware('opentrons_96_tiprack_20ul', 3)]
    tube_rack = protocol.load_labware('opentrons_10_tuberack_nest_4x50ml_6x15ml_conical', 4)
    microtube_rack = protocol.load_labware('opentrons_24_tuberack_eppendorf_2ml_safelock_snapcap', 2)
    well_plates = [protocol.load_labware('corning_96_wellplate_360ul_flat', 5),
                   protocol.load_labware('corning_96_wellplate_360ul_flat', 6),
                   protocol.load_labware('corning_96_wellplate_360ul_flat', 7),
                   protocol.load_labware('corning_96_wellplate_360ul_flat', 8),
                   protocol.load_labware('corning_96_wellplate_360ul_flat', 9)]
    trash = protocol.fixed_trash['A1']

    # Pipette
    p300 = protocol.load_instrument('p300_single_gen2', 'left', tip_racks=tips300)
    p20 = protocol.load_instrument('p20_single_gen2', 'right', tip_racks=tips20)

    # Reagents
    pico_working = tube_rack['A4']
    dilution_buffer = tube_rack['B4']
    pico_stock = microtube_rack['A1']
    nfwater = microtube_rack['B1']
    dna_std_stock = microtube_rack['B2']
    dna_std_work = microtube_rack['A2']

    if pico_every_plate:
        protocol.comment(
            "Pico Every Plate is set to true, robot will add PicoGreen reagent to each plate and pause after every plate. Stop program and change parameters if desired.")
    else:
        protocol.comment(
            "Pico Every Plate is set to false, robot will add PicoGreen reagent to all plates at end. Stop program and change parameters if desired.")

    # Function to make standards in PicoPlates
    def make_standards(plate):
        if TE_well_list20:
            p20.distribute(TE_well_vol20, dilution_buffer, [plate.wells()[well] for well in TE_well_list20])
        if TE_well_list300:
            p300.distribute(TE_well_vol300, dilution_buffer, [plate.wells()[well] for well in TE_well_list300])
        if std_well_list20:
            p20.transfer(std_well_vol20, dna_std_work, [plate.wells()[well] for well in std_well_list20], new_tip='always')
        if std_well_list300:
            p300.transfer(std_well_vol300, dna_std_work, [plate.wells()[well] for well in std_well_list300],
                      new_tip='always')
        return

    # Function to distribute DNA extract solutions
    def make_plates():
        for i in range(len(pico_plates)):
            make_standards(well_plates[pico_plates[i]])
            sublist = []
            for index in range(len(source_list)):
                [source_deck, source_well, dest_deck, dest_wells] = source_list[index]
                if dest_deck == pico_plates[i]:
                    sublist.append(index)
                    p20.transfer(well_sample_vol, well_plates[source_deck][source_well],
                                 [well_plates[dest_deck].wells()[well] for well in dest_wells], new_tip='always')
            if pico_every_plate:
                distribute_pico([well_plates[pico_plates[i]]], sublist)
                protocol.pause("Plate is done, hit resume to continue.")
        if not pico_every_plate:
            distribute_pico([well_plates[pico_plates[i]] for i in range(len(pico_plates))], range(len(source_list)))
        return

    def distribute_pico(plate_list, source):
        p300.pick_up_tip()
        for plate in plate_list:
            p300.distribute(well_pico_vol, pico_working,
                            [plate.wells()[well].top(1) for well in list(set().union(TE_well_list20, std_well_list20, TE_well_list300, std_well_list300))], touch_tip='true',
                            new_tip='never')
            for index in source:
                [source_deck, source_well, dest_deck, dest_wells] = source_list[index]
                if plate == well_plates[dest_deck]:
                    p300.distribute(well_pico_vol, pico_working,
                                [well_plates[dest_deck].wells()[well].top(1) for well in dest_wells], touch_tip='true',
                                new_tip='never')
        p300.drop_tip()
        return

    # Make Working Solutions
    if not skip_pico_prep
        p300.transfer(pico_stock_vol, (pico_working+extra_buffer), trash)
        p300.transfer(pico_stock_vol, pico_stock, pico_working, mix_after=(3, 300))
    if not skip_std_prep
        p300.transfer(std_nfw_vol, nfwater, dna_std_work)
        p20.transfer(std_stock_vol, dna_std_stock, dna_std_work, mix_after=(3, 20))

    # Distribute the samples
    make_plates()
    return
