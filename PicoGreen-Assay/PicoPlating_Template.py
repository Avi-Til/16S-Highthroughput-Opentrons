from itertools import chain
from opentrons import protocol_api

metadata = {
    'protocolName': 'PicoPlating',
    'author': 'Arval Viji Elango',
    'description': '01.25.2023',
    'apiLevel': '2.13'
}


def run(protocol: protocol_api.ProtocolContext):
    # Inserted variables

    # Labware
    tips300 = [protocol.load_labware('opentrons_96_tiprack_300ul', 1)]
    tips20 = [protocol.load_labware('opentrons_96_tiprack_20ul', 11),
              protocol.load_labware('opentrons_96_tiprack_20ul', 10),
              protocol.load_labware('opentrons_96_tiprack_20ul', 3)]
    tube_rack = protocol.load_labware('opentrons_10_tuberack_nest_4x50ml_6x15ml_conical', 4)
    microtube_rack = protocol.load_labware('opentrons_24_tuberack_eppendorf_2ml_safelock_snapcap', 2)
    well_plates = [protocol.load_labware('eppendorf96wellpcrplatetwin.tecskirted_96_wellplate_150ul', 5),
                   protocol.load_labware('eppendorf96wellpcrplatetwin.tecskirted_96_wellplate_150ul', 6),
                   protocol.load_labware('eppendorf96wellpcrplatetwin.tecskirted_96_wellplate_150ul', 7),
                   protocol.load_labware('eppendorf96wellpcrplatetwin.tecskirted_96_wellplate_150ul', 8),
                   protocol.load_labware('eppendorf96wellpcrplatetwin.tecskirted_96_wellplate_150ul', 9)]
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
            p20.distribute(TE_well_vol20, dilution_buffer, [plate.wells()[well] for well in TE_well_list20],
                           disposal_volume=0)
        if TE_well_list300:
            p300.distribute(TE_well_vol300, dilution_buffer, [plate.wells()[well] for well in TE_well_list300],
                            disposal_volume=0)
        if std_well_list20:
            p20.transfer(std_well_vol20, dna_std_work, [plate.wells()[well] for well in std_well_list20],
                         new_tip='always')
        if std_well_list300:
            p300.transfer(std_well_vol300, dna_std_work, [plate.wells()[well] for well in std_well_list300],
                          new_tip='always')
        return

    # Function to distribute DNA extract solutions
    def make_plates():
        p300.distribute(well_TE_vol, dilution_buffer,
                        list(chain.from_iterable(
                            [(well_plates[source[2]].wells()[well] for well in source[3]) for source in
                             source_list])), disposal_volume=0)
        for plate in pico_plates:
            make_standards(well_plates[plate])
            sublist = []
            for source in source_list:
                if source[2] == plate:
                    sublist.append(source)
                    p20.transfer(well_sample_vol, well_plates[source[0]][source[1]],
                                 [well_plates[source[2]].wells()[well] for well in source[3]], new_tip='always')
            if pico_every_plate:
                distribute_pico([plate], sublist)
                protocol.pause("Plate is done, hit resume to continue.")
        if not pico_every_plate:
            distribute_pico(pico_plates, source_list)
        return

    def distribute_pico(plate_list, well_list):
        p300.pick_up_tip()
        for plate in plate_list:
            p300.distribute(well_pico_vol, pico_working,
                            list(chain.from_iterable(
                                [(well_plates[plate].wells()[well].top(1) for well in source[3]) for source in
                                 well_list])),
                            touch_tip='true',
                            new_tip='never', disposal_volume=0)
            p300.distribute(well_pico_vol, pico_working,
                            [well_plates[plate].wells()[well].top(1) for well in
                             list(set().union(TE_well_list20, std_well_list20, TE_well_list300, std_well_list300))],
                            touch_tip='true',
                            new_tip='never', disposal_volume=0)
        p300.drop_tip()
        return

    # Make Working Solutions
    if not skip_pico_prep:
        p300.transfer(pico_stock_vol + extra_buffer, pico_working, trash)
        p300.transfer(pico_stock_vol, pico_stock, pico_working, mix_after=(3, 300))
    if not skip_std_prep:
        p300.transfer(std_nfw_vol, nfwater, dna_std_work)
        p20.transfer(std_stock_vol, dna_std_stock, dna_std_work, mix_after=(3, 20))

    # Distribute the samples
    make_plates()
    return
