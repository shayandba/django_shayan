"""
Generació de la documentació del projecte Pp7.2 - Django Shayan
Shayan Ali Kousar
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate,
    Paragraph, Spacer, PageBreak, HRFlowable,
    Table, TableStyle, KeepTogether
)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.pdfgen import canvas
from datetime import date


# ─── Colors del projecte ──────────────────────────────────────────────────────
BLAU_FOSC  = colors.HexColor('#004080')
BLAU_MIG   = colors.HexColor('#002a80')
BLAU_CLAR  = colors.HexColor('#a9c7ff')
BLAU_BG    = colors.HexColor('#e7f0ff')
GRIS_CLAR  = colors.HexColor('#f4f6f8')
VERD       = colors.HexColor('#28a745')
TARONJA    = colors.HexColor('#fd7e14')
VERMELL    = colors.HexColor('#dc3545')
GRIS_TEXT  = colors.HexColor('#555555')
NEGRE      = colors.HexColor('#222222')


# ─── Estils ───────────────────────────────────────────────────────────────────
def crear_estils():
    base = getSampleStyleSheet()

    estils = {
        'portada_titol': ParagraphStyle(
            'portada_titol',
            fontSize=28, leading=36,
            textColor=BLAU_FOSC,
            alignment=TA_CENTER,
            spaceAfter=10,
            fontName='Helvetica-Bold',
        ),
        'portada_subtitol': ParagraphStyle(
            'portada_subtitol',
            fontSize=16, leading=22,
            textColor=BLAU_MIG,
            alignment=TA_CENTER,
            spaceAfter=6,
            fontName='Helvetica',
        ),
        'portada_autor': ParagraphStyle(
            'portada_autor',
            fontSize=13, leading=18,
            textColor=GRIS_TEXT,
            alignment=TA_CENTER,
            fontName='Helvetica',
        ),
        'h1': ParagraphStyle(
            'h1',
            fontSize=18, leading=24,
            textColor=BLAU_FOSC,
            spaceBefore=20, spaceAfter=10,
            fontName='Helvetica-Bold',
            borderPad=4,
        ),
        'h2': ParagraphStyle(
            'h2',
            fontSize=14, leading=20,
            textColor=BLAU_MIG,
            spaceBefore=14, spaceAfter=6,
            fontName='Helvetica-Bold',
        ),
        'h3': ParagraphStyle(
            'h3',
            fontSize=12, leading=16,
            textColor=BLAU_MIG,
            spaceBefore=10, spaceAfter=4,
            fontName='Helvetica-Bold',
        ),
        'cos': ParagraphStyle(
            'cos',
            fontSize=10, leading=15,
            textColor=NEGRE,
            alignment=TA_JUSTIFY,
            spaceAfter=8,
            fontName='Helvetica',
        ),
        'codi': ParagraphStyle(
            'codi',
            fontSize=9, leading=13,
            textColor=NEGRE,
            fontName='Courier',
            backColor=colors.HexColor('#f0f0f0'),
            borderPad=6,
            spaceAfter=10,
        ),
        'nota': ParagraphStyle(
            'nota',
            fontSize=9.5, leading=14,
            textColor=BLAU_MIG,
            fontName='Helvetica-Oblique',
            spaceAfter=6,
        ),
        'toc1': ParagraphStyle(
            'toc1',
            fontSize=12, leading=18,
            textColor=BLAU_FOSC,
            fontName='Helvetica-Bold',
            leftIndent=0,
        ),
        'toc2': ParagraphStyle(
            'toc2',
            fontSize=10, leading=15,
            textColor=BLAU_MIG,
            fontName='Helvetica',
            leftIndent=20,
        ),
        'bullet': ParagraphStyle(
            'bullet',
            fontSize=10, leading=14,
            textColor=NEGRE,
            fontName='Helvetica',
            leftIndent=16,
            spaceAfter=4,
            bulletIndent=4,
        ),
    }
    return estils


# ─── DocTemplate personalitzat amb capçalera i peu ───────────────────────────
class DocPP72(BaseDocTemplate):
    def __init__(self, filename, **kwargs):
        super().__init__(filename, **kwargs)
        self.pagina_actual = 0
        frame = Frame(
            self.leftMargin, self.bottomMargin,
            self.width, self.height - 1.2 * cm,
            id='normal'
        )
        plantilla = PageTemplate(id='normal', frames=frame, onPage=self._capçalera_peu)
        self.addPageTemplates([plantilla])

    def _capçalera_peu(self, canv, doc):
        canv.saveState()
        # Línia superior
        canv.setStrokeColor(BLAU_CLAR)
        canv.setLineWidth(1.5)
        canv.line(doc.leftMargin, doc.height + doc.bottomMargin + 0.5 * cm,
                  doc.width + doc.leftMargin, doc.height + doc.bottomMargin + 0.5 * cm)
        # Peu de pàgina
        canv.setFont('Helvetica', 8)
        canv.setFillColor(GRIS_TEXT)
        canv.drawString(doc.leftMargin,
                        doc.bottomMargin - 0.6 * cm,
                        "Shayan Ali Kousar  |  Pp7.2 - Adequació d'un lloc web amb Framework Django")
        canv.drawRightString(doc.width + doc.leftMargin,
                             doc.bottomMargin - 0.6 * cm,
                             f"Pàgina {doc.page}")
        canv.restoreState()

    def afterFlowable(self, flowable):
        """Registra entrades al TOC quan troba Paragraphs marcats."""
        if isinstance(flowable, Paragraph):
            estil = flowable.style.name
            text = flowable.getPlainText()
            if estil == 'h1':
                clau = 'TOCEntry', 0, text, self.page
                self.notify('TOCEntry', (0, text, self.page))
            elif estil == 'h2':
                self.notify('TOCEntry', (1, text, self.page))


# ─── Helpers visuals ──────────────────────────────────────────────────────────
def linia(color=BLAU_CLAR, width=1):
    return HRFlowable(width='100%', thickness=width, color=color, spaceAfter=8, spaceBefore=4)


def caixa_codi(text, estils):
    """Bloc de codi amb fons gris."""
    linies = text.strip().split('\n')
    contingut = '<br/>'.join(linies)
    return Paragraph(contingut, estils['codi'])


def caixa_info(titol, text, estils, color_fons=BLAU_BG, color_bord=BLAU_CLAR):
    """Caixa destacada amb borde de color."""
    data = [[Paragraph(f'<b>{titol}</b>', estils['h3']),
             Paragraph(text, estils['cos'])]]
    taula = Table(data, colWidths=['25%', '75%'])
    taula.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), color_fons),
        ('BACKGROUND', (1, 0), (1, 0), colors.white),
        ('BOX', (0, 0), (-1, -1), 1, color_bord),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, color_bord),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [color_fons, colors.white]),
    ]))
    return taula


# ─── Contingut del document ───────────────────────────────────────────────────
def construir_document():
    estils = crear_estils()
    elements = []

    # ── PORTADA ──────────────────────────────────────────────────────────────
    elements.append(Spacer(1, 4 * cm))

    # Requadre portada
    portada_data = [[
        Paragraph("Pp7.2", estils['portada_subtitol']),
    ]]
    portada_taula = Table([[
        Paragraph("Documentació del Projecte", estils['portada_titol']),
    ]], colWidths=['100%'])
    portada_taula.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), BLAU_BG),
        ('BOX', (0, 0), (-1, -1), 2, BLAU_FOSC),
        ('PADDING', (0, 0), (-1, -1), 24),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ]))
    elements.append(portada_taula)
    elements.append(Spacer(1, 0.5 * cm))

    elements.append(Paragraph("Adequació d'un lloc web amb Framework Django", estils['portada_subtitol']))
    elements.append(Spacer(1, 0.3 * cm))
    elements.append(linia(BLAU_CLAR))
    elements.append(Spacer(1, 0.3 * cm))

    elements.append(Paragraph("Exercici: Pp5.3 — Array Multidimensional", estils['portada_subtitol']))
    elements.append(Spacer(1, 2 * cm))

    # Taula autor/data
    info_data = [
        ['Autor:', 'Shayan Ali Kousar'],
        ['Data:', date.today().strftime('%d / %m / %Y')],
        ['Tecnologia:', 'Python 3.13 + Django 6.0.2'],
        ['Activitat:', 'Ra7_2 · Pp7.2'],
    ]
    info_taula = Table(info_data, colWidths=[3.5 * cm, 8 * cm])
    info_taula.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('TEXTCOLOR', (0, 0), (0, -1), BLAU_FOSC),
        ('TEXTCOLOR', (1, 0), (1, -1), NEGRE),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [BLAU_BG, colors.white]),
        ('BOX', (0, 0), (-1, -1), 1, BLAU_CLAR),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BLAU_CLAR),
        ('PADDING', (0, 0), (-1, -1), 9),
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
    ]))
    elements.append(info_taula)
    elements.append(PageBreak())

    # ── ÍNDEX (TOC) ───────────────────────────────────────────────────────────
    elements.append(Paragraph("Índex de Continguts", estils['h1']))
    elements.append(linia())

    toc = TableOfContents()
    toc.levelStyles = [estils['toc1'], estils['toc2']]
    toc.dotsMinLevel = 0
    elements.append(toc)
    elements.append(PageBreak())

    # ── SECCIÓ 1: INTRODUCCIÓ ─────────────────────────────────────────────────
    elements.append(Paragraph("1. Introducció", estils['h1']))
    elements.append(linia())
    elements.append(Paragraph(
        "Aquest document descriu el projecte web desenvolupat per a l'activitat <b>Pp7.2 — Adequació d'un lloc "
        "web amb Framework Django</b>. El projecte consisteix a portar els tres exercicis del <b>Pp5.3</b> "
        "(originalment escrits en PHP) a un lloc web modern construït amb el framework Django.",
        estils['cos']
    ))
    elements.append(Paragraph(
        "El Pp5.3 treballava tres conceptes fonamentals de programació: la conversió de números decimals a "
        "binari, un sistema de logs amb nivells de prioritat i la visualització d'un array multidimensional "
        "amb arcs de la sèrie Naruto. Tots tres es presenten ara com pàgines web interactives.",
        estils['cos']
    ))

    elements.append(Paragraph("1.1 Objectiu de l'activitat", estils['h2']))
    elements.append(Paragraph(
        "Crear un lloc web funcional amb Django que implementi el que es va treballar a l'exercici 3 del "
        "Pp5.3 (array multidimensional), integrant-ho amb els altres exercicis de la pràctica en un projecte "
        "web cohesionat amb navegació, plantilles reutilitzables i lògica separada de la presentació.",
        estils['cos']
    ))
    elements.append(PageBreak())

    # ── SECCIÓ 2: REQUISITS ───────────────────────────────────────────────────
    elements.append(Paragraph("2. Requisits del Sistema", estils['h1']))
    elements.append(linia())
    elements.append(Paragraph(
        "Abans de poder executar el projecte, cal tenir instal·lat el programari següent:",
        estils['cos']
    ))

    req_data = [
        ['Programari', 'Versió mínima', 'Com instal·lar'],
        ['Python', '3.10 o superior', 'python.org/downloads'],
        ['Django', '4.0 o superior', 'pip install django'],
        ['Navegador web', 'Qualsevol modern', 'Chrome, Firefox, Edge...'],
    ]
    req_taula = Table(req_data, colWidths=[4 * cm, 4 * cm, 8 * cm])
    req_taula.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), BLAU_FOSC),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [BLAU_BG, colors.white]),
        ('BOX', (0, 0), (-1, -1), 1, BLAU_CLAR),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BLAU_CLAR),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ]))
    elements.append(req_taula)
    elements.append(Spacer(1, 0.5 * cm))

    elements.append(Paragraph("2.1 Verificar la instal·lació", estils['h2']))
    elements.append(Paragraph("Obre un terminal (cmd o PowerShell a Windows) i executa:", estils['cos']))
    elements.append(caixa_codi(
        "python --version\n"
        "python -m django --version",
        estils
    ))
    elements.append(Paragraph(
        "Si veus les versions de Python i Django, tot està correctament instal·lat.",
        estils['nota']
    ))
    elements.append(PageBreak())

    # ── SECCIÓ 3: ESTRUCTURA DEL PROJECTE ────────────────────────────────────
    elements.append(Paragraph("3. Estructura del Projecte", estils['h1']))
    elements.append(linia())
    elements.append(Paragraph(
        "El projecte segueix l'estructura estàndard de Django. A continuació es mostra l'arbre de fitxers "
        "i s'explica la funció de cadascun:",
        estils['cos']
    ))

    elements.append(caixa_codi(
        "Django_Shayan/\n"
        "├── manage.py               ← Eina de gestió de Django\n"
        "├── pp72_shayan/            ← Configuració del projecte\n"
        "│   ├── settings.py         ← Paràmetres generals\n"
        "│   ├── urls.py             ← URL principal (enruta a pp53)\n"
        "│   └── wsgi.py             ← Punt d'entrada per a servidors web\n"
        "└── pp53/                   ← Aplicació Django\n"
        "    ├── views.py            ← Lògica dels 3 exercicis\n"
        "    ├── urls.py             ← Les 4 rutes de l'app\n"
        "    └── templates/pp53/\n"
        "        ├── base.html       ← Plantilla base (menú + estils)\n"
        "        ├── index.html      ← Pàgina d'inici\n"
        "        ├── exercici1.html  ← Decimal a Binari\n"
        "        ├── exercici2.html  ← Sistema de Logs\n"
        "        └── exercici3.html  ← Array Multidimensional",
        estils
    ))

    elements.append(Paragraph("3.1 Descripció dels fitxers principals", estils['h2']))

    fitxers = [
        ['Fitxer', 'Funció'],
        ['manage.py',
         "Script de gestió de Django. S'usa per arrencar el servidor, "
         "crear migracions, etc."],
        ['pp72_shayan/settings.py',
         "Configuració global: apps instal·lades, base de dades, templates. "
         "Aquí s'ha afegit 'pp53' a INSTALLED_APPS."],
        ['pp72_shayan/urls.py',
         "Enruta totes les peticions HTTP cap a l'app pp53."],
        ['pp53/views.py',
         "Conté tota la lògica Python dels tres exercicis. Cada funció "
         "rep una petició i retorna una pàgina HTML renderitzada."],
        ['pp53/urls.py',
         "Defineix les 4 rutes de l'app: /, /exercici1/, /exercici2/, /exercici3/."],
        ['pp53/templates/pp53/base.html',
         "Plantilla mare que tots els exercicis hereten. Conté el menú de "
         "navegació i tots els estils CSS."],
    ]
    fitx_taula = Table(fitxers, colWidths=[4.5 * cm, 12 * cm])
    fitx_taula.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), BLAU_FOSC),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTNAME', (0, 1), (0, -1), 'Courier'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [BLAU_BG, colors.white]),
        ('BOX', (0, 0), (-1, -1), 1, BLAU_CLAR),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BLAU_CLAR),
        ('PADDING', (0, 0), (-1, -1), 7),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    elements.append(fitx_taula)
    elements.append(PageBreak())

    # ── SECCIÓ 4: COM ARRENCAR EL PROJECTE ───────────────────────────────────
    elements.append(Paragraph("4. Com Arrencar el Projecte", estils['h1']))
    elements.append(linia())
    elements.append(Paragraph(
        "Segueix aquests passos en ordre per posar en marxa el lloc web al teu ordinador:",
        estils['cos']
    ))

    passos = [
        ("Pas 1 — Obre un terminal",
         "A Windows: prem la tecla Windows, escriu <b>cmd</b> o <b>PowerShell</b> i prem Enter.",
         None),
        ("Pas 2 — Navega a la carpeta del projecte",
         "Escriu la comanda següent i prem Enter:",
         "cd C:\\Users\\kabee\\Documents\\Projectos\\Shayan\\Django_Shayan"),
        ("Pas 3 — Arrenca el servidor de desenvolupament",
         "Escriu:",
         "python manage.py runserver"),
        ("Pas 4 — Obre el navegador",
         "Obre qualsevol navegador web i ves a l'adreça:",
         "http://127.0.0.1:8000/"),
        ("Pas 5 — Explora el lloc web",
         "Ja pots navegar per les pàgines! Per aturar el servidor prem <b>Ctrl + C</b> al terminal.",
         None),
    ]

    for titol, desc, cmd in passos:
        bloc = [Paragraph(titol, estils['h3']),
                Paragraph(desc, estils['cos'])]
        if cmd:
            bloc.append(caixa_codi(cmd, estils))
        elements.append(KeepTogether(bloc + [Spacer(1, 0.2 * cm)]))

    elements.append(Paragraph(
        "Nota: El servidor de desenvolupament de Django s'executa localment. "
        "Ningú extern a la teva xarxa pot accedir-hi mentre el servidor estigui "
        "corrent en mode DEBUG=True.",
        estils['nota']
    ))
    elements.append(PageBreak())

    # ── SECCIÓ 5: PÀGINES DEL LLOC WEB ───────────────────────────────────────
    elements.append(Paragraph("5. Pàgines del Lloc Web", estils['h1']))
    elements.append(linia())
    elements.append(Paragraph(
        "El lloc web té 4 pàgines, accessibles des del menú de navegació que apareix a totes les pantalles. "
        "Cada URL correspon a una vista diferent de Django:",
        estils['cos']
    ))

    pagines = [
        ['URL', 'Pàgina', 'Descripció'],
        ['/', 'Inici', 'Pàgina de benvinguda amb accés als tres exercicis.'],
        ['/exercici1/', 'Decimal a Binari',
         "Formulari interactiu. L'usuari introdueix un número i veu el resultat en binari."],
        ['/exercici2/', 'Logs',
         "Selector de nivell de log (1, 2 o 3). Mostra els missatges segons el nivell."],
        ['/exercici3/', 'Array Multidimensional',
         "Mostra els arcs de Naruto en targetes visuals. Nucli de l'activitat Pp5.3."],
    ]
    pag_taula = Table(pagines, colWidths=[3.5 * cm, 4 * cm, 9 * cm])
    pag_taula.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), BLAU_FOSC),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTNAME', (0, 1), (0, -1), 'Courier'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [BLAU_BG, colors.white]),
        ('BOX', (0, 0), (-1, -1), 1, BLAU_CLAR),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BLAU_CLAR),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    elements.append(pag_taula)
    elements.append(PageBreak())

    # ── SECCIÓ 6: EXERCICI 1 ──────────────────────────────────────────────────
    elements.append(Paragraph("6. Exercici 1 — Conversió Decimal a Binari", estils['h1']))
    elements.append(linia())
    elements.append(Paragraph(
        "Aquesta pàgina permet a l'usuari introduir qualsevol número enter positiu i veure la seva "
        "representació en sistema binari (base 2). A diferència de la versió PHP original que tenia "
        "el número <b>24 × 4321 = 103.704</b> codificat, la versió Django és <b>interactiva</b>.",
        estils['cos']
    ))

    elements.append(Paragraph("6.1 Com funciona", estils['h2']))
    elements.append(Paragraph(
        "L'algorisme de conversió és una traducció directa del PHP original a Python. "
        "El procés és el següent:",
        estils['cos']
    ))

    passos_bin = [
        "Es divideix el número per 2 repetidament.",
        "S'emmagatzema cada residu (0 o 1) en una llista.",
        "S'inverteix la llista de residus.",
        "Es concatenen tots els bits per formar el número binari.",
    ]
    for i, p in enumerate(passos_bin, 1):
        elements.append(Paragraph(f"{i}. {p}", estils['bullet']))
    elements.append(Spacer(1, 0.3 * cm))

    elements.append(Paragraph("6.2 Codi Python (views.py)", estils['h2']))
    elements.append(caixa_codi(
        "def decimal_a_binari(num):\n"
        "    if num == 0:\n"
        "        return '0'\n"
        "    residus = []\n"
        "    while num > 0:\n"
        "        residus.append(num % 2)\n"
        "        num //= 2\n"
        "    return ''.join(str(b) for b in reversed(residus))\n"
        "\n"
        "def exercici1(request):\n"
        "    numero_str = request.GET.get('numero', '')\n"
        "    resultat = None\n"
        "    numero = ''\n"
        "    if numero_str != '':\n"
        "        numero = int(numero_str)\n"
        "        resultat = decimal_a_binari(numero)\n"
        "    return render(request, 'pp53/exercici1.html',\n"
        "                  {'numero': numero, 'resultat': resultat})",
        estils
    ))

    elements.append(Paragraph("6.3 Com usar-lo", estils['h2']))
    elements.append(Paragraph(
        "1. Ves a <b>http://127.0.0.1:8000/exercici1/</b><br/>"
        "2. Escriu un número al camp de text (per exemple: 103704).<br/>"
        "3. Fes clic a <b>Convertir</b>.<br/>"
        "4. Veuràs el resultat en binari a sota del formulari.",
        estils['cos']
    ))
    elements.append(PageBreak())

    # ── SECCIÓ 7: EXERCICI 2 ──────────────────────────────────────────────────
    elements.append(Paragraph("7. Exercici 2 — Sistema de Logs", estils['h1']))
    elements.append(linia())
    elements.append(Paragraph(
        "Simula un sistema de logs com els que s'usen en servidors reals. Hi ha tres tipus de "
        "missatge (<b>INFO</b>, <b>WARNING</b>, <b>ERROR</b>) i tres nivells de verbositat. "
        "L'usuari tria el nivell i el sistema mostra només els missatges corresponents.",
        estils['cos']
    ))

    elements.append(Paragraph("7.1 Nivells de log", estils['h2']))

    nivells_data = [
        ['Nivell', 'Mostra', 'Ús habitual'],
        ['1 — ERROR', 'Només errors crítics', 'Producció: el mínim imprescindible'],
        ['2 — WARNING', 'Errors + avisos', 'Pre-producció: detectar problemes potencials'],
        ['3 — INFO', 'Tot (errors, avisos i informació)', 'Desenvolupament: veure tot el que passa'],
    ]
    niv_taula = Table(nivells_data, colWidths=[4 * cm, 5 * cm, 7.5 * cm])
    niv_taula.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), BLAU_FOSC),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [
            colors.HexColor('#fde8e8'),
            colors.HexColor('#fff3cd'),
            colors.HexColor('#d4edda'),
        ]),
        ('BOX', (0, 0), (-1, -1), 1, BLAU_CLAR),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BLAU_CLAR),
        ('PADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(niv_taula)
    elements.append(Spacer(1, 0.4 * cm))

    elements.append(Paragraph("7.2 Codi Python (views.py)", estils['h2']))
    elements.append(caixa_codi(
        "TOTS_ELS_MISSATGES = [\n"
        "    {'tipus': 'info',    'text': 'Servidor iniciat correctament.'},\n"
        "    {'tipus': 'info',    'text': 'Consum de CPU ok.'},\n"
        "    {'tipus': 'warning', 'text': 'Consum de CPU elevat.'},\n"
        "    {'tipus': 'error',   'text': 'Missatge de correu retornat.'},\n"
        "    {'tipus': 'info',    'text': 'Consum de CPU ok.'},\n"
        "]\n"
        "\n"
        "NIVELL_MINIM = {'info': 3, 'warning': 2, 'error': 1}\n"
        "\n"
        "def exercici2(request):\n"
        "    nivell = int(request.GET.get('nivell', 3))\n"
        "    missatges = [m for m in TOTS_ELS_MISSATGES\n"
        "                 if NIVELL_MINIM[m['tipus']] <= nivell]\n"
        "    return render(request, 'pp53/exercici2.html',\n"
        "                  {'nivell': nivell, 'missatges': missatges})",
        estils
    ))
    elements.append(PageBreak())

    # ── SECCIÓ 8: EXERCICI 3 ──────────────────────────────────────────────────
    elements.append(Paragraph("8. Exercici 3 — Array Multidimensional (Naruto)", estils['h1']))
    elements.append(linia())
    elements.append(Paragraph(
        "Aquest és l'exercici principal de la pràctica Pp5.3. Implementa un <b>array multidimensional</b> "
        "(una llista de diccionaris en Python) que conté informació sobre els arcs de la sèrie <i>Naruto</i>. "
        "Cada arc té: nom, protagonista, antagonista i una llista de personatges secundaris.",
        estils['cos']
    ))

    elements.append(Paragraph("8.1 L'estructura de dades", estils['h2']))
    elements.append(Paragraph(
        "En PHP, l'exercici original usava un array associatiu multidimensional. "
        "En Python/Django, s'usa una llista de diccionaris, que és exactament equivalent:",
        estils['cos']
    ))
    elements.append(caixa_codi(
        "NARUTO = [\n"
        "    {\n"
        "        'Arc': 'Examenes Chuunin',\n"
        "        'Protagonista': 'Naruto Uzumaki',\n"
        "        'Antagonista': 'Orochimaru',\n"
        "        'Altres_Personatges': ['Sasuke Uchiha', 'Sakura Haruno',\n"
        "                               'Kakashi Hatake', 'Rock Lee'],\n"
        "    },\n"
        "    {\n"
        "        'Arc': 'Invasio de Konoha',\n"
        "        'Protagonista': 'Naruto Uzumaki',\n"
        "        'Antagonista': 'Pain',\n"
        "        'Altres_Personatges': ['Jiraiya', 'Hinata Hyuga',\n"
        "                               'Tsunade', 'Itachi Uchiha'],\n"
        "    },\n"
        "    {\n"
        "        'Arc': 'Quarta Guerra Ninja',\n"
        "        'Protagonista': 'Naruto Uzumaki',\n"
        "        'Antagonista': 'Obito Uchiha',\n"
        "        'Altres_Personatges': ['Sasuke Uchiha', 'Kakashi Hatake',\n"
        "                               'Sakura Haruno', 'Madara Uchiha'],\n"
        "    },\n"
        "]",
        estils
    ))

    elements.append(Paragraph("8.2 La vista Django", estils['h2']))
    elements.append(Paragraph(
        "La vista simplement passa l'array a la plantilla. Django s'encarrega de recórrer-lo "
        "i mostrar cada arc com una targeta visual:",
        estils['cos']
    ))
    elements.append(caixa_codi(
        "def exercici3(request):\n"
        "    return render(request, 'pp53/exercici3.html', {'naruto': NARUTO})",
        estils
    ))

    elements.append(Paragraph("8.3 La plantilla HTML", estils['h2']))
    elements.append(Paragraph(
        "La plantilla usa el bucle <b>{% for %}</b> de Django per recórrer l'array, "
        "equivalent al <b>foreach</b> de PHP:",
        estils['cos']
    ))
    elements.append(caixa_codi(
        "{% for arc in naruto %}\n"
        "<div class='pelicula'>\n"
        "    <h3>{{ arc.Arc }}</h3>\n"
        "    <p><strong>Protagonista:</strong> {{ arc.Protagonista }}</p>\n"
        "    <p><strong>Antagonista:</strong> {{ arc.Antagonista }}</p>\n"
        "    <p><strong>Altres:</strong> {{ arc.Altres_Personatges|join:', ' }}</p>\n"
        "</div>\n"
        "{% endfor %}",
        estils
    ))

    elements.append(Paragraph("8.4 Els tres arcs mostrats", estils['h2']))
    arcs_data = [
        ['Arc', 'Protagonista', 'Antagonista', 'Personatges secundaris'],
        ['Examenes Chuunin', 'Naruto Uzumaki', 'Orochimaru',
         'Sasuke, Sakura, Kakashi, Rock Lee'],
        ['Invasio de Konoha', 'Naruto Uzumaki', 'Pain',
         'Jiraiya, Hinata, Tsunade, Itachi'],
        ['Quarta Guerra Ninja', 'Naruto Uzumaki', 'Obito Uchiha',
         'Sasuke, Kakashi, Sakura, Madara'],
    ]
    arcs_taula = Table(arcs_data, colWidths=[3.8 * cm, 3.5 * cm, 3.5 * cm, 5.7 * cm])
    arcs_taula.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), BLAU_FOSC),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [BLAU_BG, colors.white]),
        ('BOX', (0, 0), (-1, -1), 1, BLAU_CLAR),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BLAU_CLAR),
        ('PADDING', (0, 0), (-1, -1), 7),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    elements.append(arcs_taula)
    elements.append(PageBreak())

    # ── SECCIÓ 9: CONCEPTES DJANGO USATS ─────────────────────────────────────
    elements.append(Paragraph("9. Conceptes Django Usats", estils['h1']))
    elements.append(linia())
    elements.append(Paragraph(
        "Aquesta secció explica els conceptes clau de Django que s'han aplicat al projecte, "
        "pensada per a qui no coneix el framework:",
        estils['cos']
    ))

    conceptes = [
        ("Patró MVT (Model-Vista-Template)",
         "Django segueix el patró MVT. En aquest projecte no s'usen Models (no hi ha base de dades), "
         "però sí Vistes (views.py, la lògica) i Templates (els fitxers .html, la presentació)."),
        ("Herència de plantilles",
         "Tots els exercicis hereten de base.html amb {% extends %}. Això evita repetir el menú "
         "i els estils a cada pàgina. Cada plantilla filla només defineix el {% block content %}."),
        ("URL routing",
         "El fitxer urls.py mapeja cada adreça URL a una funció de views.py. "
         "Quan l'usuari visita /exercici3/, Django crida la funció exercici3()."),
        ("Peticions GET",
         "Els formularis dels exercicis 1 i 2 envien dades via GET (?numero=103704). "
         "Django les recull amb request.GET.get('numero')."),
        ("Context i variables de plantilla",
         "La funció render() passa un diccionari a la plantilla. "
         "Les claus d'aquest diccionari es converteixen en variables accessibles "
         "des del HTML amb la sintaxi {{ variable }}."),
        ("Filtres de plantilla",
         "El filtre |join:', ' de Django és equivalent a implode() de PHP. "
         "Converteix la llista de personatges en un text separat per comes."),
    ]

    for titol, desc in conceptes:
        elements.append(KeepTogether([
            Paragraph(titol, estils['h3']),
            Paragraph(desc, estils['cos']),
            Spacer(1, 0.2 * cm),
        ]))

    elements.append(PageBreak())

    # ── SECCIÓ 10: EQUIVALÈNCIES PHP ↔ DJANGO ────────────────────────────────
    elements.append(Paragraph("10. Equivalències PHP ↔ Django", estils['h1']))
    elements.append(linia())
    elements.append(Paragraph(
        "Per facilitar la comprensió a qui ve del PHP original del Pp5.3, "
        "aquí es mostra la correspondència entre les dues implementacions:",
        estils['cos']
    ))

    equiv_data = [
        ['Concepte', 'PHP (Pp5.3 original)', 'Python / Django'],
        ['Array associatiu', '$arr = ["clau" => "valor"]', "d = {'clau': 'valor'}"],
        ['Array multidim.', '$arr = [["a" => 1], ["a" => 2]]', "arr = [{'a': 1}, {'a': 2}]"],
        ['Recórrer array', 'foreach ($arr as $elem)', '{% for elem in arr %}'],
        ['Mostrar variable', 'echo $variable', '{{ variable }}'],
        ['Funció', 'function nom($param) {}', 'def nom(param):'],
        ['Unir array', 'implode(", ", $arr)', '{{ arr|join:", " }}'],
        ['Paràm. URL', '$_GET["param"]', "request.GET.get('param')"],
        ['Condicional', 'if ($cond) { }', 'if cond:  /  {% if cond %}'],
    ]
    equiv_taula = Table(equiv_data, colWidths=[4 * cm, 5.5 * cm, 7 * cm])
    equiv_taula.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), BLAU_FOSC),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica'),
        ('FONTNAME', (1, 1), (2, -1), 'Courier'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [BLAU_BG, colors.white]),
        ('BOX', (0, 0), (-1, -1), 1, BLAU_CLAR),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BLAU_CLAR),
        ('PADDING', (0, 0), (-1, -1), 7),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    elements.append(equiv_taula)
    elements.append(PageBreak())

    # ── SECCIÓ 11: SOLUCIÓ DE PROBLEMES ──────────────────────────────────────
    elements.append(Paragraph("11. Solució de Problemes Comuns", estils['h1']))
    elements.append(linia())

    problemes = [
        (
            "'python' no es reconeix com una comanda",
            "Python no està instal·lat o no és al PATH del sistema. "
            "Descarrega'l de python.org i marca l'opció 'Add Python to PATH' durant la instal·lació.",
            None
        ),
        (
            "'django-admin' no es reconeix",
            "Django no està instal·lat. Obre un terminal i executa:",
            "pip install django"
        ),
        (
            "Error: That port is already in use",
            "El port 8000 l'usa un altre programa. Pots usar un port diferent:",
            "python manage.py runserver 8080"
        ),
        (
            "La pàgina no carrega / Error 404",
            "Comprova que el servidor estigui arrencat (has de veure el missatge "
            "'Starting development server at http://127.0.0.1:8000/' al terminal). "
            "Assegura't que l'adreça al navegador sigui exactament:",
            "http://127.0.0.1:8000/"
        ),
        (
            "ModuleNotFoundError: No module named 'django'",
            "Django no s'ha instal·lat a l'entorn de Python correcte. Prova:",
            "python -m pip install django"
        ),
    ]

    for titol, desc, cmd in problemes:
        bloc = [
            Paragraph(f"Problema: {titol}", estils['h3']),
            Paragraph(f"Solució: {desc}", estils['cos']),
        ]
        if cmd:
            bloc.append(caixa_codi(cmd, estils))
        bloc.append(Spacer(1, 0.3 * cm))
        elements.append(KeepTogether(bloc))

    elements.append(linia())
    elements.append(Spacer(1, 0.5 * cm))
    elements.append(Paragraph(
        "Fi del document  ·  Shayan Ali Kousar  ·  Pp7.2 amb Django",
        ParagraphStyle('fi', fontSize=10, textColor=GRIS_TEXT, alignment=TA_CENTER,
                       fontName='Helvetica-Oblique')
    ))

    return elements


# ─── Construcció del PDF ──────────────────────────────────────────────────────
def main():
    nom_fitxer = "Documentacio_Pp72_ShayanAliKousar.pdf"
    ruta = f"C:/Users/kabee/Documents/Projectos/Shayan/Django_Shayan/{nom_fitxer}"

    doc = DocPP72(
        ruta,
        pagesize=A4,
        leftMargin=2.5 * cm,
        rightMargin=2.5 * cm,
        topMargin=2.5 * cm,
        bottomMargin=2.5 * cm,
        title="Documentació Pp7.2 - Shayan Ali Kousar",
        author="Shayan Ali Kousar",
        subject="Adequació d'un lloc web amb Framework Django - Pp5.3",
    )

    elements = construir_document()
    doc.multiBuild(elements)
    print(f"PDF generat correctament: {ruta}")


if __name__ == '__main__':
    main()
