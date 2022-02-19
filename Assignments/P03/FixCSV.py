import csv

ufo = []

with open('ufo_data.csv') as f:
    csvfile = csv.DictReader(f, delimiter = ',')

    for row in csvfile:
        #loads csv dictionary into an array
        ufo.append(row)

with open('BetterUFOData.csv', 'w') as f:
    #all canadian states
    canadaStates = ['ON', 'QC', 'NS', 'NB', 'MB', 'BC', 'PE', 'SK', 'AB', 'NL']

    csvwriter = csv.writer(f,  delimiter=",", lineterminator = '\n') 

    csvwriter.writerow(list(ufo[0].keys()))

    for row in ufo:
        if row['state'] not in canadaStates:
            #makes sure no Canadian ones are pushed in the csv
            csvwriter.writerow(list(row.values()))