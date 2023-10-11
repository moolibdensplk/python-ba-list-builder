import platform
import pdfkit
import jinja2

class BAAPdfGenerator(object):
    def __init__(self, faction_name, ba_list_object, total_cost, rule_mods):
        super(BAAPdfGenerator, self).__init__()
        self.faction_name = faction_name
        self.ba_list_object = ba_list_object
        self.faction_total_cost = total_cost
        self.rules_modifications = rule_mods

    def gerate_pdf_sheet(self):
        # template variables to be replaced by actual values:

        if self.faction_name == "":
            self.faction_name = "UNKNOWN_FACTION"

        context = {
            "faction_name": self.faction_name,
            "points_spent": self.faction_total_cost
        }

        pdf_output_file_name = self.faction_name + '.pdf'

        units_table_lines = []
        for k in self.ba_list_object.keys():
            unit_type_var = "unit_type_" + str(k)
            unit_name_var = "unit_name_" + str(k)
            unit_cost_var = "unit_cost_" + str(k)
            table_line = "<tr>\
            <td >{{" + unit_name_var + "}}</td>\
            <td >{{" + unit_type_var + "}}</td>\
            <td >{{" + unit_cost_var + "}} p.</td>\
            </tr>"
            units_table_lines.append(table_line)
            context[unit_name_var] = self.ba_list_object[k]['unit_name']
            context[unit_type_var] = self.ba_list_object[k]['unit_type']
            context[unit_cost_var] = self.ba_list_object[k]['unit_cost']

        table_lines_string = ''.join(map(str, units_table_lines))

        template_header = ("<h1>Boarding Actions (WH40K 10th ed)</h1>\
        <h2>Faction List</h2>\
        <br>\
        <p>Faction: {{faction_name}}</p>\
        <p>Points limit: 500</p>\
        <p>Points spent: {{points_spent}}</p><br>\
        <h3>Units included:</h3>\
        <table style=\"border-collapse: collapse; width: 60%;\" border=\"1\"><tr>\
        <td >Unit Name</td>\
        <td >Unit Type</td>\
        <td >Unit Cost</td>\
        </tr>")

        template_foot = "</table>"

        rules_html_header = ("<h3>Rule Modifications</h3></ul>")

        rule_html_lines = ""
        for rule_line in self.rules_modifications:
            rule_html_lines = rule_html_lines + "<li>" + rule_line + "</li>"

        rule_html_lines = rule_html_lines + "</ul>"
        rules_html = rules_html_header + rule_html_lines

        complete_html_template = template_header + table_lines_string + template_foot + rules_html

        jinja_template = jinja2.Template(complete_html_template)

        output_data_for_pdf = jinja_template.render(context)

        #now export the pdf

        wkhtmltopdf_paths_per_os = {
            "Darwin": "/usr/local/bin/wkhtmltopdf",
            "Linux": "/usr/local/bin/wkhtmltopdf",
            "Windows": r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
        }
        pdf_output_paths = {
            "Darwin": "boarding_actions_lists/" + pdf_output_file_name,
            "Linux": "boarding_actions_lists/" + pdf_output_file_name,
            "Windows": 'boarding_actions_lists\\'.strip() + pdf_output_file_name
        }
        os_platform = platform.system()

        wkhtmltopdf_binary = wkhtmltopdf_paths_per_os[os_platform]
        pdf_export_config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_binary)
        pdfkit.from_string(output_data_for_pdf, pdf_output_paths[os_platform], configuration=pdf_export_config)
        print("Saved the army list in: %s" % pdf_output_paths[os_platform])

