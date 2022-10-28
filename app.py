from flask import Flask, flash, render_template, request, redirect

import requests
import json
import pyodbc
import csv

API_KEY = '2mV1iX6Fd8Fx87j_3PDsUz5p9JjNDRfvZRqoijC4wbzF_QeXe9xReZ8TMmSjp22CQtF_WCRyzt08KHKla30wMFVOSnPqTkakoVO0_tf2oH_BCyW_FQgNgKjyoTA3Y3Yx'

SEARCH_PATH = "https://api.yelp.com/v3/businesses/search"
HEADERS = {'Authorization': 'bearer %s' % API_KEY}

'''PARAMETERS = {'location':'San Diego'}

response = requests.get(url=SEARCH_PATH, 
                        params=PARAMETERS, 
                        headers=HEADERS)
'''
#business_data = response.json()  

# print the data
#print(json.dumps(business_data, indent = 3))


server = 'rushikeshbhagat.database.windows.net'
database = 'profile'
username = 'rushi'
password = 'April@5420'   
driver= '{ODBC Driver 17 for SQL Server}'

connstr = 'DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password



app = Flask(__name__)

def upload_csv(filename):
    try:
        conn = pyodbc.connect(connstr)
        cursor = conn.cursor()
        path = './'
        count = 0
        table = 'people'
        with open (filename, 'r') as file:
            
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                row = ['NULL' if val == '' or val == '-1' else val for val in row]
                row = [x.replace("'", "''") for x in row]
                out = "'" + "', '".join(str(item) for item in row) + "'"
                out = out.replace("'NULL'", 'NULL')
                query = "INSERT INTO " + table + " VALUES (" + out + ")"
                cursor.execute(query)
                count+=1
            cursor.commit()
    
    except Exception as e:
        print(e,"Error connecting DB")

    finally:
        if conn:
            cursor.close()
            conn.close()
    print("Added " + str(count) + " rows into table " + table)


def upload_image(imagefile,username):
    try:
        conn = pyodbc.connect(connstr)
        cursor = conn.cursor()
        cursor.execute("SELECT name,picture FROM people")

        list_names = cursor.fetchall()
        list_names = dict(list_names)
        print(list_names,"type")
        
        blob_service_client = BlobServiceClient.from_connection_string(blob_connstr)
        container_client = blob_service_client.get_container_client(container_name)


        if username.capitalize() in list_names.keys():
            if imagefile.filename in list_names.values():
                container_client.upload_blob(imagefile.filename, imagefile, overwrite=True)
            else:
                container_client.upload_blob(imagefile.filename, imagefile)
                old_image = list_names[username.capitalize()]
                for blob in container_client.list_blobs():
                    if old_image == blob.name:
                        container_client.delete_blob(old_image,delete_snapshots="include")
                
                cursor.execute("UPDATE people SET picture = ? WHERE name = ?;",imagefile.filename,username)
                cursor.commit()
                
        else:
            raise Exception("Wrong Username")

    except Exception as e:
        print(e,"Error connecting DB")

    finally:
        if conn:
            cursor.close()
            conn.close()


def filter_search(name,min_sal,max_sal,room,telnum):
    try:

        conn = pyodbc.connect(connstr)
        cursor = conn.cursor()
        search_query = "SELECT * FROM people WHERE 1=1 "
        if str(name) != "None" and len(name) != 0:
                search_query += " AND LOWER(name) LIKE '%"+name.lower()+"%' "
        if str(min_sal) != "None" and str(max_sal) != "None" and len(min_sal) != 0 and len(max_sal) != 0:
            if int(min_sal) > 0 and int(max_sal) > 0:
                    search_query += " AND SALARY BETWEEN " + str(min_sal) + " AND " + str(max_sal)
        if str(telnum) != "None" and len(telnum) != 0 and int(telnum) > 0:
                search_query += " AND TELNUM = " + str(telnum)
        if str(room) != "None" and len(room) != 0 and int(room) > 0:
                search_query += " AND room = " + str(room) 
        
        cursor.execute(search_query)
        list_names = cursor.fetchall()
        
        list_names_update = []
        for item in list_names:
            print(list(item),"list(item)=") 
            item = list(item) 
            if item[6] == ' ':
                item.append('')
            else:
                item.append(f"https://{blob_account_name}.blob.core.windows.net/{container_name}/{item[6]}" )      
            list_names_update.append(item)

    except Exception as e:
        print(e,"Error connecting DB")

    finally:
        if conn:
            cursor.close()
            conn.close()
    return list_names_update


def delete_profile(username):
    try:

        conn = pyodbc.connect(connstr)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM people WHERE name = ?;",username)
        cursor.commit()
        print("deleted profile of ",username)
    except Exception as e:
        print(e,"Error connecting DB")

    finally:
        if conn:
            cursor.close()
            conn.close()

def delete_picture(username):
    try:

        conn = pyodbc.connect(connstr)
        cursor = conn.cursor()
        cursor.execute("SELECT name,picture FROM people")

        list_names = cursor.fetchall()
        list_names = dict(list_names)

        blob_service_client = BlobServiceClient.from_connection_string(blob_connstr)
        container_client = blob_service_client.get_container_client(container_name)

        if username.capitalize() in list_names.keys():
            image_name = list_names[username.capitalize()]

            for blob in container_client.list_blobs():         
                if image_name == blob.name:#check if blob exisits
                    container_client.delete_blob(image_name,delete_snapshots="include")
                    cursor.execute("UPDATE people SET picture = ' ' WHERE name = ?;",username)
                    cursor.commit()
                    print(image_name," image deleted")

    except Exception as e:
        print(e,"Error connecting DB")

    finally:
        if conn:
            cursor.close()
            conn.close()

def update_fields(name,state,sal,grade,room,telnum,keyw):
    try:

        conn = pyodbc.connect(connstr)
        cursor = conn.cursor()
        update_query = "UPDATE people SET "
        update_query += " name = '" + name + "' "
        if str(state) != "None" and len(state) != 0:
            update_query += ", state = '" + str(state) + "' "
        if str(sal) != "None" and len(sal) != 0 and int(sal) > 0:
            update_query += ", salary = " + str(sal)
        if str(grade) != "None" and len(grade) != 0 and int(grade) > 0:
            update_query += ", grade = " + str(grade)
        if str(room) != "None" and len(room) != 0 and int(room) > 0:
            update_query += ", room = " + str(room)
        if str(telnum) != "None" and len(telnum) != 0 and int(telnum) > 0:
            update_query += ", telnum = " + str(telnum)
        if str(keyw) != "None" and len(keyw) != 0:
            update_query += ", keywords = '" + keyw + "' "
        update_query += " WHERE name = '" + str(name) + "' "
        print("update_query=",update_query)
        cursor.execute(update_query)
        cursor.commit()

    except Exception as e:
        print(e,"Error connecting DB")

    finally:
        if conn:
            cursor.close()
            conn.close()


@app.route("/", methods=['GET','POST'])
@app.route("/createPlan", methods=['GET','POST'])
def index():
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
        
        cols = ["Name","Website","Image", "Ratings", "Price", "Address", "Phone No."]
        filter=[]
        for business in business_data['businesses']:
            temp=[]
            temp.append((business['name']))
            temp.append((business['url']))
            temp.append((business['image_url']))
            temp.append((business['rating']))
            if "price" in business:
                temp.append((business['price']))
            else:
                business['price']=""
                temp.append(business['price'])
            temp.append((business['location']['display_address']))
            temp.append((business['phone']))
            filter.append(temp)
            
        #print(filters)
        return render_template('createPlan.html',cols=cols,filter=filter)
        #return render_template('index.html')

    return render_template('index.html')




    
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
