from flask import Flask, flash, render_template, request, redirect, session
import requests
import json

import mysql.connector
import csv
import yaml

conn = mysql.connector.connect(user="root", password="e~oJ^vNcTm5^.2BD", host="34.28.144.64", database="cloud-computing-db")
crsr = conn.cursor(dictionary=True)


# crsr.execute("select * from Persons;")
# print(crsr.fetchall())
app = Flask(__name__)


def db_call(plan_data):
    conn = mysql.connector.connect(user="root", password="e~oJ^vNcTm5^.2BD", host="34.28.144.64", database="cloud-computing-db")
    crsr = conn.cursor(dictionary=True)
    new_data = yaml.safe_load(plan_data['msg'])
    #print(new_data['location']['display_address'])
    biz_name=str(new_data['name'])
    biz_name=biz_name.replace("'","''")
    if 'price' in new_data:
        query = f"INSERT into Places (plan_id, bizid, bizname, bizurl, price, ratings, address, phone, imgurl) values ({new_data['plan_id']}, '{new_data['id']}','{biz_name}','{new_data['url']}','{new_data['price']}',{new_data['rating']},'{new_data['location']['display_address'][0]}, {new_data['location']['display_address'][1]}','{new_data['display_phone']}','{new_data['image_url']}');"
    else:
        query = f"INSERT into Places (plan_id, bizid, bizname, bizurl, price, ratings, address, phone, imgurl) values ({new_data['plan_id']}, '{new_data['id']}','{biz_name}','{new_data['url']}','NA',{new_data['rating']},'{new_data['location']['display_address'][0]}, {new_data['location']['display_address'][1]}','{new_data['display_phone']}','{new_data['image_url']}');"

    print(query)
    #print(x)
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
    selectValue = request.form.get('jobid')
    print(selectValue)
    if request.method == 'POST':
        
        if 'city' in request.form :
            term=''
            city = request.form["city"]
            if city == '':
                return render_template('index.html', err1= f"Please enter city name")
            term = request.form["name"]
          
            if term=='':
                url="https://us-central1-fresh-circle-276713.cloudfunctions.net/yelp-search/?location='"+city+"'"
            else:
                url="https://us-central1-fresh-circle-276713.cloudfunctions.net/yelp-search/?location='"+city+"'&term='"+term+"'"
            #r = requests.post(url)
            r = requests.get(url) 
            c = r.content
            result = c.decode('utf8')
            business_data = json.loads(result)
            #print(business_data)
            
            businesses=business_data['businesses']
            if 'priceBtn' in request.form :
                sort_prices_low=[]
                sort_prices_med=[]
                sort_prices_high=[]
                sort_prices_none=[]
                sort_prices=[]
                for biz in business_data['businesses']:
                    if 'price' in biz:
                        if (biz['price']=='$'):
                            sort_prices_low.append(biz)
                        elif (biz['price']=='$$'):
                            sort_prices_med.append(biz)
                        elif (biz['price']=='$$$'):
                            sort_prices_high.append(biz)
                        else:
                            sort_prices_none.append(biz)
                
                    sort_prices = sort_prices_low+sort_prices_med+sort_prices_high+sort_prices_none
                    crsr.execute("select * from Plans;")
                    result1=crsr.fetchall()
                    conn.commit()
                    
                return render_template('createPlan.html', biz_json = sort_prices,result1=result1 )
                
            crsr.execute("select * from Plans;")
            result1=crsr.fetchall()
            conn.commit()
            #print(selectValue)
            return render_template('createPlan.html', biz_json = business_data['businesses'],result1=result1)
        
        elif  'plan_name' in request.form:
            plan_name = request.form["plan_name"]
            if plan_name == '':
                return render_template('index.html', err= f"Please enter plan name")
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

@app.route("/viewPlan", methods=['GET','POST'])
def viewPlan():
    crsr.reset()
    crsr.execute("select * from Plans;")
    
    result1 = crsr.fetchall()
    #crsr.execute("INSERT into Places (plan_id, bizid, bizname, bizurl, price, ratings, address, phone, imgurl) values (32, 'ub4SJIWsZRtsowxzqYYR6t','Creative Hands','https://www.yelp.com/biz/creative-hands-arlington-2','',4.0,'2225 W Park Row Dr','(817) 695-2677','https://s3-media2.fl.yelpcdn.com/bphoto/sQF94-D7zlutaJ2hI2_P3w/o.jpg');")
    conn.commit()
    print(result1)
    selectValue = request.form.get('jobid')
    print(selectValue)
    if request.method == 'POST':
        if 'view' in request.form :

            if request.form['view']== 'rmButton':
                
                curr_element = yaml.safe_load(request.form['element_id'])
                query = f"delete from Places where plan_id={curr_element['plan_id']} and bizid='{curr_element['bizid']}';"
                print(query,"element_id")
                crsr.reset()
                crsr.execute(query)
                conn.commit()
                selectValue = str(curr_element['plan_id'])

            crsr.reset()
            crsr.execute("select * from Places where plan_id='"+selectValue+"';")
            result2=crsr.fetchall()
            conn.commit()

 
                
            
            if request.form['view']=='dlButton':
                
                crsr.execute("delete from Places where plan_id='"+selectValue+"';")
                crsr.execute("delete from Plans where id='"+selectValue+"';")
                crsr.execute("select * from Plans;")
                result1=crsr.fetchall()
                conn.commit()
                return render_template('viewPlan.html',result1=result1)
           
            #print(result1)
            for plan in result1:
                if plan['id'] == int(selectValue):
                    curr_plan_name =  plan['name']
            return render_template('viewPlan.html', result1=result1, result2=result2, curr_plan_name = curr_plan_name)
    
    return render_template('viewPlan.html',result1=result1)


if __name__ == '__main__':
    app.run(debug=True)
