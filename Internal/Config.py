import json

"""
end bp list should look like:

leaders: {
     "leader 1" : { cost: x, enhancement: y }
     "leader 2" : { cost: x, enhancement: y }
     }
battle_line: {
    "BL unit 1" : { cost: x, unit size: y }
    "BL unit 2" : { cost: x, unit size: y }
    }
other: {
    "Other unit 1" : { cost: x, unit size: y }
}
monster: {
    "Monster 1" : { cost: x, unit size: y }
}
elite: {
    "Elite 1" : { cost: x, unit size: y }
}
"""

class BoardingPatrolRoster:
    def __init__(self, faction_name, detachment_name):
        self.boarding_patrol = {
            "faction_name": faction_name,
            "detachment_name": detachment_name,
            "leaders": [],
            "battle_line": [],
            "other": [],
            "elite": [],
            "monster": [],
            "total_cost": 0
        }
        self.total_cost = 0

    def add_leader(self, leader_data):
        self.boarding_patrol["leaders"].append(leader_data)

    def set_leader_enhancement(self,data, idx):
        self.boarding_patrol["leaders"][idx] = data
        # works !!!
        # print("DEBUG: new leader data: ", self.get_leader_data(idx))

    def set_total_cost(self, cost):
        self.total_cost = cost

    def add_unit(self, unit_data):
        if unit_data["unit_type"] == "battle_line":
            self.boarding_patrol["battle_line"].append(unit_data)
        elif unit_data["unit_type"] == "other":
            self.boarding_patrol["other"].append(unit_data)
        elif unit_data["unit_type"] == "monster":
            self.boarding_patrol["monster"].append(unit_data)
        elif unit_data["unit_type"] == "elite":
            self.boarding_patrol["elite"].append(unit_data)


    def remove_from_patrol(self,unit_data, unit_type):

        list_pos = self.get_unit_index(unit_type, unit_data)
        # print("DEBUG: unit type: ", unit_type)
        # print("DEBUG: list_pos: ", list_pos)
        # print("DEBUG: unit_data: ", unit_data)
        if unit_type == "leader":
            self.boarding_patrol["leaders"].pop(list_pos)
        if unit_type == "battle_line":
            self.boarding_patrol["battle_line"].pop(list_pos)
        if unit_type == "other":
            self.boarding_patrol["other"].pop(list_pos)
        if unit_type == "elite":
            self.boarding_patrol["elite"].pop(list_pos)
        if unit_type == "monster":
            self.boarding_patrol["monster"].pop(list_pos)

    def get_leader_index(self, leader_object):
        try:
            return self.boarding_patrol["leaders"].index(leader_object)
        except:
            return None

    def get_unit_index(self, unit_type, unit_data):
        try:
            if unit_type == "leader":
                return self.boarding_patrol["leaders"].index(unit_data)
            else:
                return self.boarding_patrol[unit_type].index(unit_data)
        except ValueError:
            return None

    def get_leader_data(self, idx):
        return self.boarding_patrol["leaders"][idx]



    def get_boarding_patrol(self):
        data = self.boarding_patrol
        leaders = data["leaders"]
        battle_line = data["battle_line"]
        other = data["other"]
        elite = data["elite"]
        monster = data["monster"]

        formatted_data = f"""
        <html>
        <title> Test HTML </title>
        <body>
        <H1> Boarding Patrol - {data['faction_name']} </H1>
        <H2> Detachment - {data['detachment_name']} </H2>
        <hr width=100%>
        <h3> Leaders: </h3>
        <ul>
        """
        for leader in leaders:
            formatted_data += f"""
            <li> {leader['leader_name']} , enhancement: {leader['leader_enhancement']}, cost: {leader['leader_cost']} </li>
            """
        formatted_data += f"""
        </ul>
        <hr width=100%>
        """
        # Battle Line
        formatted_data += f"""
        <h3> Battle Line: </h3>
        <ul>
        """
        for b_unit in battle_line:
            formatted_data += f"""
            <li> {b_unit['unit_name']}, unit size: {b_unit['unit_size']}, cost: {b_unit['unit_cost']}</li>
            """
        # Elite
        formatted_data += f"""
        </ul>
        <h3> Elite: </h3>
        <ul>
        """
        for e_unit in elite:
            formatted_data += f"""
                    <li> {e_unit['unit_name']}, unit size: {e_unit['unit_size']}, cost: {e_unit['unit_cost']}</li>
            """
        # Other
        formatted_data += f"""
        </ul>
        <h3> Other: </h3>
        <ul>
        """
        for o_unit in other:
            formatted_data += f"""
            <li> {o_unit['unit_name']}, unit size: {o_unit['unit_size']}, cost: {o_unit['unit_cost']}</li>
            """
        # Monster
        formatted_data += f"""
        </ul>
        <h3> Monster: </h3>
        <ul>
        """
        for m_unit in monster:
            formatted_data += f"""
            <li> {m_unit['unit_name']}, unit size: {m_unit['unit_size']}, cost: {m_unit['unit_cost']}</li>
            """
        # Total Cost
        data['total_cost'] = self.total_cost
        formatted_data += f"""
        </ul>
        <hr width=100%>
        <h3> TOTAL COST: {data['total_cost']} / 500 points </h3>
        </body>
        </html>
        """

        return formatted_data



factions = [ "Tau Empire", "Chaos Daemons"]
detachments = {
    "Tau Empire": {"Starfire Cadre": "Internal/Datafiles/Tau/starfire_cadre.json",
                   "Kroot Raiding Party": "Internal/Datafiles/Tau/kroot_raiding_party.json"
    },
    "Chaos Daemons": {
        "Rotten and Rusted":  "Internal/Datafiles/ChaosDaemons/rotten_and_rusted.json",
        "Pandemonic Inferno": "Internal/Datafiles/ChaosDaemons/pandemonic_inferno.json"
    }
}

core_rules_file = "Internal/Datafiles/Core/core_data.json"

def get_core_enhancements(file):
    try:
        with open(file, 'r') as data_file:
            c_enhancements = json.load(data_file)
            data_file.close()
    except IOError as e:
        raise RuntimeError(f'ERROR: Unable to open core enhancements data file: %s ', file)
    return c_enhancements

def get_detachment_data(faction_name, detachment_name):
    data_file_name = detachments[faction_name][detachment_name]
    try:
        with open(data_file_name, 'r') as data_file:
            json_data = json.load(data_file)
            data_file.close()

    except IOError as e:
        raise RuntimeError(f'ERROR: Unable to open data file. '
                           f'ERROR DETAILS: {e} ')
    # get core enhancements
    core_enhancements = get_core_enhancements(core_rules_file)
    for core_enhancement in core_enhancements['leader_enhancements']:
        json_data["leader_enhancements"].append(core_enhancement)
    return json_data

def get_detachment_names(faction_name):
    available_detachments = []
    for detachment_name,data_file in detachments[faction_name].items():
        available_detachments.append(detachment_name)
    return available_detachments

