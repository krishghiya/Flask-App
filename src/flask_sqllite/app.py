from flask import Flask, render_template
import pandas as pd
import sqlite3

app = Flask(__name__)

@app.route('/')
def display():
    # data = pd.read_csv('data/deniro.csv')
    return render_template('index.html')

def run(host=None, port=None, debug=None, load_dotenv=True, **options):
    app.run(host, port, debug, load_dotenv, options)
    
if __name__=='__main__':
    app.run()