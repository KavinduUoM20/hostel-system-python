from PyQt6.QtWidgets import QMainWindow, QDialog, QMessageBox, QTableWidgetItem, QStackedWidget, QWidget, QApplication
from PyQt6.QtCore import QTimer, QTime, QDate, Qt
from PyQt6.QtGui import QPalette, QColor
from MainForm import Ui_MainWindow
import DBConnection as DB


class HostelSystem(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()

        # self.EmployeeTable.setColumnWidth(0,100)
        # self.EmployeeTable.setColumnWidth(1,300)
        # self.EmployeeTable.setColumnWidth(2,100)
        # self.EmployeeTable.setColumnWidth(3,151)

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
        self.StudentIDText.textChanged.connect(self.studentNoEntered)

        # Student Page Functions -------------------------------------------------------------------------

        # Student: Register Student
        self.SaveStudentButton.clicked.connect(self.registerStudent)

        # Student: Search Student
        self.SearcStudentButton.clicked.connect(self.searchStudent)

        # Student: View Students
        self.viewStudets()

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

    def studentNoEntered(self):
        index = self.StudentIDText.text()
        self.StudentNameText.setText("Kavindu Senevirathne")
        count = 1
        palette = self.EntranceStatus.palette()
        if (count == 1):
            palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.green)
            self.EntranceStatus.setPalette(palette)
            self.EntranceStatus.setText("IN")
        else:
            palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.red)
            self.EntranceStatus.setPalette(palette)
            self.EntranceStatus.setText("OUT")

    # (3) Student Page Controller -------------------------------------------------------------------------
    # Student: Register Student
    def registerStudent(self):

        print("Register Student Clicked!")

    # Student: Search Student
    def searchStudent(self):
        print("Search Student Clicked!")

    # Student: View Students
    def viewStudets(self):
        print("View Students Clicked!")

    # Student: Load Students
    def LoadStudents(self):
        print("Load Students Selected!")

    # Student: Return Student Details
    def returnStudent(self):
        pass

    # (4) Employee Page Controller ----------------------------------------------------------------------
    # Employee: Register Employee
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
        except Exception as e:
            print(e)


    # Employee: Search Employee
    def searchEmployee(self):
        eid = self.EmployeeIDText_2.text()
        try:
            mydb = DB.DBConnection.getConnection()
            query1 = "SELECT name FROM employee WHERE employeeid ='" + eid + "';"
            query2 = "SELECT hostelid FROM employee_hostel WHERE employeeid = '"+eid+"' ORDER BY assigned DESC LIMIT 1;"
            #Here is an issue, because I want to print hostel name in the combo.
            cursor = mydb.cursor()
            cursor.execute(query1)
            result1 = cursor.fetchone()
            self.EmployeeNameText_2.setText(result1[0])
            self.EmployeeNameText_2.setReadOnly(True)
            cursor.execute(query2)
            result2 = cursor.fetchone()
            if result2 == None:
                self.EmployeeHostelCombo.setEnabled(True)
            else:
                self.EmployeeHostelCombo.setCurrentText(str(result2[0]))
        except Exception as e:
            print(e)

    # Employee: Enable Change Hostel
    def enableChangeHostel(self):
        self.EmployeeHostelCombo.setEnabled(True)
        self.LoadHostels()

    # Employee: Save Hostel Assignment
    def saveHostelAssignment(self):
        eid = self.EmployeeIDText_2.text()
        hid = self.EmployeeHostelCombo.currentText()
        try:
            mydb = DB.DBConnection.getConnection()
            query = "UPDATE `employee_hostel` SET `hostelid` = '"+hid+"', `assigned` = CURRENT_DATE WHERE `employeeid` = '"+eid+"';"
            cursor = mydb.cursor()
            cursor.execute(query)
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

    # Hostel: View Hostel
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

    # Hostel: Search Hostel
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

    # Hostel: Load Hostels
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

    # Hostel: Register Hostel
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

    # Hostel: View Rooms
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
