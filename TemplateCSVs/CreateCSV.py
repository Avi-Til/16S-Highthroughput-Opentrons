import csv

num_rows = int(input("Enter the number of samples: "))

#initialize variables
sample_count = 0
plate_count = 0
well_count = 0

with open('output.csv', mode='w') as csv_file:
    fieldnames = ['PlateID', 'SampleID', 'WellID']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()
    for i in range(num_rows):
        #increment sample count
        sample_count += 1
        #create SampleID
        sample_id = "Sample" + hex(sample_count)[2:]
        #create PlateID
        if i % 96 == 0:
            plate_count += 1
        plate_id = "Plate" + hex(plate_count)[2:]
        #create WellID
        well_id = chr(ord('A') + (well_count) % 8) + str((well_count) // 8 % 12 +1)
        well_count += 1
        writer.writerow({'PlateID': plate_id, 'SampleID': sample_id, 'WellID': well_id})

print("CSV created successfully!")
