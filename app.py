from flask import Flask, url_for, redirect, render_template
import pandas as pd
import dataSource

app = Flask(__name__)
app.secret_key = 'somesecretkey'

@app.route("/")
def hello_world():
    return redirect(url_for('charts'))


@app.route('/charts', methods=['GET', 'POST'])
def charts():  

    try:
        df = pd.read_csv('CSVfile.csv',sep=",")

        if(dataSource.sevenDaysCheck(df['weekEndingDate'][df.index[-1]])):                    #Funcao que confere ultimo update + 7 dias
            print('Updating CSV file!')
            dataSource.newCSVfile()

    except IOError:
        print("File not accessible")
        dataSource.newCSVfile()
        df = pd.read_csv('CSVfile.csv',sep=",")

    Xaxis = df.loc[:,'weekEndingDate']
    Xaxis=Xaxis.drop_duplicates().str[0:10]

    ChinaDF = df[df['countryCode'] == 5700]
    MexDF = df[df['countryCode'] == 2010]

    ChinaDF = ChinaDF[["weekEndingDate", "weeklyExports"]]
    ChinaDF['weekEndingDate'] = ChinaDF['weekEndingDate'].str[0:10]
    ChinaDF = ChinaDF.rename(columns={'weekEndingDate': 'x', 'weeklyExports': 'y'}) 

    MexDF = MexDF[["weekEndingDate", "weeklyExports"]]
    MexDF['weekEndingDate'] = MexDF['weekEndingDate'].str[0:10]
    MexDF = MexDF.rename(columns={'weekEndingDate': 'x', 'weeklyExports': 'y'}) 
    
    ChinaDF=ChinaDF.to_dict('records')    
    MexDF=MexDF.to_dict('records')       
    
    return render_template("charts.html",labels=list(Xaxis),set1=list(ChinaDF),set2=list(MexDF))

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port="80")