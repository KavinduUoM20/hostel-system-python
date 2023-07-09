from PyQt6.QtWidgets import QMainWindow, QDialog, QMessageBox, QTableWidgetItem, QStackedWidget, QWidget, QApplication
from PyQt6.QtCore import QTimer, QTime, QDate, Qt
from PyQt6.QtGui import QPalette, QColor
from MainForm import Ui_MainWindow
from datetime import datetime
from docxtpl import DocxTemplate
import os
import DBConnection as DB
import time


class HostelSystem(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()

        self.GLOBAL_HOSTEL_STATUS = False
        # MainForm Functions ----------------------------------------------------------------------------

        # MainForm : Switch Between Pages

        self.pushButton_2.clicked.connect(self.showHome)
        self.pushButton_3.clicked.connect(self.showStudents)
        self.pushButton_4.clicked.connect(self.showEmployees)
        self.pushButton_5.clicked.connect(self.showHostels)

        # MainForm : Logout Button
        self.pushButton_21.clicked.connect(self.logout)

        # Home Page Functions ----------------------------------------------------------------------------


        # Home: Display Home Page By Default
        self.showHome()

        # Home: Display Date
        self.updateDate()

        # Home: Display Time
        timer = QTimer(self)
        timer.timeout.connect(self.updateTime)
        timer.start(1000)

        # Home: ID Scanned
        self.StudentIDText.textChanged.connect(self.LoadStudents)

        # Student Page Functions -------------------------------------------------------------------------

        # Student: Load Faculties
        self.loadFaculties()

        # Student: Load Batches
        #self.FacultyCombo.currentIndexChanged.connect(self.loadBatches)

        # Student: Register Student
        self.SaveStudentButton.clicked.connect(self.registerStudent)

        # Student: Search Student
        self.SearcStudentButton.clicked.connect(self.searchStudent)

        # Student: View Students
        self.viewStudets()

        # Student: Show Available Hostel
        self.LoadHostelsForStudents()

        # Employee Page Functions -----------------------------------------------------------------------

        # Employee : Register Employee
        self.SaveEmployeeButton.clicked.connect(self.registerEmployee)

        # Employee : Search Employee
        self.SearchEmployeeButton.clicked.connect(self.searchEmployee)

        # Employee : View Employees
        self.viewEmployees()

        # Employee : Change Hostel
        self.ChangeHostelButton.clicked.connect(self.enableChangeHostel)

        # Employee : Save Hotel Assignment
        self.SameAssignmentButton.clicked.connect(self.saveHostelAssignment)

        # Employee :
        self.EmployeeIDText_2.textChanged.connect(self.clearIDText)
        # Hostel Page Functions ------------------------------------------------------------------------

        # Hostel : Register Hostel
        self.AddHostelButton.clicked.connect(self.registerHostel)

        # Hostel : Register Room
        self.AddRoomButton.clicked.connect(self.registerRoom)

        # Hostel : Load Hostels
        #self.tab_12..connect(self.LoadHostels)
        # Hostel : Search Hostel
        self.SearchHostelButton.clicked.connect(self.searchHostel)

        # Hostel : View Hostels
        self.ViewHostels()

        self.LoadHostels()


#-------------------------------------------------------------------------------------------------------
#--------------------------------------CONTROLLER FUNCTIONS---------------------------------------------
#-------------------------------------------------------------------------------------------------------

    # (1) MainForm Controller ---------------------------------------------------------------------------

    def showHome(self):
        self.stackedWidget.setCurrentWidget(self.home)

    def showStudents(self):
        self.stackedWidget.setCurrentWidget(self.students)

    def showEmployees(self):
        self.stackedWidget.setCurrentWidget(self.employees)


    def showHostels(self):
        self.stackedWidget.setCurrentWidget(self.Hostels)

    def logout(self):
        alert = QMessageBox()
        alert.setIcon(QMessageBox.Icon.Question)
        alert.setWindowTitle('Quit Confirmation')
        alert.setText('Are you sure you want to quit?')
        alert.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        # Set the default button when Enter is pressed
        alert.setDefaultButton(QMessageBox.StandardButton.No)

        # Executing the alert box
        result = alert.exec()

        if result == QMessageBox.StandardButton.Yes:
            # User clicked Yes
            print("Quit confirmed.")
            QApplication.quit()

        else:
            # User clicked No or closed the alert box
            print("Quit canceled.")

    # (2) Home Page Controller -----------------------------------------------------------------------------

    def updateTime(self):
        current_time = QTime.currentTime()
        time_text = current_time.toString('hh:mm')
        self.TodayTimeLCD.display(time_text)

    def updateDate(self):
        current_date = QDate.currentDate()
        date_text = current_date.toString('yyyy-MM-dd')

        self.TodayDateLabel.setText(date_text)

    def loadFaculties(self):
        try:
            self.FacultyCombo.clear()
            mydb = DB.DBConnection.getConnection()
            query = "SELECT * FROM `faculty`"
            cursor = mydb.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()

            for row in rows:
                self.FacultyCombo.addItem(str(row[0])+"-"+str(row[1]))


            cursor.close()
        except Exception as e:
            print(e)

    # Load Batches
    def loadBatches(self):
        textstr = self.FacultyCombo.currentText()
        facid= ''.join(filter(str.isdigit, textstr))
        try:
            self.FacultyCombo.clear()
            mydb = DB.DBConnection.getConnection()
            query = "SELECT `batchid` FROM `batch` WHERE `facultyid` = '"+facid+"';"
            cursor = mydb.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()

            for row in rows:
                self.BatchCombo.addItem(str(row[1]))

            cursor.close()
        except Exception as e:
            print(e)

    # (3) Student Page Controller -------------------------------------------------------------------------

    # Student: Register Student
    def registerStudent(self):
        id = self.StudentIDText_2.text()
        date_str = self.AdmissionDateCalander.text()
        date_obj = datetime.strptime(date_str, "%d-%b-%y")
        date = date_obj.strftime("%d-%m-%y")
        textstr = self.FacultyCombo.currentText()
        fac = ''.join(filter(str.isdigit, textstr))
        batch = self.BatchCombo.currentText()
        hostel = self.HostelCombo.currentText()
        room = self.RoomIDText_2.text()
        fname = self.StudentNameText_2.text()
        addr = self.AddressText_2.toPlainText()
        tel = self.TelephoneNoText.text()

        try:
            mydb = DB.DBConnection.getConnection()
            query = "INSERT INTO `student`(`studentid`, `name`, `address`, `admission`, `roomid`, `telephone`, `batchid`, `facultyid`) VALUES ('"+id+"','"+fname+"','"+addr+"','"+date+"','"+room+"','"+tel+"','"+batch+"','"+fac+"');"
            cursor = mydb.cursor()
            cursor.execute(query)
            mydb.commit()
            cursor.close()
            QMessageBox.information(QMessageBox(), 'Register Student', 'Student Registered Successfully !')
            self.viewStudets()
            self.StudentIDText_2.clear()
            self.AdmissionDateCalander.clear()
            self.FacultyCombo.clear()
            self.BatchCombo.clear() # Not Clearing
            self.HostelCombo.clear()
            self.RoomIDText_2.clear()
            self.StudentNameText_2.clear()
            self.AddressText_2.clear()
            self.TelephoneNoText.clear()
        except Exception as e:
            print(e)

    # Student: Search Student - Done
    def searchStudent(self):
        id = self.StudentIDCombo.currentText()
        if self.SearcStudentButton.text() == "Search Student":
            try:
                mydb = DB.DBConnection.getConnection()
                query = "SELECT s.studentid, s.name, s.address, s.admission, s.roomid, s.telephone, s.batchid, f.name, h.name FROM student s  JOIN faculty f ON s.facultyid = f.facultyid JOIN room r ON s.roomid = r.roomid JOIN hostel h on r.hostelid = h.hostelid WHERE s.studentid = '"+id+"';"
                cursor = mydb.cursor()
                cursor.execute(query)
                result = cursor.fetchone()
                self.StudentNameText_3.setText(str(result[1]))
                self.FacultyText.setText(str(result[7]))
                self.BatchNoText_2.setText(str(result[6]))
                self.HostelNameText_4.setText(str(result[8]))
                self.RoomIDText_3.setText(str(result[4]))
                self.AddressText.setText(str(result[2]))
                self.TelephoneNoText_2.setText(str(result[5]))
                self.AdmissionDateText.setText(str(result[3]))
                self.SearcStudentButton.setText("Print Student")
                cursor.close()
            except Exception as e:
                print(e)

        elif self.SearcStudentButton.text() == "Print Student":
            alert = QMessageBox()
            alert.setIcon(QMessageBox.Icon.Question)
            alert.setWindowTitle('Print Student')
            alert.setText('Do You Want to Print Student?')
            alert.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            # Set the default button when Enter is pressed
            alert.setDefaultButton(QMessageBox.StandardButton.No)
            # Executing the alert box
            result = alert.exec()
            if result == QMessageBox.StandardButton.Yes:
                # User clicked Yes
                print("print")
                # Get Student Details
                name = self.StudentNameText_3.text()
                fac = self.FacultyText.text()
                batch = self.BatchNoText_2.text()
                hostel = self.HostelNameText_4.text()
                room = self.RoomIDText_3.text()
                addr = self.AddressText.toPlainText()
                tel = self.TelephoneNoText_2.text()
                admission = self.AdmissionDateText.text()
                id = self.StudentIDCombo.currentText()

                # Load the template file
                doc = DocxTemplate("template.docx")

                # Define the context with your variables
                context = {
                    'id': id,
                    'admission': admission,
                    'fac': fac,
                    'batch': batch,
                    'hostel': hostel,
                    'room': room,
                    'name': name,
                    'addr': addr,
                    'tel': tel
                }

                # Render the template with the context
                doc.render(context)

                # Create the output directory if it doesn't exist
                os.makedirs("./output/word/", exist_ok=True)

                # Save the generated DOCX file to the word directory
                output_word = f"./output/word/{id}.docx"
                doc.save(output_word)

                # Set Text
                self.SearcStudentButton.setText("Clear")
            else:
                # User clicked No or closed the alert box
                print("no")
                self.SearcStudentButton.setText("Clear")
        else:
            self.clearSearchIDText()

    # Student: View Students - Done
    def viewStudets(self):
        try:
            mydb = DB.DBConnection.getConnection()
            query = "SELECT s.studentid, s.name,f.name AS faculty_name, s.roomid, h.name AS hostel_name FROM student s JOIN room r ON s.roomid = r.roomid JOIN hostel h ON r.hostelid = h.hostelid JOIN faculty f ON s.facultyid = f.facultyid;"
            cursor = mydb.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            self.StudentTable.setRowCount(0)
            for row_num, row_data in enumerate(result):
                self.StudentTable.insertRow(row_num)
                for column_num,column_data in enumerate(row_data):
                    self.StudentTable.setItem(row_num, column_num,QTableWidgetItem(str(column_data)))
            cursor.close()
        except Exception as e:
            print(e)

    # Student: Load Student for Attendance - Done
    def LoadStudents(self):
        id = self.StudentIDText.text()

        #self.StudentNameText.setText()
        try:
            mydb = DB.DBConnection.getConnection()
            cursor = mydb.cursor()
            query1 = "SELECT name FROM student WHERE studentid = '"+id+"';"
            query2 = "SELECT * FROM attendance WHERE studentid = '"+id+"' AND date = CURRENT_DATE ;"
            cursor.execute(query1)
            result1 = cursor.fetchone()
            cursor.execute(query2)
            result2 = cursor.fetchall()
            self.StudentNameText.setText(result1[0])

            palette = self.EntranceStatus.palette()
            if len(result2)==0:
                query3 = "INSERT INTO attendance (studentid, date, checkin) VALUES ('"+id+"', CURRENT_DATE, CURRENT_TIME);"
                cursor.execute(query3)
                mydb.commit()
                palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.green)
                self.EntranceStatus.setPalette(palette)
                self.EntranceStatus.setText("IN")
                QMessageBox.information(QMessageBox(), 'Student Attendance', 'Student Checked In !')
                self.EntranceStatus.clear()
                self.StudentNameText.clear()
                self.StudentIDText.clear()
            else:
                aid = str(result2[0][0])
                query3 = "UPDATE attendance SET checkout = CURRENT_TIME WHERE attendanceid = '"+aid+"' AND studentid = '"+id+"'"
                cursor.execute(query3)
                mydb.commit()
                palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.red)
                self.EntranceStatus.setPalette(palette)
                self.EntranceStatus.setText("OUT")
                QMessageBox.information(QMessageBox(), 'Student Attendance', 'Student Checked Out!')
                self.EntranceStatus.clear()
                self.StudentNameText.clear()
                self.StudentIDText.clear()
            cursor.close()
        except Exception as e:
            print(e)


    # (4) Employee Page Controller ----------------------------------------------------------------------

    # Employee: Register Employee - Done
    def registerEmployee(self):
        eid =self.EmployeeIDText.text()
        ename = self.EmployeeNameText.text()
        addr = self.EmployeeAddress.toPlainText().replace('\n', ',')
        cat = self.EmployeeCategoryCombo.currentText()
        tele = self.EmployeeTelephoneText.text()
        try:
            mydb = DB.DBConnection.getConnection()
            query = "INSERT INTO `employee`(`employeeid`, `name`, `category`, `address`, `telephone`) VALUES ('"+eid+"','"+ename+"','"+cat+"','"+addr+"','"+tele+"');"
            cursor = mydb.cursor()
            cursor.execute(query)
            mydb.commit()
            cursor.close()
            QMessageBox.about(QMessageBox(), 'Register Employee', 'Employee Registered Successfully !')
            self.EmployeeNameText.clear()
            self.EmployeeAddress.clear()
            self.EmployeeIDText.clear()
            self.EmployeeTelephoneText.clear()
            self.viewEmployees()
        except Exception as e:
            print(e)


    # Employee: Search Employee -
    def searchEmployee(self):
        eid = self.EmployeeIDText_2.text()
        try:
            mydb = DB.DBConnection.getConnection()
            query1 = "SELECT e.name, eh.hostelid, h.name FROM employee e JOIN employee_hostel eh ON e.employeeid = eh.employeeid JOIN hostel h ON h.hostelid = eh.hostelid WHERE e.employeeid ='"+eid+"';"
            cursor = mydb.cursor()
            cursor.execute(query1)
            result1 = cursor.fetchone()
            if result1!=None:
                self.EmployeeNameText_2.setText(result1[0])
                self.EmployeeHostelCombo.setCurrentText(str(result1[1]))
                self.EmployeeNameText_2.setReadOnly(True)
                self.EmployeeHostelCombo.setEnabled(False)
            else:
                self.GLOBAL_HOSTEL_STATUS = True
                query2 = "SELECT name FROM employee WHERE employeeid='"+eid+"'"
                cursor.execute(query2)
                result2 = cursor.fetchone()
                self.EmployeeNameText_2.setText(result2[0])
                self.EmployeeHostelCombo.setEnabled(True)
                #self.ChangeHostelButton.setEnabled(False)


        except Exception as e:
            print(e)

    # Employee: Enable Change Hostel
    def enableChangeHostel(self):
        self.GLOBAL_HOSTEL_STATUS = False
        self.EmployeeHostelCombo.setEnabled(True)
        self.LoadHostels()

    # Employee: Save Hostel Assignment
    def saveHostelAssignment(self):
        eid = self.EmployeeIDText_2.text()
        hid = self.EmployeeHostelCombo.currentText()
        try:
            mydb = DB.DBConnection.getConnection()
            cursor = mydb.cursor()
            if self.GLOBAL_HOSTEL_STATUS == True:
                query1 = "INSERT INTO `employee_hostel` (`employeeid`,`hostelid`,`assigned`) VALUES ('"+eid+"','"+hid+"',CURRENT_DATE);"
                cursor.execute(query1)
                mydb.commit()
                QMessageBox.about(QMessageBox(), 'Assign Hostel', 'Hostel Assigned Successfully !')
                self.viewEmployees()
                self.clearEmployeeAssignText()
            else:
                query2 = "UPDATE `employee_hostel` SET `hostelid` = '"+hid+"', `assigned` = CURRENT_DATE WHERE `employeeid` = '"+eid+"';"
                cursor.execute(query2)
                mydb.commit()
                QMessageBox.about(QMessageBox(), 'Update Hostel', 'Hostel Updated Successfully !')
                self.viewEmployees()
                self.clearEmployeeAssignText()

            cursor.execute(query1)
            mydb.commit()
            cursor.close()
            QMessageBox.about(QMessageBox(), 'Assign Hostel', 'Hostel Assigned Successfully !')
            self.EmployeeIDText_2.clear()
            self.EmployeeNameText_2.clear()
            self.LoadHostels()
            self.EmployeeHostelCombo.setEnabled(False)
        except Exception as e:
            print(e)

    # Employee: Save Hostel Assignment
    def viewEmployees(self):
        try:
            mydb = DB.DBConnection.getConnection()
            query = "SELECT e.employeeid, e.name, e.category, h.name AS hostel_name FROM employee e JOIN employee_hostel eh ON e.employeeid = eh.employeeid JOIN hostel h ON eh.hostelid = h.hostelid;"
            cursor = mydb.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            print(result)
            self.EmployeeTable.setRowCount(0)
            for row_num, row_data in enumerate(result):
                self.EmployeeTable.insertRow(row_num)
                for column_num, column_data in enumerate(row_data):
                    self.EmployeeTable.setItem(row_num, column_num, QTableWidgetItem(str(column_data)))
            cursor.close()
        except Exception as e:
            print(e)

    def clearIDText(self):
        id = self.EmployeeIDText_2.text()
        if len(id) == 0:
            self.GLOBAL_HOSTEL_STATUS = False
            self.EmployeeNameText_2.clear()
            self.EmployeeHostelCombo.clear()

    def clearSearchIDText(self):
        self.StudentIDCombo.clearEditText()
        self.StudentNameText_3.clear()
        self.FacultyText.clear()
        self.BatchNoText_2.clear()
        self.HostelNameText_4.clear()
        self.RoomIDText_3.clear()
        self.AddressText.clear()
        self.TelephoneNoText_2.clear()
        self.AdmissionDateText.clear()
        self.SearcStudentButton.setText("Search Student")

    def clearEmployeeAssignText(self):
        self.EmployeeIDText_2.clear()
        self.EmployeeNameText_2.clear()
        self.EmployeeHostelCombo.clearEditText()

    # (5) Hostel Page Controller -------------------------------------------------------------------------

    # Hostel: Register Hostel
    def registerHostel(self):
        hid = self.HostelIDText.text()
        hname = self.HostelNameText_2.text()
        hloc = self.HostelLocationText.text()
        try:
            mydb = DB.DBConnection.getConnection()
            query = "INSERT INTO `hostel`(`hostelid`, `name`, `location`) VALUES ('"+hid+"','"+hname+"','"+hloc+"');"
            cursor = mydb.cursor()
            cursor.execute(query)
            mydb.commit()
            cursor.close()
            QMessageBox.about(QMessageBox(), 'Register Hostel', 'Hostel Registered Successfully !')
            self.HostelIDText.clear()
            self.HostelNameText_2.clear()
            self.HostelLocationText.clear()
            self.LoadHostels()
        except Exception as e:
            print(e)

    # Hostel: View Hostel - Done
    def ViewHostels(self):
        try:
            mydb = DB.DBConnection.getConnection()
            query = "SELECT h.hostelid, h.name, h.location, (SELECT COUNT(*) FROM room r WHERE r.hostelid = h.hostelid ) AS num_rooms FROM Hostel h;"
            cursor = mydb.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            self.HostelTable.setRowCount(0)
            for row_num, row_data in enumerate(result):
                self.HostelTable.insertRow(row_num)
                for column_num,column_data in enumerate(row_data):
                    self.HostelTable.setItem(row_num, column_num,QTableWidgetItem(str(column_data)))
            cursor.close()
        except Exception as e:
            print(e)

    # Hostel: Search Hostel - Done
    def searchHostel(self):
        id = self.SelectHostelCombo.currentText()
        try:
            mydb = DB.DBConnection.getConnection()
            query = "SELECT  `name`, `location` FROM `hostel` WHERE `hostelid`='"+id+"';"
            cursor = mydb.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            self.HostelNameText.setText(rows[0][0])
            self.HostelLoctionText.setText(rows[0][1])
            # Hostel : View Rooms - Inside Search Hostels
            self.viewRooms(id)
        except Exception as e:
            print(e)

    # Hostel: Load Hostels - In Hostels Form - Done
    def LoadHostels(self):
        try:
            self.HostelIDCombo.clear()
            self.SelectHostelCombo.clear()
            self.EmployeeHostelCombo.clear()
            mydb = DB.DBConnection.getConnection()
            query = "SELECT `hostelid` FROM `hostel`;"
            cursor = mydb.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()

            for row in rows:
                hostelid = row[0]
                self.HostelIDCombo.addItem(str(hostelid))
                self.SelectHostelCombo.addItem(str(hostelid))
                self.EmployeeHostelCombo.addItem(str(hostelid))
                self.HostelIDText.setText(str(hostelid+1))

            cursor.close()
        except Exception as e:
            print(e)



    # Hostel: Load Hostels - In Student Form
    def LoadHostelsForStudents(self):
        try:
            mydb = DB.DBConnection.getConnection()
            cursor = mydb.cursor()
            # Check Whether the Capacity of the Room Exceeded
            query1 = "SELECT * FROM `hostel`"
            cursor.execute(query1)
            results = cursor.fetchall()

            for row in results:
                self.HostelCombo.addItem(str(row[0])+"-"+row[1])

            #self.RoomIDText_2.setReadOnly(True)
            self.HostelCombo.setEnabled(False)

            cursor.close()
        except Exception as e:
            print(e)

    # Hostel: Register Hostel - Done
    def registerRoom(self):
        hid = self.HostelIDCombo.currentText()
        rid = self.RoomIDText.text()
        rcap = self.RoomCapacityText.text()
        try:
            mydb = DB.DBConnection.getConnection()
            query = "INSERT INTO `room`(`roomid`, `capacity`, `hostelid`) VALUES ('"+rid+"','"+rcap+"','"+hid+"');"
            cursor = mydb.cursor()
            cursor.execute(query)
            mydb.commit()
            cursor.close()
            QMessageBox.about(QMessageBox(), 'Register Room', 'Room Registered Successfully !')
            self.RoomIDText.clear()
            self.RoomCapacityText.clear()
        except Exception as e:
            print(e)

    # Hostel: View Rooms - Done
    def viewRooms(self,hid):
        try:
            mydb = DB.DBConnection.getConnection()
            query = "SELECT `roomid`, `capacity` FROM `room` WHERE `hostelid`='"+hid+"';"
            cursor = mydb.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            self.RoomTable.setRowCount(0)
            for row_num, row_data in enumerate(result):
                self.RoomTable.insertRow(row_num)
                for column_num,column_data in enumerate(row_data):
                    self.RoomTable.setItem(row_num, column_num,QTableWidgetItem(str(column_data)))
            cursor.close()
        except Exception as e:
            print(e)
