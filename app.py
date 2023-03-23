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

@app.route('/question10a',methods=['GET','POST'])
def question10a():
    r_from = int(request.form['low'])
    r_to = int(request.form['high'])
    n = int(request.form['n'])

    
    crsr.execute("SELECT S FROM datas")
    s_data = [row.S for row in crsr.fetchall()]
    s_data = s_data[r_from:r_to+1]
    print(s_data)
    s_data.pop()
    print(s_data)
    s_range = max(s_data) - min(s_data)
    range_size = s_range // n
    s_ranges = [min(s_data) + range_size*i for i in range(n)]
    s_ranges.append(max(s_data))

    
    s_bins = [0] * n
    for s in s_data:
        for i in range(n):
            if s >= s_ranges[i] and s <= s_ranges[i+1]:
                s_bins[i] += 1
                break

    
    sorted_bins = sorted(s_bins,reverse=True)

    
    trace = go.Bar(
        x=sorted_bins,
        y=["{} to {}".format(s_ranges[s], s_ranges[s+1]) for s in range(n)],
        orientation='h',
        marker=dict(
            color='green'
        ),
        text=sorted_bins,
        textposition='outside'
    )
    layout = go.Layout(
        width=700,
        height=500,
        margin=dict(
            l=150,
            r=50,
            b=50,
            t=50,
            pad=4
        ),
        xaxis=dict(
            title='Number of Values in each range'
        ),
        yaxis=dict(
            title='S column Ranges'
        ),
    )
    fig = go.Figure(data=[trace], layout=layout)
    return render_template('question10a.html', chart=fig.to_html())



@app.route('/question11',methods=['GET','POST'])
def question11():
    r_from = int(request.form['low'])
    r_to = int(request.form['high'])
    n = int(request.form['n'])

        
    crsr.execute("SELECT S FROM datas")
    s_data = [row.S for row in crsr.fetchall()]
    s_data = s_data[r_from:r_to+1]

        
    s_range = max(s_data) - min(s_data)
    range_size = s_range // n
    s_ranges = [min(s_data) + range_size*i for i in range(n)]
    s_ranges.append(max(s_data))

        
    s_bins = [0] * n
    for s in s_data:
        for i in range(n):
            if s >= s_ranges[i] and s <= s_ranges[i+1]:
                s_bins[i] += 1
                break

        
    sorted_bins = sorted(s_bins, reverse=True)
    trace = go.Pie(
        labels=["{} to {}".format(s_ranges[s], s_ranges[s+1]) for s in range(n)],
        values=sorted_bins,
        textinfo='value+percent',
        insidetextorientation='radial',
        hole=0.4,
        marker=dict(
            colors=['#4285F4', '#DB4437', '#F4B400', '#0F9D58'],
            line=dict(color='#FFFFFF', width=2)
        ),
        textfont=dict(size=12)
    )

    layout = go.Layout(
        width=900,
        height=500,
        margin=dict(
            l=50,
            r=50,
            b=50,
            t=50,
            pad=4
        ),
        title='S Ranges',
        title_x=0.5,
        legend=dict(orientation='h', x=0.5, y=1.1),
    )

    fig = go.Figure(data=[trace], layout=layout)
    return render_template('question11.html', chart=fig.to_html())


@app.route('/question12', methods=['GET', 'POST'])
def question12():
    lowval = request.form.get("task31")
    highval = request.form.get("task32")
    yax = []
    xax = [] 
    
    cursor.execute("select S, T from datas where R >= {} and R <= {}".format(lowval, highval))
    for data in cursor:
        yaxis =  data[0]
        xaxis = data[1]
        yaxis = "%.2f" % yaxis
        yaxis = float(yaxis)
        yax.append(yaxis)
        xax.append(xaxis)

    plt.figure(figsize =(6, 6))
    plt.title("Here is a scatter plot")
    plt.xlabel("S")
    plt.ylabel("T")
    plt.scatter(xax, yax)
    figfile = io.BytesIO()
    plt.savefig(figfile, format='jpeg')
    plt.close()
    figfile.seek(0)
    figdata_jpeg = base64.b64encode(figfile.getvalue())
    files = figdata_jpeg.decode('utf-8')
    return render_template('question12.html', outputthree = files)


















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