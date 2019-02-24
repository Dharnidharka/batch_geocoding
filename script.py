# importing csv module
import csv
import requests
import time

GOOGLE_MAPS_API_URL = 'https://maps.googleapis.com/maps/api/geocode/json?key=<YOUR API KEY>'

infile = "input1.csv"
outfile = "output1.csv"
rows = []

# reading csv file
with open(infile, 'r') as csvfile:
    # creating a csv reader object
    csvreader = csv.reader(csvfile)

    # extracting each data row one by one
    for row in csvreader:
        rows.append(row)

    # get total number of rows
    print("Total no. of rows: %d"%(csvreader.line_num))

for row in rows:
    address = row[2] + ', ' + row[0]
    print("Processing: " + address)

    params = {
                'address': address,
                'sensor': 'false',
                'region': 'India'
            }

    # Do the request and get the response data
    req = requests.get(GOOGLE_MAPS_API_URL, params=params)
    res = req.json()

    # Use the first result
    if(len(res['results']) > 0):

        result = res['results'][0]

        geodata = dict()
        geodata['lat'] = result['geometry']['location']['lat']
        geodata['lng'] = result['geometry']['location']['lng']

        # check if the coordinates were found
        if(geodata['lat'] is not None and geodata['lng'] is not None):
            row.append(geodata['lat'])
            row.append(geodata['lng'])

    else:
        print("Some problems with finding the coordinates. ", res);

    time.sleep(3)


with open(outfile, 'w') as writeFile:
    writer = csv.writer(writeFile)
    writer.writerows(rows)

csvfile.close()
writeFile.close()
