from flask import Flask, render_template, request
import mysql.connector
from mysql.connector import Error
app = Flask(__name__)


def connectdb():
    connection = mysql.connector.connect(host='localhost',
                                         database='todolist', user='root', password='cavs2016')
    return connection

@app.route('/')
def main():
    try:
        c = connectdb()
        if c.is_connected():
            s = "select * from ToDoListTable;"
            c = connectdb()
            cursor = c.cursor()
            cursor.execute(s)
            r = cursor.fetchall()
            cursor.close()
            c.close()
            return render_template('ToDoListMainPage.html',r=r)

    except Error as e:
        return f"<h1>Database Error: {e}</h1>", 500

@app.route('/Home' , methods=["POST"])
def home():
    s = "select * from ToDoListTable;"
    c = connectdb()
    cursor = c.cursor()
    cursor.execute(s)
    r = cursor.fetchall()
    return render_template('ToDoListMainPage.html',r=r)

@app.route('/AddTaskPage' , methods=["POST"])
def addtaskpage():
    return render_template('ToDoListAddTaskPage.html')

@app.route('/AddTask' , methods=["POST"])
def addtask():
    title = request.form["title"]
    duedate = request.form["duedate"]
    priority = request.form["priority"]
    s = "INSERT INTO `todolist`.`ToDoListTable` (`title`, `status`, `DueDate`, `Priority`) VALUES (%s, 'Pending', %s, %s);"
    values = (title,duedate,priority)
    c = connectdb()
    cursor = c.cursor()
    cursor.execute(s,values)
    c.commit()
    s = "select * from ToDoListTable;"
    c = connectdb()
    cursor = c.cursor()
    cursor.execute(s)
    r = cursor.fetchall()
    return render_template('ToDoListMainPage.html',r=r)

@app.route('/Delete' , methods=["POST"])
def delete():
    id = request.form["id"]
    s="DELETE FROM `todolist`.`ToDoListTable` WHERE (`id` = %s);"
    values = (id,)
    c = connectdb()
    cursor = c.cursor()
    cursor.execute(s, values)
    c.commit()
    s = "select * from ToDoListTable;"
    c = connectdb()
    cursor = c.cursor()
    cursor.execute(s)
    r = cursor.fetchall()
    return render_template('ToDoListMainPage.html', r=r)

@app.route('/Complete' , methods=["POST"])
def complete():
    id = request.form["id"]
    s = "UPDATE `todolist`.`ToDoListTable` SET `status` = 'Completed' WHERE (`id` = %s);"
    values = (id,)
    c = connectdb()
    cursor = c.cursor()
    cursor.execute(s, values)
    c.commit()
    s = "select * from ToDoListTable;"
    c = connectdb()
    cursor = c.cursor()
    cursor.execute(s)
    r = cursor.fetchall()
    return render_template('ToDoListMainPage.html', r=r)

if __name__ == '__main__':
   app.run()