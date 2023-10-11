import platform
import pdfkit
import jinja2

class BAAPdfGenerator(object):
    def __init__(self, faction_name, ba_list_object, total_cost):
        super(BAAPdfGenerator, self).__init__()
        self.faction_name = faction_name
        self.ba_list_object = ba_list_object
        self.faction_total_cost = total_cost

    def gerate_pdf_sheet(self):
        # template variables to be replaced by actual values:

        print("DEBUG: attempting to save PDF list for faction: %s" %self.faction_name)
        print("DEBUG: received the following BA list:")
        print(self.ba_list_object)

        if self.faction_name == "":
            self.faction_name = "UNKNOWN_FACTION"

        context = {
            "faction_name": self.faction_name,
            "points_spent": self.faction_total_cost,
            "boarding_action_list": self.ba_list_object
        }

        pdf_output_file_name = self.faction_name + '.pdf'

        sheet_template_folder = "html_templates/"
        template_loader = jinja2.FileSystemLoader(sheet_template_folder)
        template_env = jinja2.Environment(loader=template_loader)

        template = template_env.get_template('boarding_list_template.html')
        output_text = template.render(context)

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
        pdfkit.from_string(output_text, pdf_output_paths[os_platform], configuration=pdf_export_config)
        print("Saved the character sheet in: %s" % pdf_output_paths[os_platform])

