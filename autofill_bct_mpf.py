import io
import time
from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, A4

# Send e-cheque to:
# Bank Consortium Trust Company Limited - Client A/C - Master Clearing

employees = [
	("John Doe", "U248575(W)", "10/12/2015", [
		(100000000, "15/01/2017", "15/02/2017", 0)])
]


packet = io.BytesIO()
can = canvas.Canvas(packet, pagesize=landscape(A4))
can.setFont("Times-Roman", 8)

can.drawString(570, 523, "M-Labs Limited")
can.drawString(570, 523-13, "Sébastien Bourdeauducq")
can.drawString(570, 523-13*2, "59362721")
can.drawString(570, 523-13*3, "YYYYY")


def fillcell(x, y, text):
	cellx = [60, 159, 234, 304, 364, 421, 479, 534, 591, 645, 706, 760][x]
	celly = 415 - 13*y
	can.drawString(cellx, celly, text)

total = 0
for n, (name, hkid, startdate, contributions) in enumerate(employees):
	fillcell(0, 3*n, name)
	fillcell(1, 3*n, hkid)
	fillcell(2, 3*n, startdate)
	for m, (amount, period1, period2, surcharge) in enumerate(contributions):
		y = 3*n+m
		fillcell(4, y, str(amount))
		fillcell(5, y, period1)
		fillcell(6, y, period2)
		fillcell(7, y, str(min(1500, amount//20)))
		fillcell(9, y, str(min(1500, amount//20)))
		fillcell(11, y, str(surcharge))
		total += min(3000, amount//10) + surcharge
fillcell(11, 6*3+1, str(total))

can.drawString(430, 53, time.strftime("%d/%m/%Y"))
can.drawImage("signature.jpg", 40, 53, width=204*0.5, height=94*0.5)

can.save()


packet.seek(0)
new_pdf = PdfFileReader(packet)
existing_pdf = PdfFileReader(open("RS-M(REE).pdf", "rb"))
output = PdfFileWriter()
page = existing_pdf.getPage(0)
page.mergePage(new_pdf.getPage(0))
output.addPage(page)
outputStream = open(time.strftime("remittance_%Y_%m_%d.pdf"), "wb")
output.write(outputStream)
outputStream.close()
