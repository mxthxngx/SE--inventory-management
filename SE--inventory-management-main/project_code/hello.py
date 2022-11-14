
from flask import Flask
import json
from flask import Flask, render_template, request, url_for, flash, redirect
import sqlite3
from matplotlib.pyplot import title
from werkzeug.exceptions import abort

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__)

def get_record(item_name):
    conn = get_db_connection()
    print(item_name)
    record = conn.execute('SELECT * FROM orderDetails WHERE item_name = ?',(item_name,)).fetchone()
    print("rec: ",record)
    conn.close()
    if record is None:
        abort(404)
    return record

@app.route('/billing',methods=('GET','POST'))
def edit():
    
    if request.method=='GET':
        conn = get_db_connection()
        rec = {}
        record = conn.execute('SELECT * FROM stockDetails').fetchall()
        for i in range(0,len(record)):
            x = []
            for j in range(1,record[i][2]+1):
                x.append(j)
            rec[record[i][1]] = x
        rec = json.dumps(rec)
        
            
        

        conn.close()    
    if request.method == 'POST':
        item_name = request.form['item_name']
        items_available = request.form['items_available']
        conn = get_db_connection()
        items_total = (conn.execute('SELECT items_total FROM stockDetails WHERE item_name = ?',(item_name,)).fetchone())
        items_total = items_total[0]
        items_avail = (conn.execute('SELECT items_available FROM stockDetails WHERE item_name = ?',(item_name,)).fetchone())
        items_avail = items_avail[0]
        conn.commit()
        conn.close()
        
        if((items_avail-int(items_available))==0 or int(items_available)<0):
            conn = get_db_connection()
            print("here")
            conn.execute('DELETE FROM stockDetails WHERE item_name = ?',(item_name,))
            conn.commit()
            conn.close()
            return redirect(url_for('edit'))
            
        
        else:
            itemavail =items_avail-int(items_available)
            print("itemavail = ",items_available," ",itemavail)
            conn = get_db_connection()
            conn.execute('UPDATE stockDetails SET items_available = ? WHERE item_name = ?',(itemavail,item_name))
            conn.commit()
            conn.close()
            return redirect(url_for('edit'))
        

            

    


    return render_template('edit.html',record=record,rec=rec)



@app.route('/', methods=('GET', 'POST'))
def home():
    error = ""
    conn = get_db_connection()
    if request.method == 'POST':
        auth =""
        username = request.form['username']
        passw = request.form['password']
        authdeets = conn.execute('SELECT * FROM auth where username = ? and passw = ?',(username,passw)).fetchone()
        if authdeets:
            for auth in authdeets:
                print(auth)
        if auth != "":
            print("here")
            return redirect(url_for('index'))
        else:
            error = "INVALID DETAILS"
        conn.commit()
        conn.close()
        

    return render_template('home_auth.html',error = error)


@app.route('/ordered')
def index():
    conn = get_db_connection()
    orderdeets = conn.execute('SELECT * FROM orderDetails').fetchall()
    conn.close()
    print((orderdeets[1]['items']))
    return render_template('index2.html', orderdeets= orderdeets)


@app.route('/stock')
def stock():
    conn = get_db_connection()
    stockdeets = conn.execute('SELECT * FROM stockDetails').fetchall()
    conn.close()
    return render_template('stock.html', stockdeets= stockdeets)


@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        partner_name = request.form['partner_name']
        item_name = request.form['item_name']
        destination = request.form['destination']
        items = request.form['items']
        item_status = request.form['item_status']

        if not partner_name:
            flash('name is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO orderDetails (partner_name, destination,item_name,items,item_status) VALUES (?, ?,?,?,?)',
                         (partner_name,destination, item_name,items,item_status))
            pending = conn.execute('SELECT item_name,item_status FROM orderDetails  WHERE item_status = "Pending"')
            all =  conn.execute('SELECT * FROM orderDetails')
            flag = 0
            for i in pending:
                
                print("item from all:",i['item_name'])
                for j in all:
                    print("item from pending:",j['item_name'])
                    if(i['item_name'] == j['item_name']):
                        flag = 1
                        break
                    print(i["item_name"])
            if(flag == 0):
                    conn.execute("INSERT INTO stockDetails (item_name,items_available,items_total, action_needed) VALUES (?,?,?,?)",
            (item_name,items,items,'available'))

            
            
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')


@app.route('/<string:item_name>/edit', methods=('GET', 'POST'))
def edit_order(item_name):
    conn = get_db_connection()
    print(item_name)
    orders = get_record(item_name)
    
    
    print("order[item]",orders['item_name'])
    if request.method == 'POST':
        item_name = item_name
        partner_name = request.form['partner_name']
        destination = request.form['destination']
        items = request.form['items']
        item_status = request.form['item_status']
        print("item status ",item_status)
        if(item_status=="Delivered"):
            print("updated")
            conn.execute("INSERT INTO stockDetails (item_name,items_available,items_total, action_needed) VALUES (?,?,?,?)",
            (item_name,items,items,'available'))
        conn.execute('UPDATE orderDetails SET item_name = ?, partner_name = ?,destination=?, items = ?,item_status = ?'
                         ' WHERE item_name = ?',
                         (item_name,partner_name,destination, items,item_status,item_name))
        
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('edit_order.html', order = orders)


if __name__ == "__main__":
    app.run()
    
    
    
    
    

