from reportlab.pdfgen import canvas
from os.path import join
from matplotlib import pyplot as plt
import cStringIO
from reportlab.lib.utils import ImageReader

def addImage(c, fig):
    imgdata = cStringIO.StringIO()
    fig.savefig(imgdata, format='png')
    imgdata.seek(0) 
    img = ImageReader(imgdata)
    c.drawImage(img,0,0)

folder = r".\PDF_test"


c = canvas.Canvas(join(folder,"test.pdf"))
fig = plt.figure()
plt.plot(range(3),range(3),'*')
plt.show()
addImage(c,fig)
fig2 = plt.figure()
plt.plot(range(3),range(0,5,2),'+r')
plt.show()
addImage(c,fig2)

c.save()

