from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import json

def register_fonts():
    """Rejestruje czcionki używane w dokumencie PDF."""
    pdfmetrics.registerFont(TTFont('DejaVu', 'DejaVuSans.ttf'))
    pdfmetrics.registerFont(TTFont('DejaVu-Bold', 'DejaVuSans-Bold.ttf'))

def load_data(filename):
    """Wczytuje dane z pliku JSON i zwraca je jako słownik."""
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

def create_pdf(data, output_filename):
    """Tworzy dokument PDF z danymi."""
    c = canvas.Canvas(output_filename, pagesize=letter)
    width, height = letter

    x = 50
    y_start = height - 50
    y = y_start
    line_height = 20

    for key, value in data.items():
        if y < 70:
            c.showPage()
            y = y_start
        
        c.setFont("DejaVu-Bold", 15)
        c.drawString(x, y, key)
        y -= line_height

        c.setFont("DejaVu", 12)
        for v in value:
            if y < 50:
                c.showPage()
                c.setFont("DejaVu", 12)
                y = y_start
            c.drawString(x + 50, y, '— ' + v)
            y -= line_height
        y -= 10

    c.save()

def main():
    register_fonts()
    data = load_data('definitions.json')
    print(data)
    create_pdf(data, 'word_list.pdf')

if __name__ == "__main__":
    main()
