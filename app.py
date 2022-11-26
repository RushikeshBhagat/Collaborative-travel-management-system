from flask import Flask, flash, render_template, request, redirect, session
#from flask_session import Session
import requests
import json
import mysql.connector
import csv
import yaml


API_KEY = '2mV1iX6Fd8Fx87j_3PDsUz5p9JjNDRfvZRqoijC4wbzF_QeXe9xReZ8TMmSjp22CQtF_WCRyzt08KHKla30wMFVOSnPqTkakoVO0_tf2oH_BCyW_FQgNgKjyoTA3Y3Yx'
SEARCH_PATH = "https://api.yelp.com/v3/businesses/search"
HEADERS = {'Authorization': 'bearer %s' % API_KEY}



# crsr.execute("select * from Persons;")
# print(crsr.fetchall())
app = Flask(__name__)

def db_call(plan_data):
    conn = mysql.connector.connect(user="root", password="e~oJ^vNcTm5^.2BD", host="34.28.144.64", database="cloud-computing-db")
    crsr = conn.cursor(dictionary=True)
    new_data = yaml.safe_load(plan_data['msg'])
    #print(new_data['location']['display_address'])
    query = f"INSERT into Places (plan_id, bizid, bizname, bizurl, price, ratings, address, phone, imgurl) values ({new_data['plan_id']}, '{new_data['id']}','{new_data['name']}','{new_data['url']}','{new_data['price']}',{new_data['rating']},'{new_data['location']['display_address'][0]}, {new_data['location']['display_address'][1]}','{new_data['display_phone']}','{new_data['image_url']}');"
    print(query)
    crsr.execute(query)
    conn.commit()
    #print(new_data)
    


@app.route("/", methods=['GET','POST'])

def index():

    return render_template('index.html')

@app.route("/addTODB", methods=['GET','POST'])
def addTODB():
    if request.method == 'POST':
        data = request.json
        db_call(data)
        return data['msg']


@app.route("/createPlan", methods=['GET','POST'])
def createPlan():
    conn = mysql.connector.connect(user="root", password="e~oJ^vNcTm5^.2BD", host="34.28.144.64", database="cloud-computing-db")
    crsr = conn.cursor(dictionary=True)
    
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
            crsr.execute("select * from Plans;")
            result1=crsr.fetchall()
            conn.commit()
            selectValue = request.form.get('jobid')
            #print(selectValue)
            return render_template('createPlan.html', biz_json = business_data['businesses'],result1=result1)


        elif 'addTODB' in request.form:
            id = request.form['addTODB']
            print(id)
        
    return render_template('createPlan.html')
    


if __name__ == '__main__':
    app.run(debug=True)
