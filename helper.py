#!/usr/bin/python3


# This code has been copied from Code Wizards HQ
# It adds functions to help 

import cgi, cgitb
formData = cgi.FieldStorage()

style = '''
<style>
@import url('https://fonts.googleapis.com/css?family=Open+Sans');

body {
   text-align: center;
}

table{
  background-color: white;
  border-radius: 3px;
  font-family: 'Open Sans', sans-serif;
  font-size:18px;
  background-color:#34495e;
  table-layout: fixed;
  margin:30px auto;
}

td, th{
  padding:18px;
  border-radius: 3px;
  background-color: #2c3e50;
  color:white;
  box-shadow: 2px 2px 5px #34495e;
  text-align:center;
}

th{
  background-color: #2980b9;
}
</style>
'''

def show_data(data):
    print(style)
    print("<table><tbody>")
    typeOf = str(type(data))
    if typeOf == "<class 'sqlite3.Cursor'>":
        names = list(map(lambda x: x[0], data.description))
        print("<tr>")
        for heading in names:
            print("<th>", heading ,"</th>")
        print("</tr>")

    for row in data:
        print("<tr>")
        for data in row:
            print("<td>", data, "</td>")
        print("</tr>")
    print("</tbody></table>")

def get_input():
    if (formData):
        data = {}
        for key in formData.keys():
            data[key] = formData[key].value
        return data

def todo_app(data):
    taskHtml = "<li id={taskId} class={taskStatus}>{task}</li>"
    tasks = " "
    if len(data) > 0:
        userId = data[0][0]
        firstName = data[0][1]
        lastName = data[0][2]
        for row in data:
            if row[5] is not None and row[6] is not None and row[7] is not None:
                taskData = {
                    'taskId':row[5],
                    'task':row[6],
                    'taskStatus':row[7]
                }
                tasks += taskHtml.format(**taskData)
        listHtml = """
        <h1>Here are your tasks, """ + firstName + " " + lastName + """</h1>
        <form id ='addtask-form'>
          <input type='text' id='todo' required>
          <input type='submit'>
        </form>
        <ol id ='""" + str(userId) + """' class='taskList'>""" + tasks + """</ol>
        """
        print(listHtml)
    else:
        print("wrong username password")

import json

def create_json(cursor):
    headers = list(map(lambda x: x[0], cursor.description))
    results = []

    for row in cursor.fetchall():
        rowData = {}
        for i, col in enumerate(row):
            rowData[headers[i]] = col
        results.append(rowData)
    return json.dumps(results)

def tasks_html(data):
    html = "<li id={taskId} class={taskStatus}>{task}</li>"
    finalHtml = ""
    for row in data:
        taskData = {
            'taskId': row[1],
            'task': row[2],
            'taskStatus': row[3]
        }
        finalHtml += html.format(**taskData)
    print(finalHtml)