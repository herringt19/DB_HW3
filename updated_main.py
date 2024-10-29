from flask import Flask, render_template
import util

# create an application instance
# all requests it receives from clients to this object for handling
# we are instantiating a Flask object by passing __name__ argument to the Flask constructor. 
# The Flask constructor has one required argument which is the name of the application package. 
# Most of the time __name__ is the correct value. The name of the application package is used 
# by Flask to find static assets, templates and so on.
app = Flask(__name__)

# evil global variables
# can be placed in a config file
# here is a possible tutorial how you can do this
username='raywu1990'
password='test'
host='127.0.0.1'
port='5432'
database='dvdrental'

# route is used to map a URL with a Python function
# complete address: ip:port/
# 127.0.0.1:5000/
@app.route('/')
# this is how you define a function in Python
def index():
    # this is your index page
    # connect to DB
    cursor, connection = util.connect_to_db(username,password,host,port,database)
    # execute SQL commands
    record = util.run_and_fetch_sql(cursor, "select * from basket_a full join basket_b on basket_a.a = basket_b.b;")
    if record == -1:
        # you can replace this part with a 404 page
        print('Something is wrong with the SQL command')
    else:
        # this will return all column names of the select result table
        # ['a', 'fruit_a', 'b', 'fruit_b']
        col_names = [desc[0] for desc in cursor.description]
        # only use the first five rows
        log = record[:5]
        # log=[[1,2],[3,4]]
    # disconnect from database
    util.disconnect_from_db(connection,cursor)
    # using render_template function, Flask will search
    # the file named index.html under templates folder
    return render_template('index.html', sql_table = log, table_title=col_names)
@app.route('/api/update_basket_a')
def update_basket_a():
    try:
        # Connect to the database
        cursor, connection = util.connect_to_db(username, password, host, port, database)
        
        # Check if the entry already exists
        cursor.execute("SELECT 1 FROM basket_a WHERE a = 5")
        exists = cursor.fetchone()
        
        if exists:
            # Entry exists, so return error message
            return "Entry (5, 'Cherry') already exists in basket_a!", 200
        else:
            # Entry does not exist, so proceed with insert
            cursor.execute("INSERT INTO basket_a (a, fruit_a) VALUES (5, 'Cherry')")
            connection.commit()
            return "Success!"
    
    except Exception as e:
        # Capture and return the error message
        error_message = f"Error: {e}"
        print(error_message)  # Log to terminal
        return error_message, 500

    util.disconnect_from_db(connection, cursor)

@app.route('/api/unique')
def unique_fruits():
    try:
        # Connect to the database
        cursor, connection = util.connect_to_db(username, password, host, port, database)
        
        # Retrieve unique fruits from both tables
        fruits_a = set(row[0] for row in util.run_and_fetch_sql(cursor, "SELECT fruit_a FROM basket_a"))
        fruits_b = set(row[0] for row in util.run_and_fetch_sql(cursor, "SELECT fruit_b FROM basket_b"))
        
        # Prepare unique fruits and render in HTML table
        unique_a = fruits_a - fruits_b
        unique_b = fruits_b - fruits_a
        
        table_title = ["Unique in basket_a", "Unique in basket_b"]
        sql_table = [[", ".join(unique_a), ", ".join(unique_b)]]
        
        return render_template('index.html', table_title=table_title, sql_table=sql_table)

    except Exception as e:
        return f"Error: {e}", 500

    util.disconnect_from_db(connection, cursor)

if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1')

