import requests
import pandas as pd
import datetime
from datetime import date, timedelta

headers_dict = {"API_KEY": "###############################"}
    


def requestData(countryCode, year):         #funcao que importa por pais e ano
    URL = "https://apps.fas.usda.gov/OpenData/api/esr/exports/commodityCode/801/countryCode/"+str(countryCode)+"/marketYear/"+str(year)
    result = requests.get(url=URL, headers=headers_dict)
    df = pd.read_json(result.text, orient='records')
    #print(df.shape[0])
    return (df)

def requestCountryHistoric(countryCode, year, currentYear):      #funcao que importa o historico de todos os anos de um pais
    dfCountry=requestData(countryCode,year)
    while(year<=currentYear):
        print(year,dfCountry.shape[0])
        year+=1
        dfYear=requestData(countryCode,year)
        dfCountry=pd.concat([dfCountry,dfYear])
    #print(dfCountry)    
    return (dfCountry)

def newCSVfile():
    print('Creating new CSV file!')
    currentYear=datetime.datetime.now().year
                                                                 #from 1998, "commodityCode": 801 (https://apps.fas.usda.gov/OpenData/api/esr/datareleasedates)
    dfChina= requestCountryHistoric(5700, 1998, currentYear)     #China country code = 5700, (https://apps.fas.usda.gov/OpenData/api/esr/countries)
    dfMex= requestCountryHistoric(2010, 1998, currentYear)       #Mexico country code = 2010, (https://apps.fas.usda.gov/OpenData/api/esr/countries)

    packToCSV = pd.concat([dfMex,dfChina])
    #print(packToCSV)
    packToCSV.to_csv('CSVfile.csv', sep=',')
        
def sevenDaysCheck(lastEndingDate):                     #Funcao que confere ultimo update + X dias
    print('LastEndingDate :',lastEndingDate)
    sum = (datetime.datetime.strptime(lastEndingDate, "%Y-%m-%dT%H:%M:%S") + timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%S")
    print('+7 days        :',sum)
    now=datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    print('Now            :',now)
    return now>sum

def main():

    try:
        df = pd.read_csv('CSVfile.csv',sep=",")

        if(sevenDaysCheck(df['weekEndingDate'][df.index[-1]])):                    #Funcao que confere ultimo update + 7 dias
            print('Updating CSV file!')
            newCSVfile()

    except IOError:
        print("File not accessible")
        newCSVfile()
        df = pd.read_csv('CSVfile.csv',sep=",")

    print()
    print(df)


main()


