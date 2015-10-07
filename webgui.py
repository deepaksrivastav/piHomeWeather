#!/usr/bin/env python

import sqlite3
import sys
import cgi
import cgitb


# global variables
speriod=(15*60)-1
dbname='/home/pi/piHomeWeather/weatherdb'



# print the HTTP header
def printHTTPheader():
    print "Content-type: text/html\n\n"



# print the HTML head section
# arguments are the page title and the table for the chart
def printHTMLHead(title, table):
    print "<head>"
    print "    <title>"
    print title

    print "    </title>"
    print_graph_script(table)

    print "</head>"


# get data from the database
# if an interval is passed, 
# return a list of records from the database
def get_data(interval):

    conn=sqlite3.connect(dbname)
    curs=conn.cursor()

    if interval == None or interval == "all":
        curs.execute("SELECT datetime(timestamp, 'localtime'), temperature, humidity FROM weatherdata")
    else:
	curs.execute("SELECT datetime(timestamp, 'localtime'), temperature, humidity FROM weatherdata WHERE timestamp>datetime('now','-%s hours')" % interval)
#       curs.execute("SELECT * FROM weatherdata WHERE timestamp>datetime('2013-09-19 21:30:02','-%s hours') AND timestamp<=datetime('2013-09-19 21:31:02')" % interval)

    rows=curs.fetchall()

    conn.close()

    return rows


# convert rows from database into a javascript table
def create_table(rows):
    chart_table=""

    for row in rows[:-1]:
        rowstr="['{0}', {1}, {2}],\n".format(str(row[0]),str(row[1]),str(row[2]))
        chart_table+=rowstr

    row=rows[-1]
    rowstr="['{0}', {1}, {2}]\n".format(str(row[0]),str(row[1]),str(row[2]))
    chart_table+=rowstr

    return chart_table


# print the javascript to generate the chart
# pass the table generated from the database info
def print_graph_script(table):

    # google chart snippet
    chart_code="""
    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type="text/javascript">
      google.load("visualization", "1", {packages:["corechart"]});
      google.setOnLoadCallback(drawChart);
      function drawChart() {
        var data = google.visualization.arrayToDataTable([
          ['Time', 'Temperature', 'Humidity'],
%s
        ]);

        var options = {
          title: 'piHomeWeather'
        };

        var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
        chart.draw(data, options);
      }
    </script>"""

    print chart_code % (table)




# print the div that contains the graph
def show_graph():
    print "<h2>Temperature Chart</h2>"
    print '<div id="chart_div" style="width: 900px; height: 500px;"></div>'

def print_latest_values():
    conn=sqlite3.connect(dbname)
    curs=conn.cursor()
    curs.execute("SELECT temperature, humidity,datetime(timestamp, 'localtime') FROM weatherdata order by timestamp desc limit 1")
    rowcur=curs.fetchone()
    rowstrcur="Recorded at: {2} &nbsp;| Temperature:&nbsp;{0:0.1f}&nbsp;*C&nbsp;|&nbsp;Humidity&nbsp;{1:0.1f}%".format(rowcur[0],rowcur[1],str(rowcur[2]))
    print rowstrcur
    print "<hr>"
    conn.close()


# connect to the db and show some stats
# argument option is the number of hours
def show_stats(option):

    conn=sqlite3.connect(dbname)
    curs=conn.cursor()

    if option is None or option == "all":
        option = str(24)

    curs.execute("SELECT datetime(timestamp, 'localtime') ,max(temperature) FROM weatherdata WHERE timestamp>datetime('now','-%s hour') AND timestamp<=datetime('now')" % option)
#    curs.execute("SELECT timestamp,max(temperature) FROM weatherdata WHERE timestamp>datetime('2013-09-19 21:30:02','-%s hour') AND timestamp<=datetime('2013-09-19 21:31:02')" % option)
    rowmax=curs.fetchone()
    rowstrmax="{0}&nbsp&nbsp&nbsp{1:0.1f} C".format(str(rowmax[0]),rowmax[1])

    curs.execute("SELECT datetime(timestamp, 'localtime'),min(temperature) FROM weatherdata WHERE timestamp>datetime('now','-%s hour') AND timestamp<=datetime('now')" % option)
#    curs.execute("SELECT timestamp,min(temperature) FROM weatherdata WHERE timestamp>datetime('2013-09-19 21:30:02','-%s hour') AND timestamp<=datetime('2013-09-19 21:31:02')" % option)
    rowmin=curs.fetchone()
    rowstrmin="{0}&nbsp&nbsp&nbsp{1:0.1f} C".format(str(rowmin[0]),rowmin[1])

    curs.execute("SELECT avg(temperature) FROM weatherdata WHERE timestamp>datetime('now','-%s hour') AND timestamp<=datetime('now')" % option)
#    curs.execute("SELECT avg(temperature) FROM weatherdata WHERE timestamp>datetime('2013-09-19 21:30:02','-%s hour') AND timestamp<=datetime('2013-09-19 21:31:02')" % option)
    rowavg=curs.fetchone()

# humidity
    curs.execute("SELECT datetime(timestamp, 'localtime') ,max(humidity) FROM weatherdata WHERE timestamp>datetime('now','-%s hour') AND timestamp<=datetime('now')" % option)
    hrowmax=curs.fetchone()
    hrowstrmax="{0}&nbsp&nbsp&nbsp{1:0.1f}%".format(str(hrowmax[0]),hrowmax[1])

    curs.execute("SELECT datetime(timestamp, 'localtime'),min(humidity) FROM weatherdata WHERE timestamp>datetime('now','-%s hour') AND timestamp<=datetime('now')" % option)
    hrowmin=curs.fetchone()
    hrowstrmin="{0}&nbsp&nbsp&nbsp{1:0.1f}%".format(str(hrowmin[0]),hrowmin[1])

    curs.execute("SELECT avg(humidity) FROM weatherdata WHERE timestamp>datetime('now','-%s hour') AND timestamp<=datetime('now')" % option)
    hrowavg=curs.fetchone()

    print "<hr>"

    print "<table border=1>"
    print "<tr><td>&nbsp;</td><td>Temperature</td><td>Humidity</td>"
    print "<tr><td>Max</td><td>"
    print rowstrmax
    print "</td><td>"
    print hrowstrmax
    print "</td></tr>"
    print "<tr><td>Min</td><td>"
    print rowstrmin
    print "</td><td>"
    print hrowstrmin
    print "</td></tr>"
    print "<tr><td>Avg</td><td>"
    print "%.1f" % rowavg+" C"
    print "</td><td>"
    print "%.1f" % hrowavg+" %"
    print "</td></tr>"
    print "<table>"
    print "<hr>"

    conn.close()




def print_time_selector(option):

    print """<form action="/cgi-bin/webgui.py" method="POST">
        Show the temperature logs for  
        <select name="timeinterval">"""


    if option is not None:

        if option == "6":
            print "<option value=\"6\" selected=\"selected\">the last 6 hours</option>"
        else:
            print "<option value=\"6\">the last 6 hours</option>"

        if option == "12":
            print "<option value=\"12\" selected=\"selected\">the last 12 hours</option>"
        else:
            print "<option value=\"12\">the last 12 hours</option>"

        if option == "24":
            print "<option value=\"24\" selected=\"selected\">the last 24 hours</option>"
        else:
            print "<option value=\"24\">the last 24 hours</option>"
            
        if option == "all":
			print "<option value=\"all\" selected=\"selected\">all</option>"
        else:
            print "<option value=\"all\">all</option>"

    else:
        print """<option value="6">the last 6 hours</option>
            <option value="12">the last 12 hours</option>
            <option value="24" selected="selected">the last 24 hours</option>"""

    print """        </select>
        <input type="submit" value="Display">
    </form>"""


# check that the option is valid
# and not an SQL injection
def validate_input(option_str):
    # check that the option string represents a number
    if option_str.isalnum():
        # check that the option is within a specific range
        if int(option_str) > 0 and int(option_str) <= 24:
            return option_str
        else:
            return None
    else: 
        return None


#return the option passed to the script
def get_option():
    form=cgi.FieldStorage()
    if "timeinterval" in form:
        option = form["timeinterval"].value
        return option
    else:
        return None




# main function
# This is where the program starts 
def main():

    cgitb.enable()

    # get options that may have been passed to this script
    option=get_option()

    if option is None:
        option = str(24)

    # get data from the database
    records=get_data(option)

    # print the HTTP header
    printHTTPheader()

    if len(records) != 0:
        # convert the data into a table
        table=create_table(records)
    else:
        print "No data found"
        return

    # start printing the page
    print "<html>"
    # print the head section including the table
    # used by the javascript for the chart
    printHTMLHead("piHomeWeather", table)

    # print the page body
    print "<body>"
    print "<h1>piHomeWeather</h1>"
    print "<hr>"
    print_latest_values()
    print_time_selector(option)
    show_graph()
    show_stats(option)
    print "</body>"
    print "</html>"

    sys.stdout.flush()

if __name__=="__main__":
    main()




