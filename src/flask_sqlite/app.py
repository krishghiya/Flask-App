from flask import Flask, render_template, request, redirect
import pandas as pd
import sqlite3
import os

app = Flask(__name__)

custom_dfs = {}
list_files = os.listdir(os.path.join(os.path.dirname(__file__), 'data'))

def read(filename):
    return pd.read_csv('src/flask_sqlite/data/'+filename, quotechar='\"', skipinitialspace=True)

def connect():
    return sqlite3.connect('src/flask_sqlite/db/data.db')

@app.route('/', methods=['GET'])
def display(message=None):
    files = list_files[:]
    data_samples =  [read(f) for f in files]
    files += custom_dfs.keys()
    data_samples += custom_dfs.values()
    shapes = [f.shape for f in data_samples]
    data_samples = [f.head(2).to_html() for f in data_samples]

    return render_template('index.html', files=files, shapes=shapes, data_samples=data_samples, 
                                        size=len(files), message=message)

@app.route('/<filename>', methods=['GET'])
def display_file(filename, sample=None, message=None):

    #Check if custom df
    custom_bool = filename in custom_dfs.keys()

    # Test if file exists in folder
    files = list_files[:]
    
    if filename not in files and not custom_bool:
        return redirect('/')

    try:
        con = connect()
        data = pd.read_sql('select * from `%s`' % filename.split('.')[0], con)
        message = 'Dataframe in database'
        con.close()
    except:
        pass
    
    if sample is None:
        if not custom_bool:
            data = read(filename)
        else: 
            data = custom_dfs[filename]
    else:
        data = sample

    return render_template('file.html', data=data.to_html(), filename=filename, message=message)

@app.route('/display/db')
def display_db(result='', operation='None'):
    con = connect()
    data = pd.read_sql('select name from sqlite_master where type=\'table\'', con)
    con.close()
    return render_template('db.html', data=data.to_html(), result=result, operation=operation)

@app.route('/insert', methods=['POST'])
def insert():
    file = list(request.form.keys())[0]
    con = connect()

    data = custom_dfs.get(file, None)

    if data is None:
        data = read(file)
        file = file.split('.')[0]
    
    try:
        data.to_sql(name=file, con=con, index=False)
    except:
        pass

    con.close()
    return redirect('/'+file)
    
@app.route('/calculate', methods=['POST'])
def calculate():
    file, quantile = list(request.form.items())[0]
    data = custom_dfs[file] if file in custom_dfs.keys() else read(file)
    if quantile.isnumeric():
        data = data.quantile(int(quantile)/100)
        data = data.to_frame()
        data.columns = ['Value']
    return display_file(file, sample=data)

@app.route('/', methods=['POST'])
def compare():
    
    union = "No DF selected"
    
    files = [read(k) for k,v in request.form.items() if v == 'on']   
    if len(files):                                               
        union = set(files[0].columns)
        for f in files:
            union = union.intersection(set(f.columns))

    return display(message=union or "No common columns")

@app.route('/query', methods=['POST'])
def query():
    con = connect()
    text = request.form['query']
    name = request.form.get('name', ' ')
    try:
        data = pd.read_sql(text, con)
    except:
        return display_db(operation="Fail")

    files = list_files[:]
    files = [s.split('.')[0] for s in files]

    if name in files or ' ' in name:
            operation = "Save Fail"
    else:
        custom_dfs.update({name: data})
        operation = "Success"
    
    return render_template('db.html', result=data.to_html(), operation=operation)

def run(host=None, port=None, debug=None, load_dotenv=True):
    app.run(host, port, debug, load_dotenv)
    
if __name__=='__main__':
    app.run()