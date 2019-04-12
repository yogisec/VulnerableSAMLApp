import csv
import codecs
import io
import random
import json
import time

def csvComplaintReader():
    complaintFilename = 'complaints/complaints.csv'

    with io.open(complaintFilename, 'r', encoding='utf-8-sig') as complaint_file:
        csv_reader = csv.reader(complaint_file, delimiter=',')
        complaintValues = list(csv_reader)

    complaint_file.close()
    return complaintValues

def csvComplaintWriter(csvData):
    complaintFilename = 'complaints/complaints.csv'

    print(str(csvData))
    with open(complaintFilename, 'a') as complaint_file:
        #csv_writer = csv.writer(complaint_file)
        complaint_file.write(str(random.randint(1,2000)) + ',' + csvData + '\n')
        
    complaint_file.close()

def csvComplaintDelete():
    complaintFilename = 'complaints/complaints.csv'

    with open(complaintFilename, 'w') as complaint_file:
        complaint_file.write('')

    complaint_file.close()

def SingleCSVComplaintDelete(complaintID):
    complaintFilename = 'complaints/complaints.csv'

    with open(complaintFilename, 'w') as f:
        writer = csv.writer(f)
        for row in csv.reader(f):
            if row[0] == complaintID:
                writer.writerow('')

#### Porting from CSV to JSON for greater flexibility.....glen might have been right, this one time
def jsonComplaintReader():
    complaintFilename = 'complaints/complaints.json'
    with open(complaintFilename,'r') as complaint_file:
        data = json.load(complaint_file)
        return data

def jsonComplaintWriter(newComplaint):
    complaintFilename = 'complaints/complaints.json'

    #read in the entire file stick it into a variable
    with open(complaintFilename,'r') as complaint_file:
        data = json.load(complaint_file)
    complaint_file.close()

    data.append(newComplaint)
    stringBlob = json.dumps(data)
    with open(complaintFilename, 'w') as complaint_file:
        complaint_file.write(stringBlob)

def jsonSingleComplaintDelete(complaintID):
    complaintFilename = 'complaints/complaints.json'
    
    #read in the entire file stick it into a variable
    with open(complaintFilename,'r') as complaint_file:
        data = json.load(complaint_file)
    complaint_file.close()

    for entry in data:
        if entry['id'] == complaintID:
            data.remove(entry)
    
    stringBlob = json.dumps(data)
    with open(complaintFilename, 'w') as complaint_file:
        complaint_file.write(stringBlob)