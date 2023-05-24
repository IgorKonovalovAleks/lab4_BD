host = "127.0.0.1"
user = "postgres"
password = "q"
db_name = "postgres"
headers = {"teacher": ("id", "first name", "last name", "patronym", "phone_number", "experience"),
           "subject": ("id", "name", "specialization", "payment"),
           "specialization": ("id", "name"),
           "group": ("id", "specialization", "shift", "student number"),
           "assignment": ("id", "teacher", "group_id", "hours_amount", "subject")}

getGroups =  """SELECT public.group.group_id, public.specialization.specialization_name, public.group.shift, public.group.student_number
                        FROM public.group, public.specialization
                        WHERE public.group.specialization_id = public.specialization.specialization_id"""

getAssignments = """SELECT public.assignment.assignment_id, first_name, last_name, patronym, public.assignment.group_id, public.assignment.hours_amount, subject_name
                        FROM public.assignment, teacher, subject
                        WHERE public.assignment.teacher_id = teacher.teacher_id AND public.assignment.subject_id = subject.subject_id"""

getSpecializations = "SELECT * FROM public.specialization"

getSubjects = """SELECT subject.subject_id, subject.subject_name, specialization_name, hourly_payment
FROM subject, specialization
WHERE public.specialization.specialization_id = subject.specialization_id"""

getTeachers = "SELECT * FROM public.teacher"


insGroup = """INSERT INTO public.group (specialization_id, shift, student_number) VALUES (%s,%s, %s);"""

insTeacher = """INSERT INTO public.teacher (first_name, last_name, patronym, phone_number, experience) VALUES (%s,%s,%s,%s,%s);"""

insSubject = """INSERT INTO public.subject (subject_name, specialization_id, hourly_payment) VALUES (%s,%s,%s);"""

insSpecialization = """INSERT INTO public.specialization (specialization_name) VALUES (%s);"""

insAssignment = """INSERT INTO public.assignment (teacher_id, group_id, hours_amount, subject_id) VALUES (%s,%s,%s,%s);"""


import psycopg2
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QTableWidget, QTableWidgetItem, QHeaderView, QComboBox, QPushButton
from PyQt5.QtCore import QSize, Qt

class TableWidget(QTableWidget):
    def __init__(self, a):
        super().__init__(a)
        self.setHorizontalHeaderLabels(list('ABCDE'))
        self.verticalHeader().setDefaultSectionSize(25)
        self.horizontalHeader().setDefaultSectionSize(145)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)

    def _addRow(self):
        rowCount = self.rowCount()
        self.insertRow(rowCount )

    def _removeRow(self):
        if self.rowCount() > 0:
            self.removeRow(self.rowCount()-1)




class Example(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()
        
    
    def initUI(self):

        self.setMinimumSize(QSize(1000, 500))         
        self.setWindowTitle("LAB4")   
        central_widget = QWidget(self)              
        self.setCentralWidget(central_widget)

        self.modeRead = True

        button1 = QPushButton(self)
        button1.setText("Switch Mode")
        button1.move(900,32)

        button2 = QPushButton(self)
        button2.setText("send")
        button2.move(900,132)

        button1.clicked.connect(self.switchMode)
        button2.clicked.connect(self.send)

 
        grid_layout = QGridLayout(self)       
        central_widget.setLayout(grid_layout)  
 
        self.table = TableWidget(self) 
        self.table.setColumnCount(6)     
        self.table.setRowCount(0)
 

        self.clearTable()
        self.table.setHorizontalHeaderLabels(headers["specialization"])
 
        self.combo = QComboBox()
        self.combo.addItems(["specialization", "group", "assignment", "teacher", "subject"])
        self.combo.currentTextChanged.connect(self.textChanged)
        grid_layout.addWidget(self.combo, 0, 1)
 
        grid_layout.addWidget(self.table, 0, 0)  
        self.readSpecializations()


    def switchMode(self):
        if self.modeRead == True:
            self.clearTable()
            self.table.setHorizontalHeaderLabels(headers[str(self.combo.currentText())])
            self.table._addRow()
            self.modeRead = False
        else:
            self.clearTable()
            self.modeRead = True

    def send(self):
        t = str(self.combo.currentText())
        
        if t == "specialization":
            self.sendSpecialization()
        if t == "group":
            self.sendGroup()
        if t == "assignment":
            self.sendAssignment()
        if t == "teacher":
            self.sendTeacher()
        if t == "subject":
            self.sendSubject()

    def sendSpecialization(self):
        print(self.table.item(0, 0).text())
        data = [self.table.item(0, 0).text()]
        try:
            connection = psycopg2.connect(
            host = host,
            user = user,
            password = password,
            database = db_name
            )

            with connection.cursor() as cursor:
                cursor.execute(insSpecialization, (self.table.item(0, 1).text(),))
                connection.commit()
                print("done")
                
        except Exception as _ex:
            print("err ", _ex)
        finally:
            if connection:
                connection.close()
                print("connection closed")

    def sendTeacher(self):
        print(self.table.item(0, 0).text())
        data = [self.table.item(0, 0).text()]
        try:
            connection = psycopg2.connect(
            host = host,
            user = user,
            password = password,
            database = db_name
            )

            with connection.cursor() as cursor:
                cursor.execute(insTeacher, (self.table.item(0, 1).text(), self.table.item(0, 2).text(), self.table.item(0, 3).text(), self.table.item(0, 4).text(), self.table.item(0, 5).text()))
                connection.commit()
                print("done")
                
        except Exception as _ex:
            print("err ", _ex)
        finally:
            if connection:
                connection.close()
                print("connection closed")

    def sendSubject(self):
        print(self.table.item(0, 0).text())
        data = [self.table.item(0, 0).text()]
        try:
            connection = psycopg2.connect(
            host = host,
            user = user,
            password = password,
            database = db_name
            )

            with connection.cursor() as cursor:
                cursor.execute(insSubject, (self.table.item(0, 1).text(), self.table.item(0, 2).text(), self.table.item(0, 3).text()))
                connection.commit()
                print("done")
                
        except Exception as _ex:
            print("err ", _ex)
        finally:
            if connection:
                connection.close()
                print("connection closed")

    def sendAssignment(self):
        print(self.table.item(0, 0).text())
        data = [self.table.item(0, 0).text()]
        try:
            connection = psycopg2.connect(
            host = host,
            user = user,
            password = password,
            database = db_name
            )

            with connection.cursor() as cursor:
                cursor.execute(insAssignment, (self.table.item(0, 1).text(), self.table.item(0, 2).text(), self.table.item(0, 3).text(), self.table.item(0, 4).text()))
                connection.commit()
                print("done")
                
        except Exception as _ex:
            print("err ", _ex)
        finally:
            if connection:
                connection.close()
                print("connection closed")
    
    def sendGroup(self):
        print(self.table.item(0, 0).text())
        data = [self.table.item(0, 0).text()]
        try:
            connection = psycopg2.connect(
            host = host,
            user = user,
            password = password,
            database = db_name
            )

            with connection.cursor() as cursor:
                cursor.execute(insGroup, (self.table.item(0, 1).text(), self.table.item(0, 2).text(), self.table.item(0, 3).text()))
                connection.commit()
                print("done")
                
        except Exception as _ex:
            print("err ", _ex)
        finally:
            if connection:
                connection.close()
                print("connection closed")
    
            

    def textChanged(self, t):
        if self.modeRead == False:
            self.table.setHorizontalHeaderLabels(headers[str(self.combo.currentText())])
            return
        print(t)
        self.clearTable()
        if t == "specialization":
            self.readSpecializations()
        if t == "group":
            self.readGroups()
        if t == "assignment":
            self.readAssignments()
        if t == "teacher":
            self.readTeachers()
        if t == "subject":
            self.readSubjects()

    def ask(self, query):
        print(query)
        res = []
        try:
            connection = psycopg2.connect(
            host = host,
            user = user,
            password = password,
            database = db_name
            )

            with connection.cursor() as cursor:
                cursor.execute(query)
                c = cursor.fetchone()
                while c:
                    res.append(c)
                    c = cursor.fetchone()
        except Exception as _ex:
            print("err ", _ex)
        finally:
            if connection:
                connection.close()
                print("connection closed")
            
            return res
            
        
    
    def clearTable(self):
        for i in range(6):
            self.table.setHorizontalHeaderLabels(["" for i in range(6)])
        print(self.table.rowCount())
        while self.table.rowCount() > 0:
            self.table._removeRow()

    def readAssignments(self):

        self.table.setHorizontalHeaderLabels(headers["assignment"])
        res = self.ask(getAssignments)
        
        for i in range(len(res)):
            try:
                res[i] = (res[i][0], ' '.join(res[i][1:4]), *res[i][4:])
            except:
                res[i] = (res[i][0], ' '.join(res[i][1:3]), *res[i][4:])
        
        for i in range(len(res)):
            self.table._addRow()
            for j in range(len(res[0])):
                try:
                    self.table.setItem(i, j, QTableWidgetItem(str(res[i][j])))
                except:
                    self.table.setItem(i, j, QTableWidgetItem(''))

    def readTeachers(self):

        self.table.setHorizontalHeaderLabels(headers["teacher"])
        res = self.ask(getTeachers)
        
        for i in range(len(res)):
            self.table._addRow()
            for j in range(len(res[0])):
                try:
                    self.table.setItem(i, j, QTableWidgetItem(str(res[i][j])))
                except:
                    self.table.setItem(i, j, QTableWidgetItem(''))

    def readGroups(self):
        print(headers["group"])
        self.table.setHorizontalHeaderLabels(headers["group"])
        res = self.ask(getGroups)
        
        for i in range(len(res)):
            self.table._addRow()
            for j in range(len(res[0])):
                try:
                    self.table.setItem(i, j, QTableWidgetItem(str(res[i][j])))
                except:
                    self.table.setItem(i, j, QTableWidgetItem(''))

    def readSpecializations(self):

        self.table.setHorizontalHeaderLabels(headers["specialization"])
        res = self.ask(getSpecializations)
        
        for i in range(len(res)):
            self.table._addRow()
            for j in range(len(res[0])):
                try:
                    self.table.setItem(i, j, QTableWidgetItem(str(res[i][j])))
                except:
                    self.table.setItem(i, j, QTableWidgetItem(''))

    def readSubjects(self):

        self.table.setHorizontalHeaderLabels(headers["subject"])
        res = self.ask(getSubjects)
        
        print(res)
        for i in range(len(res)):
            self.table._addRow()
            for j in range(len(res[0])):
                try:
                    self.table.setItem(i, j, QTableWidgetItem(str(res[i][j])))
                except:
                    self.table.setItem(i, j, QTableWidgetItem(''))
                    






if __name__ == '__main__':


    

    app = QApplication(sys.argv)
    mw = Example()
    mw.show()
    sys.exit(app.exec_())
    
    
