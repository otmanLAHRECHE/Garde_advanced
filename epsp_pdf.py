
from fpdf import FPDF


class EpspPdf(FPDF):
    def header(self):
        self.set_margins(10, 0, 10)
        self.set_auto_page_break(auto=False)
        self.set_font("helvetica", "B", 12)
        # Moving cursor to the right:

        self.cell(80)
        self.cell(30, 10, "MINISTERE DE LA SANTE", 0, 0, "C")

        self.ln(5)

        self.cell(80)
        self.set_font("helvetica", "B", size=12)
        self.cell(30, 10, "DIRECTION DE LA SANTE ET DE LA POPULATION DE LA WILAYA DE DJANET", 0, 0, "C")

        self.ln(12)
        self.set_font("helvetica", "B", size=10)
        self.cell(0, 10, "ETABLISSEMENT PUBLIC DE SANTE DE PROXIMITE DE DJANET", 0, 0)

        self.ln(5)



    def footer(self):
        # Position cursor at 1.5 cm from bottom:
        self.set_y(-15)
        # Setting font: helvetica italic 8
        #self.set_font("helvetica", "I", 8)
        # Printing page number:
        #self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", 0, 0, "C")


# Instantiation of inherited class
