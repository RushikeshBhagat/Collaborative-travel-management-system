from flask import Flask, flash, render_template, request, redirect, session
from flask_session import Session
import requests
import json
import mysql.connector
import csv


API_KEY = '2mV1iX6Fd8Fx87j_3PDsUz5p9JjNDRfvZRqoijC4wbzF_QeXe9xReZ8TMmSjp22CQtF_WCRyzt08KHKla30wMFVOSnPqTkakoVO0_tf2oH_BCyW_FQgNgKjyoTA3Y3Yx'
SEARCH_PATH = "https://api.yelp.com/v3/businesses/search"
HEADERS = {'Authorization': 'bearer %s' % API_KEY}


conn = mysql.connector.connect(user="root", password="e~oJ^vNcTm5^.2BD", host="34.28.144.64", database="cloud-computing-db")

crsr = conn.cursor(dictionary=True)

app = Flask(__name__)


@app.route("/", methods=['GET','POST'])

def index():

    return render_template('index.html')

@app.route("/createPlan", methods=['GET','POST'])
def createPlan():
    if request.method == 'POST':

        if 'city' in request.form :
            city = request.form["city"]
            term = request.form["name"]

        PARAMETERS = {'location':city,
                        'term':term,
                        'limit':10}

        response = requests.get(url=SEARCH_PATH, 
                                 params=PARAMETERS, 
                                 headers=HEADERS)
        
        business_data = response.json()
        businesses=business_data['businesses']

        return render_template('createPlan.html', biz_json = business_data['businesses'])
        #print(business_data)
    return render_template('createPlan.html')
    


if __name__ == '__main__':
    app.run(debug=True)
