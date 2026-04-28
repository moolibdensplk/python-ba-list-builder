import json
from typing_extensions import SupportsIndex

class BoardingPatrolRoster:
    def __init__(self, faction_name, detachment_name):
        self.leaders = []
        self.battle_line = []
        self.other = []
        self.elite = []
        self.monster = []
        self.leader_enhancement = ''
        self.boarding_patrol = {
            "faction_name": faction_name,
            "detachment_name": detachment_name,
            "leaders": self.leaders,
            "battle_line": [],
            "other": [],
            "elite": [],
            "monster": [],
            "total_cost": 0
        }
        self.total_cost = 0

    def add_leader(self, leader_data):
        self.leaders.append(leader_data)
        self.boarding_patrol["leaders"] = self.leaders

    def set_leader_enhancement(self,data, idx):
        self.leaders[idx]= data
        self.boarding_patrol["leaders"] = self.leaders[idx]

    def set_total_cost(self, cost):
        self.total_cost = cost

    def add_unit(self, unit_data):
        if unit_data["unit_type"] == "battle_line":
            self.battle_line.append(unit_data)
            self.boarding_patrol["battle_line"] = self.battle_line
        elif unit_data["unit_type"] == "other":
            self.other.append(unit_data)
            self.boarding_patrol["other"] = self.other
        elif unit_data["unit_type"] == "monster":
            self.monster.append(unit_data)
            self.boarding_patrol["monster"] = self.monster
        elif unit_data["unit_type"] == "elite":
            self.elite.append(unit_data)
            self.boarding_patrol["elite"] = self.elite

    def remove_from_patrol(self,unit_data, unit_type):
        list_pos = self.get_unit_index(unit_type, unit_data)
        if unit_type == "leader":
            self.leaders.pop(list_pos)
            self.boarding_patrol["leaders"] = self.leaders
        if unit_type == "battle_line":
            self.battle_line.pop(list_pos)
            self.boarding_patrol["battle_line"] = self.battle_line
        if unit_type == "other":
            self.other.pop(list_pos)
            self.boarding_patrol["other"] = self.other
        if unit_type == "elite":
            self.elite.pop(list_pos)
            self.boarding_patrol["elite"] = self.elite
        if unit_type == "monster":
            self.monster.pop(list_pos)
            self.boarding_patrol["monster"] = self.monster

    def get_unit_index(self, unit_type, unit_data) -> SupportsIndex:
        if unit_type == "leader":
            leader_index = self.leaders.index(unit_data)
            return leader_index
        if unit_type == "battle_line":
            battle_line_index = self.battle_line.index(unit_data)
            return battle_line_index
        if unit_type == "other":
            other_index = self.other.index(unit_data)
            return other_index
        if unit_type == "monster":
            monster_index = self.monster.index(unit_data)
            return monster_index
        if unit_type == "elite":
            elite_index = self.elite.index(unit_data)
            return elite_index
        else:
            return -1


    def get_leader_data(self, idx):
        leader_data = self.leaders[idx]
        return leader_data

    def get_boarding_patrol(self):
        data = self.boarding_patrol
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
        for leader in self.leaders:
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
        for b_unit in self.battle_line:
            formatted_data += f"""
            <li> {b_unit['unit_name']}, unit size: {b_unit['unit_size']}, cost: {b_unit['unit_cost']}</li>
            """
        # Elite
        formatted_data += f"""
        </ul>
        <h3> Elite: </h3>
        <ul>
        """
        for e_unit in self.elite:
            formatted_data += f"""
                    <li> {e_unit['unit_name']}, unit size: {e_unit['unit_size']}, cost: {e_unit['unit_cost']}</li>
            """
        # Other
        formatted_data += f"""
        </ul>
        <h3> Other: </h3>
        <ul>
        """
        for o_unit in self.other:
            formatted_data += f"""
            <li> {o_unit['unit_name']}, unit size: {o_unit['unit_size']}, cost: {o_unit['unit_cost']}</li>
            """
        # Monster
        formatted_data += f"""
        </ul>
        <h3> Monster: </h3>
        <ul>
        """
        for m_unit in self.monster:
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
    except IOError:
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
