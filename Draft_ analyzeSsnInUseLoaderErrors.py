import csv
import os
import os.path, time
from datetime import date
from datetime import datetime

def fileReportingReview():

    # Set File Paths
    notImportedFilesLocation = 'c:/Users/tape/Documents/Python/DummyData' # TESTING LOCATION
    reportOutputLocation = 'c:/Users/tape/Documents/Python/ReportOutput' # TESTING LOCATION

    # Set Search Parameters
    # fileNameExclusionList = ('fix','AnalystChange')
    earliestFileCreationDateToReview = '2019-03-29'

    # Set directory to File Paths
    os.chdir(notImportedFilesLocation)

    print(os.getcwd()) # DEBUG

    # Initialize Variables
    dateOfFileCreation = ''
    countOfRecordsWithError = 0
    countOfParticipantsWithError = 0
    countOfTotalRecords = 0
    dataSetByDate = [['File Date','Total Loader Errors','Count of Errors by Record','Count Of Errors by Participant']] # [dateOfFileCreation,countOfTotalRecords,countOfRecordsWithError,countOfParticipantsWithError]
    fileDataSaved = False



    # Loop Through Loader Error Files in Directory
    for loaderFile in os.listdir():
        
        # Get File Creation Date
        dateOfFileCreation = str(datetime.fromtimestamp(os.path.getctime(loaderFile)))[:10]

        # Don't Review Certain Date Ranges
        if dateOfFileCreation < earliestFileCreationDateToReview:
            continue

        # Don't Review Certain Files with Naming Conventions
        if "fix" in loaderFile:
            continue

        print(dateOfFileCreation) # DEBUG

        # Open and Read File
        with open(loaderFile, 'r', newline='') as csv_file:
            csv_reader= csv.reader(csv_file)

            print(loaderFile) # DEBUG

            # Loop Through Each Row on the File
            for line in csv_reader:
                countOfTotalRecords += 1
                
                # Review Row: get length, check last field for error message
                col = len(line) - 1
                # "SsnAlreadyInUseInSystem:socialSecurityNumber;SsnAlreadyInUseInSystem:dependentSocialSecurityNumber"

                if "SsnAlreadyInUseInSystem:socialSecurityNumber" in line[col]:
                    countOfRecordsWithError += 1
                    countOfParticipantsWithError += 1

                # “SsnAlreadyInUseInSystem:dependentSocialSecurityNumber”

            # Save Data Points Collected from File Reviewed
            datesOfData = len(dataSetByDate)
            print(datesOfData)
            if len(dataSetByDate) == 1:
                dataSetByDate.insert(len(dataSetByDate),[dateOfFileCreation,countOfTotalRecords,countOfRecordsWithError,countOfParticipantsWithError])
                print(dataSetByDate)
            else:
                for dates in range(1,datesOfData):
                    print(dataSetByDate[dates][0])

                    # Add to Total if File Creation Date Exists
                    if dataSetByDate[dates][0] == dateOfFileCreation:
                        dataSetByDate[dates][1] = dataSetByDate[dates][1] + countOfTotalRecords
                        dataSetByDate[dates][2] = dataSetByDate[dates][2] + countOfRecordsWithError
                        dataSetByDate[dates][3] = dataSetByDate[dates][3] + countOfParticipantsWithError
                        print(dataSetByDate)
                        fileDataSaved = True
                
                # Track New File Creation Date
                if fileDataSaved == False:
                        dataSetByDate.insert(len(dataSetByDate),[dateOfFileCreation,countOfTotalRecords,countOfRecordsWithError,countOfParticipantsWithError])  
        
            # Reset the Counting Variables for Next Loop
            countOfRecordsWithError = 0
            countOfParticipantsWithError = 0
            countOfTotalRecords = 0
            fileDataSaved = False
            

    
    print("Results:")

    # Move to Directory to Report Output Location
    os.chdir(reportOutputLocation)

    # Output CSV File with Results
    reportDate = str(date.today())
    reportOutputFilePathName = reportOutputLocation + "/SsnInUseReviewReport_" + str(reportDate) + ".csv"

    # ADD - Check if report name exists, don't replace

    # [dateOfFileCreation,countOfTotalRecords,countOfRecordsWithError,countOfParticipantsWithError]

    # Open File to Write
    with open(reportOutputFilePathName, 'w', newline='') as reportFile:
        thewriter = csv.writer(reportFile)

        # Loop Through Results List to Write to CSV
        for dateSet in range(0,len(dataSetByDate)):
            thewriter.writerow(dataSetByDate[dateSet])
            print(dataSetByDate[dateSet])


def main():
    fileReportingReview

main()