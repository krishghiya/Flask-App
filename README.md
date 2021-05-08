# Flask sqllite Package

This is a package used to load files and manipulate a SQLite database using DataFrames,  
on a Flask Server  

## Installation instructions:  
Need python >= 3.6  

1. Open a terminal and navigate to the project directory:
`cd path/to/project`

2. Install the .whl package:
`pip install dist/flask_sqlite-0.0.1-py3-none-any.whl`

3. You can now import the package in any python script
`from flask_sqlite import app`

4. Start the server using app.run(). You can pass in optional arguments such as port  
   just like in Flask
`app.run(port=5000)`

5. Go to a browser and visit localhost:port where port is your specified port
http://localhost:5000/
## Features

- Load data from one on of the files in to a Pandas Data-Frame (DF) with unique name  
  Clicking on a file will load and display it   

- Load data from SqlLite DB to DF with unique name  
  You can execute queries and save the result to a DF with unique name(no spaces!)

- Write DF into the SqlLite DB  
  You can insert any DF into the db by clicking the insert button  

- Write DF into the SqlLite File  
  Inserting into the db will commit it to the file  

- Given two DF names: return the column names they have in common  
  You can compare multiple DFs by clicking the checkbox and then compare. If just 1 DF is selected  
  then all columns will be returned

- For a given DF and a number N between 0 and 100, return the Nth percentile of all the  
  columns with numerical data type  
  You can click on a DF and then enter an integer between 0-100 to view the percentile results  
  for each column  

  ## Tests  

1. To run tests you need pytest  
`pip install pytest`  

2. Navigate to the project directory and run the following command  
`pytest`
