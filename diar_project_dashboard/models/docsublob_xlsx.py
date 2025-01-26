from odoo import models
class PartnerXlsx(models.AbstractModel):
    _name = 'report.diar_project_dashboard.docsublog'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, partners):
        for obj in partners:
            report_name = obj.name
            # One sheet by partner
            worksheet = workbook.add_worksheet(report_name[:31])
            bold = workbook.add_format({'bold': True})
            worksheet.write(0, 0, obj.name, bold)
            headings = ["Category", "Values"]
            data = [
                ["Apple", "Cherry", "Pecan"],
                [60, 30, 10],
            ]

            worksheet.write_row("A1", headings, bold)
            worksheet.write_column("A2", data[0])
            worksheet.write_column("B2", data[1])

            #######################################################################
            #
            # Create a new chart object.
            #
            chart1 = workbook.add_chart({"type": "pie"})

            # Configure the series. Note the use of the list syntax to define ranges:
            chart1.add_series(
                {
                    "name": "Pie sales data",
                    "categories": ["Sheet1", 1, 0, 3, 0],
                    "values": ["Sheet1", 1, 1, 3, 1],
                }
            )

            # Add a title.
            chart1.set_title({"name": "Popular Pie Types"})

            # Set an Excel chart style. Colors with white outline and shadow.
            chart1.set_style(10)

            # Insert the chart into the worksheet (with an offset).
            worksheet.insert_chart("C2", chart1, {"x_offset": 25, "y_offset": 10})

            #######################################################################
            #
            # Create a Pie chart with user defined segment colors.
            #

            # Create an example Pie chart like above.
            chart2 = workbook.add_chart({"type": "pie"})

            # Configure the series and add user defined segment colors.
            chart2.add_series(
                {
                    "name": "Pie sales data",
                    "categories": "=Sheet1!$A$2:$A$4",
                    "values": "=Sheet1!$B$2:$B$4",
                    "points": [
                        {"fill": {"color": "#5ABA10"}},
                        {"fill": {"color": "#FE110E"}},
                        {"fill": {"color": "#CA5C05"}},
                    ],
                }
            )

            # Add a title.
            chart2.set_title({"name": "Pie Chart with user defined colors"})

            # Insert the chart into the worksheet (with an offset).
            worksheet.insert_chart("C18", chart2, {"x_offset": 25, "y_offset": 10})

