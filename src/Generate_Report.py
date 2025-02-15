from fpdf import FPDF
import sqlite3

def generate_report():
    conn = sqlite3.connect("../data/osint_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ThreatData")
    results = cursor.fetchall()
    conn.close()

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="OSINT Investigation Report", ln=True, align="C")

    for row in results:
        pdf.multi_cell(0, 10, txt=f"Username: {row[1]} | Post: {row[2]}", border=0)

    pdf.output("../reports/OSINT_Report.pdf")
    print("Report saved as OSINT_Report.pdf")

generate_report()
