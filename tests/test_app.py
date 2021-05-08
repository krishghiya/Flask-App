from flask_sqlite import app
import os

def test_files():
    path = os.getcwd()
    files = os.listdir(os.path.join(path, 'src', 'flask_sqlite', 'data'))
    assert 'deniro.csv' in files and 'zillow.csv' in files and 'biostats.csv' in files

def test_db():
    path = os.getcwd()
    path = os.path.join(path, 'src', 'flask_sqlite')
    assert os.path.exists(os.path.join(path, 'db'))

def test_html():
    path = os.getcwd()
    files = os.listdir(os.path.join(path, 'src', 'flask_sqlite', 'templates'))
    assert 'index.html' in files and 'db.html' in files and 'file.html' in files

def test_read():
    path = os.getcwd()
    files = os.listdir(os.path.join(path, 'src', 'flask_sqlite', 'data'))
    try:
        [app.read(file) for file in files]
        assert True
    except:
        assert False

def test_connection():
    try:
        con = app.connect()
        con.close()
        assert True
    except:
        assert False