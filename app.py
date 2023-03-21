import pyodbc
from flask import Flask, request, render_template
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import base64
import io

application = app = Flask(__name__)
app.secret_key = "Secret Key"

app = Flask(__name__)
app.config["image_folder"] = "./static/"
app.config['UPLOAD_EXTENSIONS'] = ['jpg', 'png', 'gif']
app.secret_key = "Secret Key"


DRIVER = '{ODBC Driver 18 for SQL Server}'
SERVER = 'adbserver.database.windows.net'
DATABASE = 'chetanadb'
USERNAME = 'chetanbalaji'
PASSWORD = 'Springadb123'

cnxn = pyodbc.connect("Driver={};Server=tcp:{},1433;Database={};Uid={};Pwd={};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;".format(DRIVER, SERVER, DATABASE, USERNAME, PASSWORD))
crsr = cnxn.cursor()

conn = pyodbc.connect("Driver={};Server=tcp:{},1433;Database={};Uid={};Pwd={};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;".format(DRIVER, SERVER, DATABASE, USERNAME, PASSWORD))
cursor = conn.cursor()

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")

@app.route('/task1', methods=['GET', 'POST'])
def task1():
    data_values = []
    data_pie = []
    labels = []
    pct_val = []
    nval = request.form.get("task1")
    cursor.execute("select MAX(column1) from data2")
    for data in cursor:
        for value in data:
            data_max = value
    cursor.execute("select MIN(column1) from data2")
    for data in cursor:
        for value in data:
            data_min = value
    data_bin =  (data_max - data_min)/int(nval)
    tmp = 30
    for i in range(int(nval)+1):
        val =  tmp + data_bin
        tmp = val
        data_values.append(val)
    for i in range (len(data_values)-1):
        cursor.execute("select column1 from data2 where column1 >= {} and column1 < {}".format(data_values[i], data_values[i+1]))
        lengthcheck = cursor.fetchall()
        data_pie.append(len(lengthcheck))  
    for i in range(len(data_values) -1):
        labelss = "{} - {}".format(data_values[i], data_values[i+1])
        labels.append(labelss)
    print(data_pie)
    print(data_values)
    for i in range(len(data_pie)):
        val_pct = (data_pie[i] / int(data_values[i])) * 100
        val_pct = float(val_pct)
        pct_val.append(val_pct)
    plt.figure(figsize =(7, 7))
    plt.title("Here is a pie chart with {} Slices".format(nval))
    plt.pie(data_pie, labels=data_pie, startangle=0, autopct= "%1.2f%%")
    plt.legend(data_pie, labels=labels, loc="upper right", bbox_to_anchor=(1.1,1.025))
    figfile = io.BytesIO()
    plt.savefig(figfile, format='jpeg')
    plt.close()
    figfile.seek(0)
    figdata_jpeg = base64.b64encode(figfile.getvalue())
    files = figdata_jpeg.decode('utf-8')   
    return render_template('task1.html', outputone = files, )

@app.route('/task2', methods=['GET', 'POST'])
def task2():
    nvalue = request.form.get("task2")
    lowval =  request.form.get("task21")
    highval = request.form.get("task22")
    print(nvalue, lowval, highval)
    data1_tab = []
    limits = []
    cursor.execute("select MAX(column2) from data2 where column2>{} and column2<{}".format(lowval, highval))
    for data in cursor:
        for value in data:
            data_max = value
    cursor.execute("select MIN(column2) from data2 where column2>{} and column2<{}".format(lowval, highval))
    for data in cursor:
        for value in data:
            data_min = value
    data_bin = int(data_max - data_min)/int(nvalue)
    for i in range(int(nvalue)+1):
        val = data_min + (data_bin * i)
        val = "%.2f" % val
        data1_tab.append(val)
    for i in range (len(data1_tab)-1):
        cursor.execute("select column2 from data2 where column2 > {} and column2 < {}".format(data1_tab[i], data1_tab[i+1]))
        lengthcheck = cursor.fetchall()
        limits.append(len(lengthcheck)) 
    data1_tab.pop()
    print(data_min, data_max)
    print(data1_tab, limits)
    plt.figure(figsize =(6, 6))
    plt.title("Here is a bar chart with {} bars".format(nvalue))
    plt.xlabel("Type")
    plt.ylabel("Count")
    bars  = plt.barh(data1_tab, limits)
    plt.bar_label(bars)
    figfile = io.BytesIO()
    plt.savefig(figfile, format='jpeg')
    plt.close()
    figfile.seek(0)
    figdata_jpeg = base64.b64encode(figfile.getvalue())
    files = figdata_jpeg.decode('utf-8')
    return render_template('task2.html', outputtwo = files,)

@app.route('/task3', methods=['GET', 'POST'])
def task3():
    lowval = request.form.get("task31")
    highval = request.form.get("task32")
    yax = []
    xax = [] 
    
    cursor.execute("select * from data2 where column1 > {} and column1 < {}".format(lowval, highval))
    for data in cursor:
        yaxis =  data[0] + data[1]
        xaxis = data[0]
        yaxis = "%.2f" % yaxis
        yaxis = float(yaxis)
        yax.append(yaxis)
        xax.append(xaxis)

    plt.figure(figsize =(6, 6))
    plt.title("Here is a scatter plot")
    plt.xlabel("Type")
    plt.ylabel("Count")
    plt.scatter(xax, yax)
    figfile = io.BytesIO()
    plt.savefig(figfile, format='jpeg')
    plt.close()
    figfile.seek(0)
    figdata_jpeg = base64.b64encode(figfile.getvalue())
    files = figdata_jpeg.decode('utf-8')
    return render_template('task3.html', outputthree = files)

if __name__ == "__main__":
    app.run(debug=True)