from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
#from reportlab.rl_config import defaultPageSize
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table
from reportlab.platypus import TableStyle
from reportlab.lib import colors
from reportlab.lib.units import inch


PAGE_HEIGHT=letter[1]; PAGE_WIDTH=letter[0]
styles = getSampleStyleSheet()

pageinfo = " |  StoreSoft"


def myFirstPage(canvas, doc, nota, salidas):
    canvas
    canvas.saveState()
    #Cabecera ------------------------------------
    nombre = "TIENDA DON LUIS"
    rfc = "XXXX010101"
    calle ="Av. Plan de San Luis"
    ext ="1820"
    inte = " "
    col = "Chapultepec Country"
    cp = "44620"
    ciudad = "Guadalajara"
    estado = "Jalisco"
    pais = "México"
    canvas.setStrokeColorRGB(.6588,0,.0627)
    canvas.setFillColorRGB(.6588,0,.0627)
    canvas.rect(0,PAGE_HEIGHT-70,PAGE_WIDTH, 120,fill=True,stroke=False)

    canvas.drawImage("logo.png", PAGE_WIDTH-170, PAGE_HEIGHT-40, width=120, height=60)

    canvas.setFillColorRGB(1,1,1)
    canvas.setFont("Helvetica", 12)
    cabecera = canvas.beginText(50, PAGE_HEIGHT+10)
    cabecera.textLines("%s\n%s\nAv. %s No.%s Int.%s\nCol. %s, C.P. %s\n%s, %s, %s." % (nombre, rfc, calle, ext, inte, col, cp, ciudad, estado, pais))
    canvas.drawText(cabecera)
    #Fin de cabecera ---------------------------------
    #Info Cliente ------------------------------------
    nombre = "ABDIEL OTONIEL FLORES GONZALEZ"
    rfc = "XXXX010101"
    calle ="Av. Plan de San Luis"
    ext ="1820"
    inte = " "
    col = "Chapultepec Country"
    cp = "44620"
    ciudad = "Guadalajara"
    estado = "Jalisco"
    pais = "México"
    codigoNota = "Nota-1"
    fechaHora = "13/04/2020 13:12:32"
    canvas.setFillColorRGB(.2196,.2196,.2196)
    canvas.setFont("Helvetica", 12)
    cliente = canvas.beginText(50, 630+70)
    cliente.textLines("%s\n%s\nAv. %s No.%s Int.%s\nCol. %s, C.P. %s\n%s, %s, %s." % (nombre, rfc, calle, ext, inte, col, cp, ciudad, estado, pais))
    canvas.drawText(cliente)

    canvas.setFillColorRGB(.6588,0,.0627)
    canvas.setFont("Helvetica-Bold", 15)
    canvas.drawRightString(PAGE_WIDTH-50,630+70,"%s" %(codigoNota))
    canvas.setFillColorRGB(.2196,.2196,.2196)
    canvas.setFont("Helvetica-Bold", 12)
    canvas.drawRightString(PAGE_WIDTH-50,590+70,"Fecha y Hora:")
    canvas.setFont("Helvetica", 12)
    canvas.drawRightString(PAGE_WIDTH-50,575+70,"%s" % (fechaHora))
    #-------------------------------------------------
    #Pie de pagina -----------------------------------
    canvas.setFont('Helvetica',9)
    canvas.drawCentredString(PAGE_WIDTH/2, 50, "Página %d %s" % (doc.page, pageinfo))
    canvas.setFillColorRGB(.6588,0,.0627)
    canvas.rect(0,0,PAGE_WIDTH, 20,fill=True,stroke=False)
    #-------------------------------------------------
    canvas.restoreState()

def myLaterPages(canvas, doc, nota, salidas):
    canvas.saveState()
    #Cabecera ------------------------------------
    canvas.setFillColorRGB(.6588,0,.0627)
    canvas.rect(0,PAGE_HEIGHT+30,PAGE_WIDTH, 20,fill=True,stroke=False)
    #Fin de cabecera ---------------------------------
    #Pie de pagina -----------------------------------
    canvas.setFillColorRGB(.2196,.2196,.2196)
    canvas.setFont('Helvetica',9)
    canvas.drawCentredString(PAGE_WIDTH/2, 50, "Página %d %s" % (doc.page, pageinfo))
    canvas.setFillColorRGB(.6588,0,.0627)
    canvas.rect(0,0,PAGE_WIDTH, 20,fill=True,stroke=False)
    #-------------------------------------------------
    canvas.restoreState()

def hacerTabla():
    datos = [["CANTIDAD","                       NOMBRE                       ","  P/U  ","TOTAL"],
                ["1","Producto2","750","1500"],
                ["1","Producto3","750","1500"],
                ["1","Producto4","750","1500"],
                ["1","Producto5","750","1500"],
                ["1","Producto6","750","1500"],
                ["1","Producto7","750","1500"],
                ["1","Producto8","750","1500"],
                ["1","Producto9","750","1500"],
                ["1","Producto10","750","1500"],
                ["1","Producto11","750","1500"],
                ["1","Producto12","750","1500"],
                ["1","Producto13","750","1500"],
                ["1","Producto14","750","1500"],
                ["1","Producto15","750","1500"],
                ["1","Producto16","750","1500"],
                ["1","Producto17","750","1500"],
                ["1","Producto18","750","1500"],
                ["1","Producto19","750","1500"],
                ["1","Producto20","750","1500"],
                ["1","Producto21","750","1500"],
                ["1","Producto22","750","1500"],
                ["1","Producto23","750","1500"],
                ["1","Producto24","750","1500"],
                ["1","Producto25","750","1500"],
                ["1","Producto26","750","1500"],
                ["1","Producto27","750","1500"],
                ["1","Producto28","750","1500"],
                ["1","Producto28","750","1500"],
                ["1","Producto28","750","1500"],
                ["1","Producto28","750","1500"],
                ["1","Producto28","750","1500"],
                ["1","Producto28","750","1500"],
                ["1","Producto28","750","1500"],
                ["1","Producto28","750","1500"],
                ["1","Producto28","750","1500"],
                ["1","Producto28","750","1500"],
                ["1","Producto28","750","1500"],
                [" "," ","TOTAL:","50,000.00"]]
    tabla = Table(datos)
    tabla.setStyle(TableStyle([ 
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('FONT',(0,0),(-1,0),'Helvetica-Bold'),
        ('BACKGROUND',(0,0),(-1,0),(.6588,0,.0627)),
        ('TEXTCOLOR',(0,0),(-1,0),colors.white),
        ('FONT',(2,-1),(-1,-1),'Helvetica-Bold'),
        ('BACKGROUND',(2,-1),(-1,-1),(.6588,0,.0627)),
        ('TEXTCOLOR',(2,-1),(-1,-1),colors.white),
        ('TEXTCOLOR',(0,1),(-2,-2),(.2196,.2196,.2196)),
        ('ALIGN',(0,0),(-1,0),'CENTER'),
        ('ALIGN',(0,1),(1,-2),'CENTER'),
        ('ALIGN',(2,1),(3,-1),'RIGHT'),]))
    
    for i in range(1, len(datos)-1):
        if i % 2 == 0:
            bc = (.80,.80,.80)
        else:
            bc = colors.white
    
        ts = TableStyle(
            [('BACKGROUND',(0,i),(-1,i),bc)]
            )
        tabla.setStyle(ts)
    return tabla

def go():
    doc = SimpleDocTemplate("Nota-1")
    Story = [Spacer(1,150)]
    tabla = hacerTabla()
    Story.append(tabla)
    doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)