import sqlite3



from epsp_pdf import EpspPdf
import os
basedir = os.path.dirname(__file__)


def get_workerId_by_name(name, service):
    connection = sqlite3.connect("database/sqlite.db")
    cur = connection.cursor()
    sql_q = 'SELECT worker_id FROM health_worker where full_name=? and service=?'
    cur.execute(sql_q, (name, service))
    results = cur.fetchall()
    connection.close()
    return results


def get_workerService_by_name(name):
    connection = sqlite3.connect("database/sqlite.db")
    cur = connection.cursor()
    sql_q = 'SELECT service FROM health_worker where full_name=?'
    cur.execute(sql_q, (name,))
    results = cur.fetchall()
    connection.close()
    return results

def get_workers_count(service):
    connection = sqlite3.connect("database/sqlite.db")
    cur = connection.cursor()
    sql_q = 'SELECT count(*) FROM health_worker where service=?'
    cur.execute(sql_q, (service,))
    results = cur.fetchall()
    connection.close()
    return results


def get_guard_months_count(service):
    connection = sqlite3.connect("database/sqlite.db")
    cur = connection.cursor()
    sql_q = 'SELECT count(*) FROM guard_mounth where service=?'
    cur.execute(sql_q, (service,))
    results = cur.fetchall()
    connection.close()
    return results


def get_consultation_months_count(service):
    connection = sqlite3.connect("database/sqlite.db")
    cur = connection.cursor()
    sql_q = 'SELECT count(*) FROM consultaion_mounth where service=?'
    cur.execute(sql_q, (service,))
    results = cur.fetchall()
    connection.close()
    return results


def create_garde_page(service,  month, year, data, path):
    pdf = EpspPdf()
    pdf.alias_nb_pages()
    pdf.add_page()
    if service == "urgence":
        service = "URGENCE"
        grd_cons = "GARDE MEDECINS GENERALISTE"
    elif service == "dentiste":
        service = "CHIRURGIE DENTAIRE"
        grd_cons = "GARDE DES MEDECINS DENTISTES"
    elif service == "labo":
        service = "LABORATOIRE"
        grd_cons = "GARDE LABORATOIRE"

    elif service == "radio":
        service = "RADIOLOGIE"
        grd_cons = "GARDE RADIOLOGIE"

    elif service == "admin":
        service = "ADMINISTRATION"
        grd_cons = "GARDE ADMINISTRATIVE"

    elif service == "dentiste_inf":
        service = "CHIRURGIE DENTAIRE"
        grd_cons = "GARDE (DENTISTE INFIRMIERS)"

    elif service == "pharm":
        service = "PHARMACIE"
        grd_cons = "GARDE PHARMACIE"

    pdf.set_font("helvetica", size=12)
    pdf.cell(0, 10, "Service de: "+service, 0, 0, markdown=True)
    pdf.ln(10)

    pdf.set_font("helvetica", "B", size=17)
    pdf.cell(0, 10, "Planing de "+grd_cons, 1, 0, "C")
    pdf.ln(8)
    m = ""
    if month == 1:
        m = "janvier"
    elif month == 2:
        m = "février"
    elif month == 3:
        m = "mars"
    elif month == 4:
        m = "avril"
    elif month == 5:
        m = "mai"
    elif month == 6:
        m = "juin"
    elif month == 7:
        m = "juillet"
    elif month == 8:
        m = "août"
    elif month == 9:
        m = "septembre"
    elif month == 10:
        m = "octobre"
    elif month == 11:
        m = "novembre"
    elif month == 12:
        m = "décembre"
    pdf.set_font("helvetica", size=12)
    pdf.cell(0, 10, "Mois de "+m+"/"+str(year), 0, 0, "C")

    pdf.ln(8)

    pdf.set_font("Times", size=10)
    line_height = pdf.font_size * 1.9
    col_width = pdf.epw / 4
    fill = False
    for row in data:
        for datum in row:
            if datum == "Vendredi" or datum == "Samedi":
                fill = True

            if datum == "Jours" or datum == "Date" or datum == "De 08h:00 à 20h:00" or datum == "De 20h:00 à 08h:00" or datum == "De 08h:00 à 16h:00" or datum == "De 16h:00 à 20h:00" or datum == "De 16h:00 à 08h:00":
                pdf.set_font("Times", "B", size=10)
                pdf.multi_cell(col_width, line_height, datum, border=1, ln=3, max_line_height=pdf.font_size)
            else:
                if service == "CHIRURGIE DENTAIRE":
                    if datum == "Dr/ ":
                        datum = " "

                if datum == " ":
                    pdf.set_fill_color(215, 215, 215)
                    pdf.set_font("Times", size=10)
                    pdf.multi_cell(col_width, line_height, datum, border=1, ln=3, max_line_height=pdf.font_size,
                                   fill=True)
                else:
                    pdf.set_fill_color(224, 235, 255)
                    pdf.set_font("Times", size=10)
                    pdf.multi_cell(col_width, line_height, datum, border=1, ln=3, max_line_height=pdf.font_size,
                                   fill=fill)


        fill = False

        pdf.ln(line_height)

    pdf.ln(1)
    pdf.set_right_margin(30)
    pdf.set_left_margin(30)
    pdf.cell(0, 10, "Chef service", 0, 0, "L")
    pdf.cell(0, 10, "D.S.S", 0, 0, "R")

    pdf.output(path)


def create_recap_page(service, rec, month, year, data, chef, path):
    pdf = EpspPdf()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font("helvetica", size=12)
    pdf.cell(0, 10, "Service de: "+service, 0, 0, markdown=True)
    pdf.ln(10)

    pdf.set_font("helvetica", "B", size=17)
    pdf.cell(0, 10, "RECAP de " + rec, 1, 0, "C")
    pdf.ln(8)
    m = ""
    if month == 1:
        m = "janvier"
    elif month == 2:
        m = "février"
    elif month == 3:
        m = "mars"
    elif month == 4:
        m = "avril"
    elif month == 5:
        m = "mai"
    elif month == 6:
        m = "juin"
    elif month == 7:
        m = "juillet"
    elif month == 8:
        m = "août"
    elif month == 9:
        m = "septembre"
    elif month == 10:
        m = "octobre"
    elif month == 11:
        m = "novembre"
    elif month == 12:
        m = "décembre"
    pdf.set_font("helvetica", size=12)
    pdf.cell(0, 10, "Mois de "+m+"/"+str(year), 0, 0, "C")

    pdf.ln(8)

    pdf.set_font("Times", size=10)
    line_height = pdf.font_size * 1.9
    col_width = pdf.epw / 5  # distribute content evenly
    fill = False
    for row in data:
        for datum in row:
            if datum == " / " or datum == "Jours ouvrable" or datum == "Jours week-end" or datum == "Jours fériés" or datum == "Total" :
                pdf.set_font("Times", "B", size=10)
                pdf.multi_cell(col_width, line_height, datum, border=1, ln=3, max_line_height=pdf.font_size)
            else:
                pdf.set_fill_color(224, 235, 255)
                pdf.set_font("Times", size=10)

                pdf.multi_cell(col_width, line_height, str(datum), border=1, ln=3, max_line_height=pdf.font_size,
                                   fill=fill)

        fill = not fill

        pdf.ln(line_height)

    pdf.ln(2)
    pdf.set_right_margin(30)
    pdf.set_left_margin(30)

    if chef != "":
        pdf.cell(0, 10, "Recuperation de chef service (4 jours): " + chef, 0, 0, "L")

    pdf.output(path)


def create_garde_inf_page(service, grd_cons, month, year, data, groupes, path):
    pdf = EpspPdf()
    pdf.alias_nb_pages()
    pdf.add_page()

    if service == "inf":
        service = "URGENCE"
        grd_cons = "GARDE (GROUPES DES INFIRMIERS)"
    elif service == "surv":
        service = "URGENCE"
        grd_cons = "GARDE INFIRMIERS SURVEILLANTS"


    pdf.set_font("helvetica", size=12)
    pdf.cell(0, 10, "Service de: "+service, 0, 0, markdown=True)
    pdf.ln(10)

    pdf.set_font("helvetica", "B", size=17)
    pdf.cell(0, 10, "Planing de "+grd_cons, 1, 0, "C")
    pdf.ln(8)
    m = ""
    if month == 1:
        m = "janvier"
    elif month == 2:
        m = "février"
    elif month == 3:
        m = "mars"
    elif month == 4:
        m = "avril"
    elif month == 5:
        m = "mai"
    elif month == 6:
        m = "juin"
    elif month == 7:
        m = "juillet"
    elif month == 8:
        m = "août"
    elif month == 9:
        m = "septembre"
    elif month == 10:
        m = "octobre"
    elif month == 11:
        m = "novembre"
    elif month == 12:
        m = "décembre"
    pdf.set_font("helvetica", size=12)
    pdf.cell(0, 10, "Mois de "+m+"/"+str(year), 0, 0, "C")

    pdf.ln(8)

    pdf.set_font("Times", size=10)
    line_height = pdf.font_size * 1.7
    col_width = pdf.epw / 4
    fill = False
    for row in data:
        for datum in row:
            if datum == "Vendredi" or datum == "Samedi":
                fill = True

            if datum == "Jours" or datum == "Date" or datum == "De 08h:00 à 20h:00" or datum == "De 20h:00 à 08h:00" or datum == "De 08h:00 à 16h:00" or datum == "De 16h:00 à 20h:00" or datum == "De 16h:00 à 08h:00":
                pdf.set_font("Times", "B", size=10)
                pdf.multi_cell(col_width, line_height, datum, border=1, ln=3, max_line_height=pdf.font_size)
            else:
                if(datum == " "):
                    pdf.set_fill_color(215, 215, 215)
                    pdf.set_font("Times", size=10)
                    pdf.multi_cell(col_width, line_height, datum, border=1, ln=3, max_line_height=pdf.font_size,
                                   fill=True)
                else:
                    pdf.set_fill_color(224, 235, 255)
                    pdf.set_font("Times", size=10)
                    pdf.multi_cell(col_width, line_height, datum, border=1, ln=3, max_line_height=pdf.font_size,
                                   fill=fill)

        fill = False
        pdf.ln(line_height)

    for groupe in groupes:
        pdf.cell(0, 10, groupe, 0, 0, "L")
        pdf.ln(4)


    pdf.ln(20)
    pdf.set_right_margin(30)
    pdf.set_left_margin(30)
    pdf.cell(0, 10, "Chef service", 0, 0, "L")
    pdf.cell(0, 10, "D.S.S", 0, 0, "R")

    pdf.output(path)


def create_statistique_page(month, year, data, path):
    pdf = EpspPdf()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font("helvetica", size=12)
    pdf.cell(0, 10, "Service de: RADIOLOGIE", 0, 0, markdown=True)
    pdf.ln(10)

    pdf.set_font("helvetica", "B", size=17)
    pdf.cell(0, 10, "Statistique de service RADIOLOGIE", 1, 0, "C")
    pdf.ln(8)
    m = ""
    if month == 1:
        m = "janvier"
    elif month == 2:
        m = "février"
    elif month == 3:
        m = "mars"
    elif month == 4:
        m = "avril"
    elif month == 5:
        m = "mai"
    elif month == 6:
        m = "juin"
    elif month == 7:
        m = "juillet"
    elif month == 8:
        m = "août"
    elif month == 9:
        m = "septembre"
    elif month == 10:
        m = "octobre"
    elif month == 11:
        m = "novembre"
    elif month == 12:
        m = "décembre"
    pdf.set_font("helvetica", size=12)
    pdf.cell(0, 10, "Mois de "+m+"/"+str(year), 0, 0, "C")

    pdf.ln(8)

    pdf.set_font("Times", size=10)
    line_height = pdf.font_size * 1.9
    col_width = pdf.epw / 5  # distribute content evenly
    fill = False
    for row in data:
        for datum in row:
            if datum == "Examen" or datum == "Homme" or datum == "Famme" or datum == "Enfant" or datum == "Total":
                pdf.set_font("Times", "B", size=10)
                pdf.multi_cell(col_width, line_height, datum, border=1, ln=3, max_line_height=pdf.font_size)
            else:
                pdf.set_fill_color(224, 235, 255)
                pdf.set_font("Times", size=10)

                pdf.multi_cell(col_width, line_height, str(datum), border=1, ln=3, max_line_height=pdf.font_size,
                                   fill=fill)

        fill = not fill

        pdf.ln(line_height)

    pdf.ln(2)
    pdf.set_right_margin(30)
    pdf.set_left_margin(30)
    pdf.output(path)
