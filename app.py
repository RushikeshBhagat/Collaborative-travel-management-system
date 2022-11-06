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
crsr.execute("select * from Persons;")
print(crsr.fetchall())

server = 'rushikeshbhagat.database.windows.net'
database = 'profile'
username = 'rushi'
password = 'April@5420'   
driver= '{ODBC Driver 17 for SQL Server}'

connstr = 'DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password



app = Flask(__name__)







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
        PARAMETERS = {'location':city,
                        'term':term,
                        'limit':10}

        response = requests.get(url=SEARCH_PATH, 
                                params=PARAMETERS, 
                                headers=HEADERS)
        
        business_data = response.json()
            
        #print(filters)
        return render_template('createPlan.html', biz_json = business_data['businesses'])

    return render_template('createPlan.html')
    
@app.route("/update", methods=['GET','POST'])
def update():
    if request.method == 'POST':
        if 'name' in request.form :
            name = request.form["name"]
            state = request.form["state"]
            sal = request.form["salary"]
            grade = request.form["grade"]
            room = request.form["room"]
            telnum = request.form["telnum"]
            keyw = request.form["keywords"]
            update_fields(name,state,sal,grade,room,telnum,keyw)

    return render_template("update.html")

app.config['IMAGE_TYPE'] = ['PNG', 'JPG', 'JPEG', 'GIF']
app.config['CSV_TYPE'] = ['CSV']

def csv_type(filename):
    if not '.' in filename:
        return False
    ext = filename.rsplit('.',1)[1]

    if ext.upper() in app.config['CSV_TYPE']:
        return True
    else:
        return False

def image_type(filename):
    if not '.' in filename:
        return False
    ext = filename.rsplit('.',1)[1]

    if ext.upper() in app.config['IMAGE_TYPE']:
        return True
    else:
        return False

@app.route("/upload", methods=['GET','POST'] )
def upload():
    if request.method == 'POST':
        if 'csvfile' in request.files:

            csvfile = request.files["csvfile"]

            if not csv_type(csvfile.filename):
                print('file extension not allowed')
                return render_template("upload.html")
            upload_csv(csvfile.filename)


            print("csv uploaded")

        if 'imagefile' in request.files and 'username' in request.form:
            imagefile = request.files["imagefile"]
            
            if not image_type(imagefile.filename):
                print('file extension not allowed')
                return render_template("upload.html")

            upload_image(imagefile,request.form["username"])

            print("image uploaded")

        if 'name' in request.form:
            delete_profile(request.form["name"])

        if 'picture' in request.form:
            delete_picture(request.form["picture"])


    return render_template("upload.html")



if __name__ == '__main__':
    app.run(debug=True)
