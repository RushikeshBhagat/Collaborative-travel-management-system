from flask import Flask, flash, render_template, request, redirect

import requests
import json
import pyodbc
import csv
import mysql.connector


API_KEY = '2mV1iX6Fd8Fx87j_3PDsUz5p9JjNDRfvZRqoijC4wbzF_QeXe9xReZ8TMmSjp22CQtF_WCRyzt08KHKla30wMFVOSnPqTkakoVO0_tf2oH_BCyW_FQgNgKjyoTA3Y3Yx'
SEARCH_PATH = "https://api.yelp.com/v3/businesses/search"
HEADERS = {'Authorization': 'bearer %s' % API_KEY}

conn = mysql.connector.connect(user="root", password="e~oJ^vNcTm5^.2BD", host="34.28.144.64", database="cloud-computing-db")

crsr = conn.cursor(dictionary=True)
'''crsr.execute("select * from Plans;")
print(crsr.fetchall())'''


app = Flask(__name__)

'''def cPlan(plan):
    crsr = conn.cursor()
    crsr.execute('INSERT INTO plan (planID, planName) VALUES(%s, %s)',(plan["id"], plan["name"]))
    #cursor.execute('INSERT INTO places (planID, planName) VALUES(%s, %s)',(businesses["id"], plan["name"]))
    #biz_id=crsr.execute('select places.planID from places,plan where plan.planID=')
    crsr.execute('INSERT INTO places (planID, planName) VALUES(%s, %s)',(businesses["id"], businesses["name"],
    businesses["image_url"],businesses["location"]["display_address"]))
    conn.commit()'''





@app.route("/", methods=['GET','POST'])

def index():

        #return render_template('index.html')

    return render_template('index.html')

@app.route("/createPlan", methods=['GET','POST'])
def createPlan():
    if request.method == 'POST':

        if 'city' in request.form :
            city = request.form["city"]
            term = request.form["name"]
            plan_name = request.form["plan_name"]

        #crsr = conn.cursor(dictionary=True)
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

        PARAMETERS = {'location':city,
                        'term':term,
                        'limit':10}

        response = requests.get(url=SEARCH_PATH, 
                                params=PARAMETERS, 
                                headers=HEADERS)
        
        business_data = response.json()
        businesses=business_data['businesses']
        return render_template('createPlan.html', biz_json = business_data['businesses'],curr_plan =plan_name )
        #print(business_data)
    return render_template('createPlan.html')

@app.route("/viewPlan", methods=['GET','POST'])
def viewPlan():
    crsr.reset()
    crsr.execute("select * from Plans;")
    result1=crsr.fetchall()
    
    
    #crsr.execute("INSERT into Places (plan_id, bizid, bizname, bizurl, price, ratings, address, phone, imgurl) values (24, 'ub4SJIWsZRtsowxzqYYR6t','Creative Hands','https://www.yelp.com/biz/creative-hands-arlington-2','',4.0,'2225 W Park Row Dr','(817) 695-2677','https://s3-media2.fl.yelpcdn.com/bphoto/sQF94-D7zlutaJ2hI2_P3w/o.jpg');")
    conn.commit()
    #print(result2)
    selectValue = request.form.get('jobid')
    print(selectValue)
    if request.method == 'POST':
        if 'view' in request.form : 
            
            crsr.execute("select * from Places where plan_id='"+selectValue+"';")
            result2=crsr.fetchall()
            conn.commit()
            return render_template('viewPlan.html', result1=result1, result2=result2)
    
    return render_template('viewPlan.html',result1=result1)

if __name__ == '__main__':
    app.run(debug=True)
