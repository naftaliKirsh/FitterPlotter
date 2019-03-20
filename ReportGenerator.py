import cStringIO
from reportlab.pdfgen import canvas

class ReportGenerator:
    """Class for generating reports including raw data and fits plots
    """

    def __init__(self, data_plotter, file_name):
        """Creates a new report.
        Args:
            file_name: the file name
            data_plotter: a MultiDataPlotter containing the data to save
        """
        self.canvas = canvas.Canvas(file_name)
        self.data_plotter = data_plotter

    def save_report(self):
        """Saves the report"""
        
        self.canvas.save()

    def add_rawdata_plot(self, )

    