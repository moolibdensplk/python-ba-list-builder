from PyQt5.uic import loadUi
from PyQt5 import QtCore, QtGui, QtWidgets
# from faction_choice_dialog import *
from Internal.error_window import *
from Internal.boarding_actions_list import *
from Internal.error_window import *
from Internal.pdf_generator import *
import sys


class BAAListBuilderWindow(QtWidgets.QMainWindow):
    def __init__(self, faction):
        super(BAAListBuilderWindow, self).__init__()
        self.faction = faction
        self.list_saved = False
        self.list_validated = False
        loadUi("ui/listBuilderWindow.ui", self)
        self.faction_label_text = "Building Boarding Actions List for: %s" % self.faction
        self.factionLabel.setText(self.faction_label_text)
        # initialize a faction army list object
        self.faction_army_list = BoardingActionsList(self.faction)
        self.faction_selected_units = {}
        self.characters_in_the_list = 0
        self.battleline_in_the_list = 0
        self.fastattack_in_the_list = 0
        self.elite_in_the_list = 0
        self.krootmerc_in_the_list = 0
        self.other_in_the_list = 0
        self.dependency_check_result = False

        # Faction Unique limits
        if self.faction == "Tau Empire":
            self.duplicate_fastattck_units_allowed = False
            self.duplicate_krootemerc_units_allowed = False
            self.max_krootmerc_units = self.faction_army_list.faction_data['Boarding Actions Limits']['max_krootmerc_units']
            self.max_elite_units = self.faction_army_list.faction_data['Boarding Actions Limits']['max_elite_units']
            self.max_fastattack_units = self.faction_army_list.faction_data['Boarding Actions Limits']['max_fastattack_units']
        if faction == "Chaos Daemons":
            self.duplicate_characters_allowed = False
            self.max_other_units = self.faction_army_list.faction_data['Boarding Actions Limits']['max_other_units']
        # common limits
        self.max_characters = self.faction_army_list.faction_data['Boarding Actions Limits']['max_characters']
        self.max_battleline = self.faction_army_list.faction_data['Boarding Actions Limits']['max_battleline_units']

        # set the current points at 0
        self.faction_army_list.set_total_cost(0)

        self.available_units = self.faction_army_list.faction_data['Boarding Actions Units']
        # init the table unitListTableWidget()
        item = self.unitListTableWidget.horizontalHeaderItem(0)
        item.setText("Unit Name")
        item = self.unitListTableWidget.horizontalHeaderItem(1)
        item.setText("Unit Type")
        item = self.unitListTableWidget.horizontalHeaderItem(2)
        item.setText("Required Units")
        item = self.unitListTableWidget.horizontalHeaderItem(3)
        item.setText("Unit Size")
        item = self.unitListTableWidget.horizontalHeaderItem(4)
        item.setText("Unit Cost (Points)")

        # self.scroll_area = self.factionListScrollArea
        # populate the combobox with units and their cost
        for unit in self.available_units:
            # unit will be Str
            unit_name_with_cost = unit + ", Cost: " + str(self.available_units[unit]['unit_cost'])
            self.unitChoiceComboBox.addItem(unit_name_with_cost, self.available_units[unit])

        self.set_updated_status_text()

        def close_list():
            sys.exit(1)

        def clear_list():
            while self.unitListTableWidget.rowCount() > 0:
                    self.unitListTableWidget.removeRow(0)
            self.faction_selected_units.clear()
            self.faction_army_list.set_total_cost(0)
            self.set_updated_status_text()
            self.characters_in_the_list = 0

        def get_unit_size_step(unit_sizes):
            diff_list = []

            def check(list):
                return all(i == list[0] for i in list)

            for i in range(1, len(unit_sizes)):
                diff_list.append((unit_sizes[i] - unit_sizes[i - 1]))
            if check(diff_list) and len(diff_list) > 1:
                # return first element, as all will be the same !
                return diff_list[0]
            else:
                # if you cannot get a step, or the unit_sizes only contained ONE element
                # return ZERO
                return 0

        def add_unit_to_list():

            current_unit_obj = self.unitChoiceComboBox.currentData()
            current_unit_cost = current_unit_obj['unit_cost']
            current_unit_name = current_unit_obj['unit_name']
            current_unit_dependencies = current_unit_obj['requires']
            current_unit_sizes = current_unit_obj['unit_sizes']
            current_unit_type = current_unit_obj['unit_type']

            current_list_units = []



            # testing
            for iD in self.faction_selected_units.keys():
                current_list_units.append(self.faction_selected_units[iD]['unit_name'])
            # pas the requirements and a list of unit names already in the list
            # print("DEBUG: list of units in the list: %s" %str(current_list_units))
            # validate before adding

            if len(current_unit_dependencies) > 0:
                if len(current_unit_dependencies) > 1:
                    for i in range(0,len(current_unit_dependencies)):
                        self.dependency_check_result = self.faction_army_list.check_require(current_unit_dependencies[i], current_list_units)
                        if self.dependency_check_result:
                            self.dependency_check_result = True
                            break
                else:
                    self.dependency_check_result = self.faction_army_list.check_require(current_unit_dependencies[0], current_list_units)

            else:
                self.dependency_check_result = True


            if self.faction_army_list.check_if_unit_fits(current_unit_cost) :
                if self.dependency_check_result == False:
                    #error dependency
                    error_text = "ERROR: cannot add %s - this unit requires:\n %s" \
                                 " to be in your list." % (current_unit_name,current_unit_dependencies)
                    self.error_window = BAAErrorWindow(error_text, "err")
                    self.error_window.show()

                else:
                    # add size selector button (spin button) in the unit size column
                    selector_min = current_unit_sizes[0]
                    selector_max = current_unit_sizes[len(current_unit_sizes)-1]
                    selector_step = get_unit_size_step(current_unit_sizes)
                    unit_size_selector = QtWidgets.QSpinBox(self, value=selector_min, maximum=selector_max, minimum=selector_min, singleStep=selector_step)
                    # add handler to this instance fo selector button, to update cost based on selected size

                    def update_unit_cost():
                        # works as intended !
                        chosen_size = unit_size_selector.value()
                        # print("DEBUG: current index: %d" % current_unit_sizes.index(unit_size_selector.value()))
                        # below index will be the "incremented value
                        cost_multiplier = current_unit_sizes.index(chosen_size) + 1
                        new_cost = current_unit_cost * cost_multiplier
                        selected_table_row = self.unitListTableWidget.currentRow()
                        previous_cost_value = int(self.unitListTableWidget.item(selected_table_row,4).text())
                        # now update the value of the cell with the unit cost
                        self.unitListTableWidget.setItem(selected_table_row, 4,QtWidgets.QTableWidgetItem(str(new_cost)))
                        self.update_total_costs_when_spinning(previous_cost_value, new_cost, current_unit_cost)
                        self.set_updated_status_text()
                    unit_size_selector.valueChanged.connect(update_unit_cost)
                    row_count = self.unitListTableWidget.rowCount()
                    if current_unit_type == 'character' and self.characters_in_the_list >= self.max_characters:
                        error_text = "ERROR: cannot add %s - you already have a character in the list" % current_unit_name
                        self.error_window = BAAErrorWindow(error_text, "err")
                        self.error_window.show()
                    else:
                        #add this data to the row in table
                        self.unitListTableWidget.insertRow(row_count)
                        self.unitListTableWidget.setItem(row_count, 0, QtWidgets.QTableWidgetItem(current_unit_name))
                        self.unitListTableWidget.setItem(row_count, 1, QtWidgets.QTableWidgetItem(current_unit_type))
                        self.unitListTableWidget.setItem(row_count, 2,QtWidgets.QTableWidgetItem(str(current_unit_dependencies)))
                        # now add a spin button with the correct available unit sizes, which is defined above
                        self.unitListTableWidget.setCellWidget(row_count, 3, unit_size_selector)
                        self.unitListTableWidget.setItem(row_count, 4,QtWidgets.QTableWidgetItem(str(current_unit_cost)))
                        # add unit cost to totals ....
                        self.faction_army_list.set_total_cost(current_unit_cost + self.faction_army_list.get_total_cost())
                        self.set_updated_status_text()
                        # add unit to the faction list object:
                        # using row count as a UNIQUE ID.
                        self.faction_selected_units[row_count] = current_unit_obj
                        if current_unit_type == 'character':
                            self.characters_in_the_list = 1
            else:
                remaining_points = self.faction_army_list.max_points - self.faction_army_list.get_total_cost()
                error_text = "ERROR: cannot add unit - doesnt fit into remaining points: %d " % remaining_points
                self.error_window = BAAErrorWindow(error_text, "err")
                self.error_window.show()


        def remove_selected_unit():
            current_row = self.unitListTableWidget.currentRow()
            if current_row >= 0:
                unit_cost_to_deduct = self.unitListTableWidget.item(current_row,4).text()
                unit_type_to_remove = self.unitListTableWidget.item(current_row,1).text()
                self.unitListTableWidget.removeRow(current_row)
                self.faction_army_list.set_total_cost(self.faction_army_list.get_total_cost() - int(unit_cost_to_deduct))
                self.set_updated_status_text()
                self.faction_selected_units.pop(current_row)
                # regular dict.pop() does not solve it, as it does not update unique ID to match the row !
                updated_army_list = self.faction_army_list.remove_key(self.faction_selected_units, current_row)
                self.faction_selected_units = updated_army_list
                if unit_type_to_remove == 'character':
                    self.characters_in_the_list = 0


        def validate_list():

            list_validation_errors = {
                'size_validation': 'PASS',
                'character_limit': 'PASS',
                'battleline_limit': 'PASS'
            }
            character_limit_error = False

            list_size_validation = self.check_list_size_status()

            # selected_unit_names = []
            # for key in self.faction_selected_units.keys():
            #    selected_unit_names.append(self.faction_selected_units[key]['unit_name'])
            # print("DEBUG: selected units: ")
            # print(str(selected_unit_names))

            list_unit_types = []

            for id in self.faction_selected_units.keys():
                list_unit_types.append(self.faction_selected_units[id]['unit_type'])

            if list_size_validation:
                list_validation_errors['size_validation'] = 'PASS'
            else:
                list_validation_errors['size_validation'] = 'FAIL'

            if self.faction_army_list.check_max_characters(self.faction_selected_units, self.max_characters):
                list_validation_errors['character_limit'] = 'PASS'
            else:
                list_validation_errors['character_limit'] = 'FAIL'


            if self.faction_army_list.check_max_battleline(self.faction_selected_units, self.max_battleline):
                list_validation_errors['battleline_limit'] = 'PASS'
            else:
                list_validation_errors['battleline_limit'] = 'FAIL'

            # faction specific checks
            # TAU
            if self.faction == "Tau Empire":
                # check max elites
                if self.faction_army_list.check_max_elites(
                        self.faction_selected_units, self.max_elite_units):
                    list_validation_errors['elites_limit'] = 'PASS'
                else:
                    list_validation_errors['elites_limit'] = 'FAIL'

                # check max fast attacks
                if self.faction_army_list.check_max_fast_attack(
                        self.faction_selected_units, self.max_fastattack_units):
                    list_validation_errors['fastattack_limit'] = 'PASS'
                else:
                    list_validation_errors['fastattack_limit'] = 'FAIL'

                # check max kroot mercs
                if self.faction_army_list.check_max_krootmerc(
                        self.faction_selected_units, self.max_krootmerc_units):
                    list_validation_errors['krootmerc_limit'] = 'PASS'
                else:
                    list_validation_errors['krootmerc_limit'] = 'FAIL'

            if self.faction == "Chaos Daemons":
                # check max other
                if self.faction_army_list.check_max_other(
                        self.faction_selected_units, self.max_other_units):
                    list_validation_errors['other_limit'] = 'PASS'
                else:
                    list_validation_errors['other_limit'] = 'FAIL'


            #  Check DUPLICATE UNITS in general (takes care of every type that does not allow unit duplication)
            duplicated_unit_types = self.faction_army_list.check_duplicate_unit(self.faction_selected_units)
            if len(duplicated_unit_types) > 0:
                for utype in duplicated_unit_types:
                    dup_key_name = "%s_duplication" % utype
                    list_validation_errors[dup_key_name] = 'FAIL'

            print("DEBUG: validation object values")
            #print(list_validation_errors.values())
            if "FAIL" in list_validation_errors.values():
                failed_validations = []
                for k, val in list_validation_errors.items():
                    if "FAIL" in val:
                        failed_validations.append(k)
                print("DEBUG: failed validations: %s" % str(failed_validations))
                errors = "Your army list has failed to validate!\n" \
                         "Things that FAILED to validate:\n" \
                         "%s\n" % str(failed_validations)

                self.error_window = BAAErrorWindow(errors, "err")
                self.error_window.setWindowTitle("Boarding Actions App - List Validation")
                self.list_validated = False
                self.error_window.show()
            else:
                no_errors = "Your army list is valid !"
                self.error_window = BAAErrorWindow(no_errors, "ok")
                self.error_window.setWindowTitle("Boarding Actions App - List Validation")
                self.list_validated = True
                self.error_window.show()

        def save_list():
            list_object = self.faction_selected_units
            faction_name = self.faction
            faction_cost = self.faction_army_list.get_total_cost()
            print("DEBUG: trying to generate PDF file")
            print("DEBUG: checking validation ...")
            if self.list_validated:
                print("DEBUG: safe to output to PDF")
                print("DEBUG: army list: %s" % str(list_object))
                print("DEBUG: faction: %s" % faction_name)
                pdf_export = BAAPdfGenerator(faction_name, list_object, faction_cost)
                pdf_export.gerate_pdf_sheet()

            else:
                print("DEBUG: List NOT validated ! fix list validation errors !")
                self.error_window = BAAErrorWindow("LIST NOT VALIDATED.\n Fix all the validation errors first!", "err")
                self.error_window.setWindowTitle(
                    "Boarding Actions App - Save List Error")
                self.list_validated = False
                self.error_window.show()

        self.saveListButton.clicked.connect(save_list)
        self.closeListButton.clicked.connect(close_list)
        self.addToListButton.clicked.connect(add_unit_to_list)
        self.validateListButton.clicked.connect(validate_list)
        self.clearListButton.clicked.connect(clear_list)
        self.removeSelectedUnitButton.clicked.connect(remove_selected_unit)


    def check_list_size_status(self):
        if self.faction_army_list.get_total_cost() <= self.faction_army_list.max_points:
            return True
        else:
            return False

    def get_unit_names_from_current_list(self):
        list_of_unit_names_in_army_list = []
        for key in self.faction_selected_units.keys():
            list_of_unit_names_in_army_list.append(self.faction_selected_units[key]['unit_name'])
            return list_of_unit_names_in_army_list
    def set_updated_status_text(self):
        total_cost = self.faction_army_list.get_total_cost()
        max_cost =  self.faction_army_list.max_points
        self.status_text = "Total cost of selected units: %d / %d" % (total_cost, max_cost)

        if total_cost <= max_cost:
            color_effect_ok = QtWidgets.QGraphicsColorizeEffect()
            color_effect_ok.setColor(QtCore.Qt.darkGreen)

            self.listStatusBarLabel.setGraphicsEffect(color_effect_ok)
        else:
            color_effect_err = QtWidgets.QGraphicsColorizeEffect()
            color_effect_err.setColor(QtCore.Qt.darkRed)
            self.listStatusBarLabel.setGraphicsEffect(color_effect_err)
            self.listStatusBarLabel.setStyleSheet("font-weight: bold")
            self.status_text = "LIST ERROR: Total cost of selected units: %d / %d" % ( total_cost, max_cost)
        self.listStatusBarLabel.setText(self.status_text)

    def update_total_costs_when_spinning(self, unit_previous_cost, unit_new_cost, unit_base_cost):
        current_total_cost = self.faction_army_list.get_total_cost()
        if unit_new_cost > unit_previous_cost:
            current_total_cost = current_total_cost + unit_base_cost
            self.faction_army_list.set_total_cost(current_total_cost)
        elif unit_new_cost < unit_previous_cost:
            current_total_cost = current_total_cost - unit_base_cost
            self.faction_army_list.set_total_cost(current_total_cost)
        else:
            current_total_cost = current_total_cost
            self.faction_army_list.set_total_cost(current_total_cost)





