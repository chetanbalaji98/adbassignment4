import pyodbc
from flask import Flask, request, render_template
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import base64
import io
import plotly
import json
from markupsafe import Markup
import plotly.graph_objs as go

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
    percentages=[]
    nval = request.form.get("task1")
    cursor.execute("select MAX(column1) from data2")
    for data in cursor:
        for value in data:
            data_max = value
    print("data_max")
    print(data_max)
    cursor.execute("select MIN(column1) from data2")
    for data in cursor:
        for value in data:
            data_min = value

    data_bin =  (data_max - data_min)/int(nval)

    print("data_bin")
    print(data_bin)
    
    print("data_min")
    print(data_min)

    for i in range(int(nval)+1):
        val = data_min + (data_bin * i)
        data_values.append(val)

    for i in range (len(data_values)-1):
        cursor.execute("select column1 from data2 where column1 >= {} and column1 <= {}".format(data_values[i], data_values[i+1]))
        lengthcheck = cursor.fetchall()
        data_pie.append(len(lengthcheck))  

    for i in range(len(data_values) -1):
        labelss = "{} - {}".format(data_values[i], data_values[i+1])
        labels.append(labelss)

    
    for i in range(len(data_pie)):
        val=data_pie[i]/50
        finval=val*100
        ufinval=str(finval)+"%"
        percentages.append(ufinval)

    print("Data Values")
    print(data_values)
    print("data_pie")
    print(data_pie)
    print (len(percentages))

    print(percentages)

    plt.figure(figsize =(7, 7))
    plt.title("Here is a pie chart with {} Slices".format(nval))
    plt.pie(data_pie, labels=percentages, startangle=0, autopct=None)
    legend1=plt.legend(data_pie, labels=data_pie, loc=1)
    plt.legend(data_pie, labels=labels,loc=3)
    plt.gca().add_artist(legend1)
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
    print(data_max,data_min)
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
    colors=['red','grey','green']
    bars  = plt.barh(data1_tab, limits,color=colors)
    
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
    
    cursor.execute("select * from data2 where column1 >= {} and column1 <= {}".format(lowval, highval))
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
    #plt.hist(xax)
    figfile = io.BytesIO()
    plt.savefig(figfile, format='jpeg')
    plt.close()
    figfile.seek(0)
    figdata_jpeg = base64.b64encode(figfile.getvalue())
    files = figdata_jpeg.decode('utf-8')
    return render_template('task3.html', outputthree = files)

@app.route('/pie', methods=['GET', 'POST'])
def pie():
    data_values = []
    data_pie = []
    labels = []
    pct_val = []
    percentages=[]
    nval = request.form.get("task1")
    print(nval)
    cursor.execute("select MAX(mag) from all_month")
    for data in cursor:
        for value in data:
            data_max = value
    print("data_max")
    print(data_max)
    cursor.execute("select MIN(mag) from all_month")
    for data in cursor:
        for value in data:
            data_min = value

    data_bin =  (data_max - data_min)/int(nval)

    print("data_bin")
    print(data_bin)
    
    print("data_min")
    print(data_min)

    for i in range(int(nval)+1):
        val = data_min + (data_bin * i)
        data_values.append(val)

    for i in range (len(data_values)-1):
        cursor.execute("select mag from all_month where mag >= {} and mag <= {}".format(data_values[i], data_values[i+1]))
        lengthcheck = cursor.fetchall()
        data_pie.append(len(lengthcheck))  

    for i in range(len(data_values) -1):
        labelss = "{} - {}".format(data_values[i], data_values[i+1])
        labels.append(labelss)

    
    for i in range(len(data_pie)):
        val=data_pie[i]/10944
        finval=val*100
        ufinval=str(finval)+"%"
        percentages.append(ufinval)

    print("Data Values")
    print(data_values)
    print("data_pie")
    print(data_pie)
    print (len(percentages))

    print(percentages)

    plt.figure(figsize =(6, 6))
    plt.title("Here is a pie chart with {} Slices".format(nval))
    plt.pie(data_pie, labels=percentages, startangle=0, autopct=None)
    legend1=plt.legend(data_pie, labels=data_pie, loc=1)
    plt.legend(data_pie, labels=labels,loc=3)
    plt.gca().add_artist(legend1)
    figfile = io.BytesIO()
    plt.savefig(figfile, format='jpeg')
    plt.close()
    figfile.seek(0)
    figdata_jpeg = base64.b64encode(figfile.getvalue())
    files = figdata_jpeg.decode('utf-8')   
    return render_template('pie.html', outputfour = files, )

@app.route('/piewithplotly',methods=['GET','POST'])
def piewithplotly():
    # retrieve user input from form
    n = int(request.form['task1'])

    # calculate ranges
    crsr.execute("SELECT MIN(column1), MAX(column1) FROM data2")
    result = crsr.fetchone()
    min_mag, max_mag = result[0], result[1]
    range_size = (max_mag - min_mag) / n

    # build query to count number of entries in each range
    count_query = "SELECT COUNT(*) FROM data2 WHERE column1 >= ? AND column1 <= ?"

    # retrieve counts for each range
    counts = []
    for i in range(n):
        lower_bound = min_mag + i * range_size
        upper_bound = lower_bound + range_size
        crsr.execute(count_query, (lower_bound, upper_bound))
        result = crsr.fetchone()
        counts.append(result[0])

    # calculate fraction of data in each slice
    total_count = sum(counts)
    fractions = [count / total_count for count in counts]

    # generate Pie Chart
    labels = [f"Range {i+1}" for i in range(n)]
    fig = go.Figure(data=[go.Pie(labels=labels, values=fractions, hole=0.6)])
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(width=800, height=600)

    # render Pie Chart in HTML template
    chart = fig.to_html(full_html=False)

    return render_template('piewithplotly.html', chart=chart)


@app.route('/barwithplotly', methods=['GET', 'POST'])
def barwithplotly():
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
    print(data_max,data_min)
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
    bar_fig = go.Figure([go.Bar(x=data1_tab,y=limits)])
    fig_json=json.dumps(bar_fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('barwithplotly.html',plot=Markup(fig_json))

    #return render_template('barwithplotly.html', outputtwo = files,)

if __name__ == "__main__":
    app.run(debug=True)