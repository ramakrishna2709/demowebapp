from mysql.connector import Error
from mysql.connector import pooling
from flask import Flask,render_template,redirect, url_for, request

app = Flask(__name__)
@app.route('/healthz')
def health():
    try:
        connection_pool = pooling.MySQLConnectionPool(pool_name="pynative_pool",
                                                    pool_size=5,
                                                    pool_reset_session=True,
                                                    host='mysql_db',
                                                    database='test_db',
                                                    user='test',
                                                    password='test123')

        print("Printing connection pool properties ")
        print("Connection Pool Name - ", connection_pool.pool_name)
        print("Connection Pool Size - ", connection_pool.pool_size)

        # Get connection object from a pool
        connection_object = connection_pool.get_connection()

        if connection_object.is_connected():
            db_Info = connection_object.get_server_info()
            print("Connected to MySQL database using connection pool ... MySQL Server version on ", db_Info)

            cursor = connection_object.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("Your connected to - ", record)
            cursor.execute("select * from test_db.myusers limit 10")
            result = cursor.fetchall()
            item = ""
            for x in range(len(result)):
                item = str(item) + str(result[x])
            print("Your data  - ", result)

    except Error as e:
        print("Error while connecting to MySQL using Connection pool ", e)
    finally:
        # closing database connection.
        if connection_object.is_connected():
            cursor.close()
            connection_object.close()
            print("MySQL connection is closed")
            
    return render_template('health.html', users=item, dbstatus=db_Info)
    

@app.route('/success/<fname>/<lname>/')
def success(fname,lname):
   
   return "Successfully stored the data with the values of {} and {}".format(fname, lname)

@app.route('/') 
def index():
   return render_template('index.html')

@app.route('/storeuser', methods=['GET', 'POST'])
def insert():
    if request.method == 'POST':
        first_name = request.form['fname']
        last_name = request.form['lname']
        connection_pool1 = pooling.MySQLConnectionPool(pool_name="pynative_pool",
                                                    pool_size=5,
                                                    pool_reset_session=True,
                                                    host='mysql_db',
                                                    database='test_db',
                                                    user='test',
                                                    password='test123')

       
        connection_object1 = connection_pool1.get_connection()

        if connection_object1.is_connected():
            db_Info = connection_object1.get_server_info()
            print("Connected to MySQL database using connection pool ... MySQL Server version on ", db_Info)

            cursor = connection_object1.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone() 
            print("Your connected to - ", record)
            cursor.execute("INSERT INTO myusers(firstname, lastname) VALUES (%s, %s)", (first_name, last_name))
            connection_object1.commit()
        return redirect(url_for('success',fname = first_name, lname = last_name))
    else:
        user = request.args.get('fname')
        return redirect(url_for('success',fname = user))
  
    
    
       
if __name__ == '__main__':
    app.run(host="0.0.0.0",debug = True )