from flask import Flask, flash, render_template, request, redirect
import requests
import json
import csv
import mysql.connector


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
            return render_template('createPlan.html', biz_json = business_data['businesses'] )
        
        elif  'plan_name' in request.form:
            plan_name = request.form["plan_name"]
            crsr.reset()
            crsr.execute("select name from Plans;")
            result = crsr.fetchall()
            conn.commit()
            list_of_plan_names=[]
            for row in result:
                list_of_plan_names.append(row['name'])
            print(list_of_plan_names)
            if plan_name in list_of_plan_names:
                return render_template('index.html', err= "Plan Already exists")
            query = f"insert into Plans (name) values ('{plan_name}');"
            crsr.execute(query)
            conn.commit()
            return render_template('index.html', err= f"{plan_name} is created")
        
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
