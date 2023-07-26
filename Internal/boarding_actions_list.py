import json

# needs to be global
faction_data_files = {
            "Tau Empire": "faction-data/tau_empire_points.json",
            "Chaos Daemons": "faction-data/chaos_daemons_points.json"
}

# needs to be global too
def get_factions():
    tmp_available_factions = []
    for faction in faction_data_files.keys():
        tmp_available_factions.append(faction)
    return tmp_available_factions


class BoardingActionsList(object):
    def __init__(self, faction_name):
        self.faction_name = faction_name
        self.available_units = []
        # this is going to be the json with selected unit objects
        self.selected_units = {}
        self.max_points = 500
        self.current_points = 0
        self.available_factions = []
        self.faction_data = self.load_faction_data()

    def load_faction_data(self):
        faction_file = faction_data_files[self.faction_name]
        try:
            with open(faction_file, 'r') as data_file:
                json_data = json.load(data_file)
                data_file.close()
                return json_data
        except IOError as e:
            raise RuntimeError(f'ERROR: Unable to open data file. '
                               f'ERROR DETAILS: {e} ')

    def check_if_unit_fits(self, unit_cost: int):
        eq = self.max_points - self.current_points
        if eq >= unit_cost:
            return True
        else:
            return False

    def check_require(self, req_unit_name, selected_units):
        # this does not work as expected
        #print("DEBUG: checking if %s is in %s" % (req_unit_name,
        #                                          str(selected_units)))
        # print("DEBUG: size of units_added: %s" % str(len(selected_units)))

        if req_unit_name in selected_units:
            #print("DEBUG: FOUND %s!! in %s.." % (req_unit_name,
            #                                     str(selected_units)))
            return True
        else:
            #print("ERROR: prerequisite unit: %s NOT PRESENT in the list."
            #      % req_unit_name)
            return False

    def check_max_characters(self, army_list, max_char):
        characters = 0
        for id in army_list.keys():
            if army_list[id]['unit_type'] == 'character':
                characters = characters + 1
        if characters > max_char:
            return False
        else:
            return True

    def check_max_battleline(self, army_list, max_bl):
        battleline = 0
        for id in army_list.keys():
            if army_list[id]['unit_type'] == 'battleline':
                battleline = battleline + 1
        if battleline > max_bl:
            return False
        else:
            return True

    def check_max_elites(self, army_list, max_elite):
        elites = 0
        for id in army_list.keys():
            if army_list[id]['unit_type'] == 'elite':
                elites = elites + 1
        if elites > max_elite:
            return False
        else:
            return True

    def check_max_fast_attack(self, army_list, max_fa):
        fastattacks = 0
        for id in army_list.keys():
            if army_list[id]['unit_type'] == 'fastattack':
                fastattacks = fastattacks + 1
        if fastattacks > max_fa:
            return False
        else:
            return True

    def check_max_krootmerc(self, army_list, max_kroot):
        krootmercs = 0
        for id in army_list.keys():
            if army_list[id]['unit_type'] == 'krootmerc':
                krootmercs = krootmercs + 1
        if krootmercs > max_kroot:
            return False
        else:
            return True

    def check_max_other(self, army_list, max_other):
        others = 0
        for id in army_list.keys():
            if army_list[id]['unit_type'] == 'krootmerc':
                others = others + 1
        if others > max_other:
            return False
        else:
            return True

    def check_duplicate_unit(self, army_list):
        temp_fa = []
        temp_oth = []
        temp_el = []
        temp_char = []
        temp_krootmerc = []
        duplicate_unit_types = []

        # fill the arrays with unit names
        for i in army_list.keys():
            if army_list[i]['unit_type'] == 'elite':
                temp_el.append(army_list[i]['unit_name'])
            elif army_list[i]['unit_type'] == 'fastattack':
                temp_fa.append(army_list[i]['unit_name'])
            elif army_list[i]['unit_type'] == 'other':
                temp_oth.append(army_list[i]['unit_name'])
            elif army_list[i]['unit_type'] == 'character':
                temp_char.append(army_list[i]['unit_name'])
            elif army_list[i]['unit_type'] == 'krootmerc':
                temp_krootmerc.append(army_list[i]['unit_name'])

        temp_el_dupes = [unit for unit in temp_el if temp_el.count(unit) > 1]
        temp_fa_dupes = [unit for unit in temp_fa if temp_fa.count(unit) > 1]
        temp_oth_dupes = [unit for unit in temp_oth
                          if temp_oth.count(unit) > 1]
        temp_char_dupes = [unit for unit in temp_char
                           if temp_char.count(unit) > 1]
        temp_kroot_dupes = [unit for unit in temp_krootmerc
                            if temp_krootmerc.count(unit) > 1]
        elite_duplicates = list(set(temp_el_dupes))
        fastattack_duplicates = list(set(temp_fa_dupes))
        other_duplicates = list(set(temp_oth_dupes))
        character_duplicates = list(set(temp_char_dupes))
        krootmerc_duplicates = list(set(temp_kroot_dupes))
        if len(elite_duplicates) > 0:
            duplicate_unit_types.append("elite")
        if len(fastattack_duplicates) > 0:
            duplicate_unit_types.append("fastattack")
        if len(other_duplicates) > 0:
            duplicate_unit_types.append("other")
        if len(character_duplicates) > 0:
            duplicate_unit_types.append("character")
        if len(krootmerc_duplicates) > 0:
            duplicate_unit_types.append("krootmerc")

        # print("DEBUG: duplicated units in types: %s" % duplicate_unit_types)
        return duplicate_unit_types

    def get_faction_rules(self):
        return self.faction_data['Boarding Actions Rules Modifications']

    def get_faction_limits(self):
        return self.faction_data['Boarding Actions Limits']

    def set_total_cost(self, faction_selected_cost):
        self.current_points = faction_selected_cost

    def get_total_cost(self):
        # print("CURRENT total cost = %d" %self.current_points)
        return self.current_points

    def remove_key(self, d, del_key):
        new_dict = {}
        for key, val in d.items():
            if key < del_key:
                new_dict[key] = val
            elif key > del_key:
                new_dict[key - 1] = val
            else:
                continue
        return new_dict

