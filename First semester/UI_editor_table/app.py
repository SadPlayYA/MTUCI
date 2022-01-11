from PyQt5.QtWidgets import (QApplication, QWidget,
                             QTabWidget, QAbstractScrollArea,
                             QVBoxLayout, QHBoxLayout,
                             QTableWidget, QGroupBox,
                             QTableWidgetItem, QPushButton, QMessageBox,
                             QAbstractButton, QButtonGroup
                             )
from config import database, user, password, host
from PyQt5.QtGui import QIcon
import psycopg2
import sys



class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']
        self.day = {i: j for i, j in zip(self.days, range(len(self.days)))}
        self.day_ = {i: j for i, j in zip(range(len(self.days)), self.days)}
        self.join_btns = []

        self.setWindowTitle("Timetable-editor")
        self.resize(700, 700)
        self.setWindowIcon(QIcon('icon.jpg'))
        self.setStyleSheet('#icon.jpg')
        self.vbox = QVBoxLayout(self)
        self.tabs = QTabWidget(self)
        self.vbox.addWidget(self.tabs)

        self._connect_to_db()
        self._create_timetable_tab()
        self._create_teacher_tab()
        self._create_subjects_tab()


    # connect to the database
    def _connect_to_db(self):
        self.conn = psycopg2.connect(
            database=database,
            user=user,
            password=password,
            host=host,
        )
        self.cursor = self.conn.cursor()


    # create and fill in a tab for editing the schedule
    def _create_timetable_tab(self):
        self.timetable_tab = QWidget()
        self.tabs.addTab(self.timetable_tab, "Timetable")

        self.svbox = QVBoxLayout()
        self.shbox1 = QVBoxLayout()

        self.table_gboxes = []
        self.update_btns = []

        self.buttonGroup = QButtonGroup(self)
        self.buttonGroup.buttonClicked[QAbstractButton].connect(
            lambda button=QAbstractButton: self._change_day_from_table(button))

        self.delbuttonGroup = QButtonGroup(self)
        self.delbuttonGroup.buttonClicked[QAbstractButton].connect(
            lambda button=QAbstractButton: self._del_row_table(button))

        for i in self.days:
            sel_zap = QGroupBox(i)
            self.shbox1.addWidget(sel_zap)
            self.table_gboxes.append((sel_zap, i))

        for i in self.table_gboxes:
            self._create_table(i)

        self.svbox.addLayout(self.shbox1)
        self.shbox2 = QHBoxLayout()
        self.svbox.addLayout(self.shbox2)

        self.upd_btn = QPushButton("Update")
        self.upd_btn.clicked.connect(lambda: self._update_timetable())
        self.shbox1.addWidget(self.upd_btn)

        self.ins_btn = QPushButton("Add")
        self.ins_btn.clicked.connect(lambda: self._insert_row_table())
        self.shbox1.addWidget(self.ins_btn)

        self.timetable_tab.setLayout(self.svbox)


    # create a table for a specific day. All tables will be arranged vertically
    def _create_table(self, table_gbox):
        self.table = QTableWidget()
        self.table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Subject", "Place", "Time", "Week", "Change", "Delete"])

        self._update_table(table_gbox[1])

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.table)
        table_gbox[0].setLayout(self.mvbox)


    # table update handler
    def _update_table(self, table_gbox):
        sel_zap = "SELECT * FROM timetable WHERE day='{}' ORDER BY week".format(table_gbox)
        self.cursor.execute(sel_zap)
        records = list(self.cursor.fetchall())
        self.table.setRowCount(len(records))

        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Change " + '{} {}'.format(i, self.day[table_gbox]))
            delButton = QPushButton("Delete " + '{} {}'.format(i, self.day[table_gbox]))
            self.table.setItem(i, 0, QTableWidgetItem(str(r[2])))
            self.table.setItem(i, 1, QTableWidgetItem(str(r[3])))
            self.table.setItem(i, 2, QTableWidgetItem(str(r[4])))
            self.table.setItem(i, 3, QTableWidgetItem(str(r[5])))
            self.table.setCellWidget(i, 4, joinButton)
            self.table.setCellWidget(i, 5, delButton)

            self.buttonGroup.addButton(joinButton)
            self.delbuttonGroup.addButton(delButton)


    # update handler for a specific day
    def _change_day_from_table(self, button):
        print("Enter for change >> ")
        get_from_button = button.text().split()[1:]
        num_str = (int(get_from_button[0]), self.day_[int(get_from_button[1])])
        row = list()


        for box in self.table_gboxes:
            if box[1] == num_str[1]:
                self._create_table(box)
                for i in range(self.table.columnCount()):
                    try:
                        row.append(self.table.item(num_str[0], i).text())
                    except:
                        row.append(None)


        try:
            write_dann = list(input().split(', '))
            write_dann.append(num_str[1])
            write_dann.extend([_ for _ in row if _ is not None])
            sel_zap = "UPDATE timetable SET subject='{0}', room_numb='{1}', start_time='{2}', week='{3}' " \
                      "WHERE day='{4}' and subject='{5}' and room_numb='{6}' and start_time='{7}' and week='{8}'".format(
                write_dann[0], write_dann[1], write_dann[2], write_dann[3], write_dann[4], write_dann[5],
                write_dann[6], write_dann[7], write_dann[8])
            self.cursor.execute(sel_zap)
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Enter all fields")


    def _insert_row_table(self):
        try:
            print("Enter the data in order >> id, day, subject, room_numb, start_time, week")
            sel_zap = "INSERT INTO timetable (id, day, subject, room_numb, start_time, week) " \
                      "VALUES ('{}','{}','{}','{}','{}','{}')".format(*input().split(', '))
            self.cursor.execute(sel_zap)
            self.conn.commit()
            print("[Done!]")
        except:
            QMessageBox.about(self, "Error", "Insertion error")


    # function that deletes a line in the schedule for a specific day
    def _del_row_table(self, button):
        get_from_button = button.text().split()[1:]
        num_str = (int(get_from_button[0]), self.day_[int(get_from_button[1])])
        row = list()


        for box in self.table_gboxes:
            if box[1] == num_str[1]:
                self._create_table(box)
                for i in range(self.table.columnCount()):
                    try:
                        row.append(self.table.item(num_str[0], i).text())
                    except:
                        row.append(None)


        try:
            sel_zapros = "DELETE FROM timetable WHERE day='{}' and subject='{}' and room_numb='{}' " \
                         "and start_time='{}' and week='{}'".format(num_str[1], row[0], row[1], row[2],row[3])
            self.cursor.execute(sel_zapros)
            self.conn.commit()
            print("[Done!]")
        except:
            QMessageBox.about(self, "Error", "Deletion error")


    # function that creates a tab with teachers
    def _create_teacher_tab(self):
        self.teachers_tab = QWidget()
        self.tabs.addTab(self.teachers_tab, "Teachers")
        self.prepod_table = QTableWidget()
        self.prepod_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.prepod_box = QGroupBox()
        self.prepod_table.setColumnCount(2)
        self.prepod_table.setHorizontalHeaderLabels(["Teacher", 'Subject'])

        self.cursor.execute("SELECT * FROM teachers")
        records = self.cursor.fetchall()
        self.prepod_table.setRowCount(len(records))

        for i, r in enumerate(records):
            r = list(r)
            self.prepod_table.setItem(i, 0, QTableWidgetItem(str(r[1])))
            self.prepod_table.setItem(i, 1, QTableWidgetItem(str(r[2])))

        self.prepod_mvbox = QVBoxLayout()
        self.tupd_btn = QPushButton("Update")
        self.tupd_btn.clicked.connect(lambda: self._update_timetable())
        self.prepod_mvbox.addWidget(self.tupd_btn)
        self.prepod_mvbox.addWidget(self.prepod_table)
        self.teachers_tab.setLayout(self.prepod_mvbox)


    # function that creates a tab with items
    def _create_subjects_tab(self):
        self.subjects_tab = QWidget()
        self.tabs.addTab(self.subjects_tab, "Subjects")
        self.subj_table = QTableWidget()
        self.subj_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.subj_box = QGroupBox()
        self.subj_table.setColumnCount(1)
        self.subj_table.setHorizontalHeaderLabels(["Subjects"])
        self.cursor.execute("SELECT * FROM subjects")
        records = self.cursor.fetchall()
        self.subj_table.setRowCount(len(records))


        for i, r in enumerate(records):
            r = list(r)
            self.subj_table.setItem(i, 0, QTableWidgetItem(str(r[0])))


        self.subj_mvbox = QVBoxLayout()
        self.supd_btn = QPushButton("Update")
        self.supd_btn.clicked.connect(lambda: self._update_timetable())
        self.subj_mvbox.addWidget(self.supd_btn)
        self.subj_mvbox.addWidget(self.subj_table)
        self.subjects_tab.setLayout(self.subj_mvbox)


    # update schedule
    def _update_timetable(self):
        self._create_timetable_tab()
        self._create_teacher_tab()
        self._create_subjects_tab()

        for _ in range(3):
            self.tabs.removeTab(0)





app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec_())