import csv
from bs4 import BeautifulSoup
import requests
import xlwt


#Open the file
with open("Sec 10-k Filings.csv") as csv_file:

    #Initiate variables/readers
    csv_reader = csv.reader(csv_file, delimiter=',')
    row_counter = 0
    col_counter = 0

    #For every row
    for row in csv_reader:
        #First row does nothing
        if row_counter == 0:
            for col in range(0,len(row)):
                print(row[col] + " : " + str(col))

            row_counter +=1

        #for the rows that matter
        else:
            #Import the info that matters from the csv file
            f_fdate = row[1]
            cik = row[4]
            file_txt_link = 7
            file_htm_link = 8

            #Create url
            url = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK="\
                + str(cik) + "&type=10&dateb=" + f_fdate + "&owner=exclude&count=100"
            r = requests.get(url)
            #print(url)
            br = BeautifulSoup(r.content, "html.parser")

            #Find the document links
            for tableFile2 in br.find_all("table", {"class": "tableFile2"}):
                num = 0
                for tr in tableFile2.find_all("tr"):
                    if(num == 1):
                        for a in tr.find_all("a"):
                            new_link = a.get("href")
                            break
                    num +=1
                break

            #Assemble the new link for the scraper to go to
            new_link = "https://www.sec.gov" + new_link
            #print(new_link)
            r2 = requests.get(new_link)

            #Go to the new link
            br2 = BeautifulSoup(r2.content, "html.parser")

            #Find the first table
            for tableFile in br2.find_all("table", {"class": "tableFile"}):
                num = 0
                new10k = ""
                for tr in tableFile.find_all("tr"):

                    td = tr.find_all("td")
                    if(num == 1):
                        if "10-K" in td[1].get_text() or "10-Q" in td[3].get_text():
                            _10k = td[2].find("a").get("href")
                            if(".htm" in _10k):

                                new10k = _10k
                                new10k = "https://sec.gov" + new10k
                    num += 1
                    try:
                        if ".txt" in td[2].find("a").get("href"):
                            submission = td[2].find("a").get("href")
                        #print("txt file is: " + submission)
                    except:
                        continue
                #print("html file is: " + new10k)
                #print("txt file is: " + submission)
                print("txt file is: " + submission)
                print("html file is: " + new10k)
                with open("newfile.csv", "a") as write_file:
                    writer = csv.writer(write_file, delimiter=',')
                    writer.writerow(
                        [row[0], row[1], row[2], row[3], row[4], row[5], row[6], "https://sec.gov" + submission,
                         new10k])
                break






