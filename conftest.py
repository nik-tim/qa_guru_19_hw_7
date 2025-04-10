import os
import csv
import zipfile
import pytest
from fpdf import FPDF
from openpyxl import Workbook


@pytest.fixture(scope="session", autouse=True)
def generate_files_and_archive():
    os.makedirs("files", exist_ok=True)

    # CSV
    csv_data = [['a1', 'b1', 'c1'],
                ['a2', 'b2', 'c2'],
                ['a3', 'b3', 'c3']]
    with open("files/Test_CSV.csv", "w", newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerows(csv_data)

    # XLSX
    wb = Workbook()
    ws = wb.active
    for row in csv_data:
        ws.append(row)
    wb.save("files/Test_Excel.xlsx")

    # PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, "This is a test PDF document.")
    pdf.output("files/Test_Pdf.pdf")

    # Архивирование
    archive_path = "files/archive.zip"
    with zipfile.ZipFile(archive_path, 'w') as zf:
        for filename in ["Test_CSV.csv", "Test_Excel.xlsx", "Test_Pdf.pdf"]:
            zf.write(os.path.join("files", filename), arcname=filename)
