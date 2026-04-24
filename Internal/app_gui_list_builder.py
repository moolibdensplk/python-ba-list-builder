from PyQt5.QtWidgets import QTableWidgetItem, QTableWidget, QWidget, QComboBox, QAbstractItemView, QFileDialog
import asyncio
from playwright.async_api import async_playwright
from Internal.Config import *
from Internal.app_gui_full_list_view import *


import sys
import os


class ListBuilderWindow(QtWidgets.QMainWindow):
    def __init__(self, faction_name,detachment_name):
        super(ListBuilderWindow, self).__init__()
        loadUi("Internal/listBuilderWindow.ui", self)
        self.faction_name = faction_name
        self.detachment_name = detachment_name
        # initiate an empty boarding patrol "list" (not to confuse with python list !) object
        self.boarding_patrol_roster = BoardingPatrolRoster(self.faction_name, self.detachment_name)
        self.detachment_data = get_detachment_data(self.faction_name, self.detachment_name)
        self.enhancements_list = self.detachment_data["leader_enhancements"]
        self.total_cost = 0
        self.max_cost = 500
        self.setupUi(self)
        self.show()

    def get_max_leaders(self):
        max_leaders = self.detachment_data["mustering_rules"]["max_leaders"]
        return max_leaders

    def is_duplicate_leader_allowed(self):
        is_allowed = self.detachment_data["mustering_rules"]["is_duplicate_leader_allowed"]
        return is_allowed

    def check_if_leader_present_in_table(self, leader_name):
        rows = self.tableLeaders.rowCount()
        if rows > 0:
            for row in range(0, rows):
                if self.tableLeaders.item(row, 1).text() == leader_name:
                    return True
            return False
        else:
            return False

    def update_cost_add(self, unit_cost):
        self.total_cost += unit_cost
        self.currentCostLabel.setText(str(self.total_cost))

    def update_cost_sub(self, unit_cost):
        self.total_cost -= unit_cost
        self.currentCostLabel.setText(str(self.total_cost))

    def check_cost_fit(self,unit_cost):
        if self.total_cost + unit_cost <= self.max_cost:
            return True
        else:
            return False


    def check_max_leaders(self):
        if self.tableLeaders.rowCount() < self.get_max_leaders():
            return True
        else:
            return False

    def check_selected_enhancements(self):
        selected_enhancements = []
        max_rows = self.tableLeaders.rowCount()
        current_row = self.tableLeaders.currentRow()

        for row in range(0, max_rows):
            enh_widget = self.tableLeaders.cellWidget(row, 2)
            current_leader_name = self.tableLeaders.item(row, 1).text()
            current_leader_enhancement = enh_widget.currentText()
            current_leader_cost = int(self.tableLeaders.item(row, 3).text())

            if enh_widget.currentText() in selected_enhancements:
                # set both widgets red ??
                for x in range(0, max_rows):
                    w =  self.tableLeaders.cellWidget(x, 2)
                    w.setStyleSheet("color: red")
                print("DEBUG: ENHANCEMENT DUPLICATION DETECTED! Not adding to the list ! Change one of the enhancements!")
                # add a custom error popup later..... (instead of the print above)
            else:
                selected_enhancements.append(enh_widget.currentText())
                enh_widget.setStyleSheet("color: green")
            l_data = {'leader_name': current_leader_name, 'leader_enhancement': current_leader_enhancement,
                      'leader_cost': current_leader_cost}
            self.boarding_patrol_roster.set_leader_enhancement(l_data, row)

    def check_battleline_count(self, unit_name):
        max_unique_battleline_units = self.detachment_data["mustering_rules"]["max_unique_battleline_units"]
        row_count = self.tableUnits.rowCount()
        unit_type = self.detachment_data["units"][unit_name]["unit_type"]
        bl_count = 0

        bl_units = []
        for row in range(0, row_count):
            if self.tableUnits.item(row, 2).text() == unit_type:
                bl_count += 1
                bl_units.append(self.tableUnits.item(row, 1).text())

        if bl_units.count(unit_name) < max_unique_battleline_units:
            return True
        else:
            return False

    def check_other_count(self,unit_name):
        row_count = self.tableUnits.rowCount()
        max_others = self.detachment_data["mustering_rules"]["max_other_units"]
        max_unique_others = self.detachment_data["mustering_rules"]["max_unique_other_units"]
        unit_type = self.detachment_data["units"][unit_name]["unit_type"]
        other_unit_count = 0
        unique_others = []

        for row in range(0, row_count):
            if self.tableUnits.item(row, 2).text() == unit_type:
                other_unit_count += 1
                unique_others.append(self.tableUnits.item(row, 1).text())
        if other_unit_count < max_others:
            if unique_others.count(unit_name) < max_unique_others :
                return True
            else:
                return False
        else:
            return False


    def check_monster_count(self, unit_name):
        max_monsters = self.detachment_data["mustering_rules"]["max_monster_units"]
        unit_type = self.detachment_data["units"][unit_name]["unit_type"]
        row_count = self.tableUnits.rowCount()

        monsters = []
        for row in range(0, row_count):
            if self.tableUnits.item(row, 2).text() == unit_type:
                monsters.append(self.tableUnits.item(row, 1).text())
        if len(monsters) < max_monsters:
            if monsters.count(unit_name) < max_monsters:
                return True
            else:
                return False
        else:
            return False

    def check_elite_count(self, unit_name):
        max_elites = self.detachment_data["mustering_rules"]["max_other_units"]
        max_unique_elites = self.detachment_data["mustering_rules"]["max_elite_units"]
        return True


    def close_button_clicked(self):
        sys.exit(0)

    def add_unit_to_table(self, unit_data):
        # insert data at the right row:
        self.tableUnits.insertRow(self.tableUnits.rowCount())
        l_id = QTableWidgetItem(str(self.tableUnits.rowCount() - 1))
        name = QTableWidgetItem(unit_data["unit_name"])
        u_type = QTableWidgetItem(unit_data["unit_type"])
        cost = QTableWidgetItem(str(unit_data["unit_cost"]))
        self.tableUnits.setItem(self.tableUnits.rowCount() - 1, 0, l_id)
        self.tableUnits.setItem(self.tableUnits.rowCount() - 1, 1, name)
        self.tableUnits.setItem(self.tableUnits.rowCount() - 1, 2, u_type)
        self.tableUnits.setItem(self.tableUnits.rowCount() - 1, 3, cost)

    def add_unit_pressed(self):
        unit_name = str(self.unitListBox.currentText())
        unit_cost = self.detachment_data["units"][unit_name]["unit_cost"]
        unit_type = self.detachment_data["units"][unit_name]["unit_type"]
        unit_size = self.detachment_data["units"][unit_name]["unit_size"]
        unit_data = {"unit_name": unit_name, "unit_type": unit_type,"unit_cost": unit_cost, "unit_size": unit_size}
        # print("DEBUG: Unit DATA", unit_data)
        # checks for Monster units
        if self.check_cost_fit(unit_cost):
            # monster unit checks
            if self.detachment_data["units"][unit_name]["unit_type"] == "monster":
                if self.check_monster_count(unit_name):
                    self.add_unit_to_table(unit_data)
                    self.boarding_patrol_roster.add_unit(unit_data)
                    self.update_cost_add(unit_cost)
            # checks for Elite units
            elif self.detachment_data["units"][unit_name]["unit_type"] == "elite":
                if self.check_elite_count(unit_name):
                    print("DEBUG: check elite unit = True")
                    self.add_unit_to_table(unit_data)
                    self.boarding_patrol_roster.add_unit(unit_data)
                    self.update_cost_add(unit_cost)
            # checks for Other units
            elif self.detachment_data["units"][unit_name]["unit_type"] == "other":
                print("DEBUG: UNIT TYPE: OTHER ....")
                if self.check_other_count(unit_name):
                    self.add_unit_to_table(unit_data)
                    self.boarding_patrol_roster.add_unit(unit_data)
                    self.update_cost_add(unit_cost)
            # checks for Battleline units
            elif self.detachment_data["units"][unit_name]["unit_type"] == "battle_line":
                if self.check_battleline_count(unit_name):
                    self.add_unit_to_table(unit_data)
                    self.boarding_patrol_roster.add_unit(unit_data)
                    self.update_cost_add(unit_cost)

    def get_selected_enhancement(self, row):
        w = self.tableLeaders.cellWidget(row, 3)
        enhancement = w.currentText()
        return enhancement

    def add_leader_to_table(self, leader_data):
        # insert data at the right row:
        self.tableLeaders.insertRow(self.tableLeaders.rowCount())
        l_id = QTableWidgetItem(str(self.tableLeaders.rowCount() - 1))
        name = QTableWidgetItem(leader_data["leader_name"])
        enhancements_box = QComboBox()
        enhancements_box.setPlaceholderText("No Enhancement")
        enhancements_box.addItems(self.enhancements_list)

        cost = QTableWidgetItem(str(leader_data["leader_cost"]))

        self.tableLeaders.setItem(self.tableLeaders.rowCount() - 1, 0, l_id)
        self.tableLeaders.setItem(self.tableLeaders.rowCount() - 1, 1, name)
        self.tableLeaders.setCellWidget(self.tableLeaders.rowCount() - 1, 2, enhancements_box)
        enh_widget = self.tableLeaders.cellWidget(self.tableLeaders.rowCount() - 1, 2)
        # the below works
        enh_widget.currentIndexChanged.connect(self.check_selected_enhancements)
        self.tableLeaders.setItem(self.tableLeaders.rowCount() - 1, 3, cost)


    def add_leader_pressed(self):
        selected_leader_name = str(self.leaderListBox.currentText())
        leader_data = {"leader_name": selected_leader_name,
                       "leader_enhancement": self.detachment_data["leaders"][selected_leader_name]["leader_enhancement"],
                       "leader_cost": self.detachment_data["leaders"][selected_leader_name]["unit_cost"],}
        cost_check = self.detachment_data["leaders"][selected_leader_name]["unit_cost"]
        if (self.check_max_leaders() and not self.check_if_leader_present_in_table(selected_leader_name)
                and self.check_cost_fit(cost_check)):
                self.add_leader_to_table(leader_data)
                self.boarding_patrol_roster.add_leader(leader_data)
                self.update_cost_add(leader_data["leader_cost"])

                #print("DEBUG: selected leader data: ", leader_data)


    def remove_unit_pressed(self):
        total_rows = self.tableUnits.rowCount()
        if total_rows > 0:
            selected_row = self.tableUnits.currentRow()
            if selected_row < 0:
                # happens only when deleting one unit.
                # after adding a second unit, and deleting without selecting anything,
                # it chooses row ZERO: 0
                selected_row = total_rows - 1
            unit_name = self.tableUnits.item(selected_row, 1).text()
            unit_type = self.tableUnits.item(selected_row, 2).text()
            unit_cost = int(self.tableUnits.item(selected_row, 3).text())
            unit_size = int(self.detachment_data["units"][unit_name]["unit_size"])
            self.tableUnits.removeRow(selected_row)
            unit_data_to_delete = {'unit_name': unit_name, 'unit_type': unit_type, 'unit_cost': unit_cost,
                                   'unit_size': unit_size}
            self.boarding_patrol_roster.remove_from_patrol(unit_data_to_delete, unit_type)
            self.update_cost_sub(unit_cost)


    def remove_leader_pressed(self):
        total_rows = self.tableLeaders.rowCount()

        if total_rows > 0:
            selected_row = self.tableLeaders.currentRow()
            # if you don't select a leader, always choose the last one to remove
            if selected_row < 0:
                # happens only when deleting one leader.
                # after adding a second leader, and deleting without selecting anything,
                # it chooses row ZERO: 0
                selected_row = total_rows - 1
            leader_name = self.tableLeaders.item(selected_row, 1).text()
            # use .currentText() because the widget in that cell is a dropdown list (comboBox object)
            leader_enh = self.tableLeaders.cellWidget(selected_row, 2).currentText()
            leader_cost = int(self.tableLeaders.item(selected_row, 3).text())
            leader_data_to_delete = {'leader_name': leader_name, 'leader_enhancement': leader_enh , 'leader_cost': leader_cost,
                                    }
            self.boarding_patrol_roster.remove_from_patrol(leader_data_to_delete, "leader")
            self.tableLeaders.removeRow(selected_row)
            self.update_cost_sub(int(leader_cost))

    def view_full_list(self):

        # print("DEBUG: FULL LIST VIEW:")
        self.boarding_patrol_roster.set_total_cost(self.total_cost)
        # print(self.boarding_patrol_roster.get_boarding_patrol())

        self.ui = BoardingPatrolViewWindow(self.boarding_patrol_roster.get_boarding_patrol())

    async def html_to_pdf(self, html_content, output_path):
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.set_content(html_content)
            await page.pdf(path=output_path)
            await browser.close()

    def getSaveFileName(self):
        file_filter = 'PDF Files (*.pdf);;'
        response = QFileDialog.getSaveFileName(
        parent = self,
        caption = 'Select the file to save',
        directory = 'PDF File.pdf',
        filter = file_filter,
        initialFilter = 'PDF File (*.pdf)'
        )
        print(response)
        return response[0]


    def save_list_button_clicked(self):
        self.boarding_patrol_roster.set_total_cost(self.total_cost)
        ba_list = self.boarding_patrol_roster.get_boarding_patrol()
        save_file_name = self.getSaveFileName()
        asyncio.run(self.html_to_pdf(ba_list, save_file_name))

    def setupUi(self, ListBuilderWindow):
        ListBuilderWindow.setObjectName("ListBuilderWindow")
        QtCore.QMetaObject.connectSlotsByName(ListBuilderWindow)
        # set labels
        self.currentFactionLabel.setText(self.faction_name)
        self.currentDetachmentLabel.setText(self.detachment_name)
        # set the table 1st column width ("id") to be narrow
        # width: 500
        self.tableLeaders.setColumnWidth(0,20)
        self.tableLeaders.setColumnWidth(1,200)
        self.tableLeaders.setColumnWidth(2,230)
        self.tableLeaders.setColumnWidth(3,50)
        # self.tableLeaders.setRowCount(2)
        self.tableUnits.setColumnWidth(0,20)
        self.tableUnits.setColumnWidth(1,200)
        self.tableUnits.setColumnWidth(2,230)
        self.tableUnits.setColumnWidth(3,50)

        # set both tables read only - disabling manual editing
        self.tableLeaders.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableUnits.setEditTriggers(QAbstractItemView.NoEditTriggers)


        # populate the dropdowns
        self.leaderListBox.addItems(list(self.detachment_data["leaders"].keys()))
        self.unitListBox.addItems(list(self.detachment_data["units"].keys()))

        # button connectors
        self.addLeaderButton.clicked.connect(self.add_leader_pressed)
        self.addUnitButton.clicked.connect(self.add_unit_pressed)
        self.removeLeaderButton.clicked.connect(self.remove_leader_pressed)
        self.removeUnitButton.clicked.connect(self.remove_unit_pressed)
        self.closeAppButton.clicked.connect(self.close_button_clicked)
        self.viewFullListButton.clicked.connect(self.view_full_list)
        self.saveListButton.clicked.connect(self.save_list_button_clicked)


