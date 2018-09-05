import csv
import codecs
import io

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
        complaint_file.write(csvData + '\n')
        
    complaint_file.close()

def csvComplaintDelete():
    complaintFilename = 'complaints/complaints.csv'

    with open(complaintFilename, 'w') as complaint_file:
        complaint_file.write('')

    complaint_file.close()