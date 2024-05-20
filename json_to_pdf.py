from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import json

# Otwieranie pliku JSON do odczytu
with open('definitions.json', 'r') as file:
    # Wczytywanie zawartości pliku JSON do słownika
    data_dict = json.load(file)

print(data_dict)

c = canvas.Canvas("word_list.pdf", pagesize=letter)
width, height = letter  # width i height to szerokość i wysokość strony

x = 50  # Margines z lewej strony
y_start = height - 50  # Początkowa wysokość od góry strony z pewnym marginesem
y = y_start
line_height = 20  # Wysokość linii (odstęp między słowami)

c.setFont("Courier", 12)

for key, value in data_dict.items():
    c.setFont("Courier", 12)
    if y < 50:
        c.showPage()
        y = y_start

    c.drawString(x, y, key)
    y -= line_height

    c.setFont("Times-Roman", 12)
    for v in value:
        if y < 50:
            c.showPage()
            y = y_start
        c.drawString(x + 50, y, '- ' + v)
        y -= line_height

c.save()
