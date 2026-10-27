import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            super().showPage()
        super().save()

    def draw_header_footer(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#4A5568"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(45, 11 * inch - 36, "INGENIERIA DE MATERIALES POLIMERICOS — GUIA TECNICA RIGUROSA")
            self.drawRightString(8.5 * inch - 45, 11 * inch - 36, "MODULO 2: SUBTEMAS 4.5 - 4.12")
            self.setStrokeColor(colors.HexColor("#CBD5E0"))
            self.setLineWidth(0.6)
            self.line(45, 11 * inch - 40, 8.5 * inch - 45, 11 * inch - 40)
        
        # Footer (all pages)
        self.setStrokeColor(colors.HexColor("#CBD5E0"))
        self.setLineWidth(0.6)
        self.line(45, 42, 8.5 * inch - 45, 42)
        self.drawString(45, 30, "Licenciatura en Ingenieria Quimica | Pesos Moleculares, Arquitectura, Isomeria y Cristalinidad")
        page_str = f"Pagina {self._pageNumber} de {page_count}"
        self.drawRightString(8.5 * inch - 45, 30, page_str)
        self.restoreState()

def build_pdf(filename="Modulo_2_Polimeros_Pesos_Estructura_Cristalinidad_IQ.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=45,
        rightMargin=45,
        topMargin=50,
        bottomMargin=50
    )
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#0F2942'),
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor('#A51C30'),
        spaceAfter=10
    )
    
    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#0F2942'),
        spaceBefore=12,
        spaceAfter=5,
        keepWithNext=True
    )
    
    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13.5,
        textColor=colors.HexColor('#1A365D'),
        spaceBefore=8,
        spaceAfter=3,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor('#2D3748'),
        spaceAfter=5
    )
    
    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#2D3748'),
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=3
    )

    formula_style = ParagraphStyle(
        'Formula_Box',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=11.5,
        textColor=colors.HexColor('#1A202C'),
        spaceBefore=2,
        spaceAfter=2
    )
    
    box_text = ParagraphStyle(
        'Callout_Text',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8,
        leading=11.5,
        textColor=colors.HexColor('#1A365D')
    )

    table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7,
        leading=9,
        textColor=colors.white,
        alignment=1
    )

    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7,
        leading=9,
        textColor=colors.HexColor('#2D3748')
    )

    story = []

    # Title & Metadata Card
    story.append(Paragraph("FUNDAMENTOS DE CIENCIA E INGENIERIA DE MATERIALES", subtitle_style))
    story.append(Paragraph("Modulo 2: Pesos Moleculares, Arquitectura Macromolecular, Isomeria y Cristales", title_style))
    story.append(Paragraph("<b>Compendio Riguroso de Ingenieria Quimica</b> | Basado en W.D. Callister (Capitulo 4, Subtemas 4.5 a 4.12) interconectado con Termodinamica Estadistica, Reologia de Polimeros y Difraccion de Rayos X.", body_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0F2942"), spaceBefore=3, spaceAfter=8))

    # Academic Purpose Box
    card_data = [[
        Paragraph(
            "<b>FUENTE MAESTRA PARA CLASE MAGISTRAL DE 90 MINUTOS & PODCAST DE NOTEBOOKLM:</b><br/>"
            "Este compendio técnico integra la totalidad de los conceptos avanzados de física de polímeros requeridos para una sesión intensiva de hora y media: "
            "momentos estadísticos de masa molar (Mn, Mw, Mz, PDI), conformación de ovillo aleatorio, entrelazamientos y viscosidad de fundido, clasificación topológica "
            "(lineal, ramificado, entrecruzado, red), estereoisomerismo (tacticidad) e isomería geométrica (cis/trans), clasificación termoplástica vs. termoestable, "
            "arquitectura de copolímeros y termodinámica de cristalización con el modelo de láminas plegadas y esferulitas.",
            box_text
        )
    ]]
    card_table = Table(card_data, colWidths=[522])
    card_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#EBF8FF')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#3182CE')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(card_table)
    story.append(Spacer(1, 6))

    # =========================================================================
    # SECCION 4.5: PESO MOLECULAR Y DISTRIBUCIONES
    # =========================================================================
    story.append(Paragraph("4.5 Peso Molecular: Promedios Estadisticos, Polidispersidad y Metodos Experimentales", h1_style))
    story.append(Paragraph(
        "A diferencia de las especies quimicas puras de masa molar univoca, la polimerizacion sintetica es un proceso estocastico que produce un ensamble de cadenas "
        "con longitudes diversas. El peso molecular debe caracterizarse mediante funciones de distribucion estadistica y promedios ponderados:",
        body_style
    ))

    mw_box = [
        [Paragraph(
            "<b>1. PESO MOLECULAR PROMEDIO EN NUMERO (M_n):</b><br/>"
            "Representa la media aritmetica de las masas molares de todas las cadenas presentes. Se determina experimentalmente por metodos coligativos "
            "(osmometria de membrana, crioscopia, ebullometria y titulacion de grupos terminales):<br/>"
            "<b>M_n = &Sigma; (x_i &middot; M_i) = (&Sigma; N_i &middot; M_i) / (&Sigma; N_i)</b><br/>"
            "donde x_i = N_i / &Sigma; N_i es la fraccion numerica de cadenas con masa molar M_i.<br/><br/>"
            "<b>2. PESO MOLECULAR PROMEDIO EN PESO (M_w):</b><br/>"
            "Pondera con mayor peso a las moleculas mas pesadas, gobernando la resistencia mecanica y tenacidad. Se mide por dispersion de luz estatica (Rayleigh) "
            "y ultracentrifugacion:<br/>"
            "<b>M_w = &Sigma; (w_i &middot; M_i) = (&Sigma; N_i &middot; M_i&sup2;) / (&Sigma; N_i &middot; M_i)</b><br/>"
            "donde w_i = (N_i &middot; M_i) / &Sigma; (N_i &middot; M_i) es la fraccion en peso.<br/><br/>"
            "<b>3. GRADO DE POLIMERIZACION PROMEDIO (DP):</b><br/>"
            "Numero medio de unidades repetitivas (meros) por cadena macromolecular: <b>DP_n = M_n / m_0</b>  y  <b>DP_w = M_w / m_0</b> (donde m_0 es la masa molar del mer).<br/><br/>"
            "<b>4. INDICE DE POLIDISPERSIDAD / DISPERSIDAD (&ETH;):</b><br/>"
            "<b>&ETH; = M_w / M_n &ge; 1.0</b><br/>"
            "&bull; Polimero Monodisperso ideal (proteinas biologicas, polimeros vivos anionicos de Szwarc): &ETH; = 1.00.<br/>"
            "&bull; Polimerizacion por condensacion en equilibrio (Distribucion mas probable de Flory): &ETH; = 1 + p &rarr; 2.0 (a p &rarr; 1).<br/>"
            "&bull; Polimerizacion radicalaria con terminacion bimolecular: &ETH; = 1.5 a 2.0 (sin transferencia de cadena).<br/>"
            "&bull; Resinas comerciales industriales (Ziegler-Natta heterogeneas): &ETH; = 4.0 a 20.0.",
            formula_style
        )]
    ]
    t_mw = Table(mw_box, colWidths=[522])
    t_mw.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F7FAFC')),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor('#CBD5E0')),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_mw)
    story.append(Spacer(1, 6))

    story.append(Paragraph("4.5.1 Influencia del Peso Molecular en las Propiedades Mecanicas y Termicas (Figura 4.4 de Callister)", h2_style))
    story.append(Paragraph(
        "Las propiedades mecanicas (resistencia a la traccion &sigma;_ts) y termicas (temperatura de fusion T_m) aumentan asintoticamente con el peso molecular hasta una meseta critica:<br/>"
        "<b>&sigma;_ts = &sigma;_{ts,&infin;} - (A / M_n)</b> (Ecuacion de Flory-Fox).<br/>"
        "&bull; <b>Por debajo de M_n &approx; 10,000 g/mol:</b> Las cadenas son cortas y fluyen o se desmoronan bajo tension (ceras quebradizas sin resistencia estructural).<br/>"
        "&bull; <b>Por encima de un peso critico de entrelazamiento (M_c &approx; 10,000 - 30,000 g/mol):</b> Las cadenas se entrelazan fisicamente de forma densa, "
        "desarrollando una red viscoelastica que imparte tenacidad al impacto y resistencia a la fractura.<br/>"
        "&bull; <b>Efecto en Reologia de Procesos IQ:</b> La viscosidad de cizallamiento en estado fundido a baja deformacion (&eta;_0) sigue la ley de potencias de Berry y Fox: "
        "&eta;_0 &prop; M_w para M &lt; M_c, y <b>&eta;_0 &prop; M_w^(3.4) para M &gt; M_c</b>. Un incremento modesto en M_w dispara la presion de extrusion y el requerimiento de potencia de los motores de bombeo.",
        body_style
    ))

    story.append(Spacer(1, 6))

    # =========================================================================
    # SECCION 4.6: FORMA MOLECULAR Y CONFORMACION
    # =========================================================================
    story.append(Paragraph("4.6 Forma Molecular: Rotacion Interna, Ovillos Estadisticos y Entrelazamientos", h1_style))
    story.append(Paragraph(
        "Alrededor de cada enlace simple C-C sp&sup3;, los atomos pueden girar libremente describiendo un cono de rotacion espacial con angulo de 109.5&deg; (Figura 4.5 de Callister). "
        "Como una macromolecula contiene decenas de miles de enlaces consecutivos, esta rotacion probabilistica provoca que la cadena se pliegue, doble y contorsione sobre si misma (Figura 4.6).",
        body_style
    ))

    shape_box = [
        [Paragraph(
            "<b>MODELO DEL OVILLO ESTADISTICO ALEATORIO (RANDOM COIL):</b><br/>"
            "En estado no deformado (fundido o solucion theta), la conformacion macromolecular se modela como un paseo aleatorio espacial.<br/>"
            "&bull; <b>Longitud de contorno extendido (L_c):</b> Distancia total si la cadena se estirara en linea recta en zig-zag:<br/>"
            "L_c = N &middot; d_(C-C) &middot; sen(109.5&deg;/2) = N &middot; 0.126 nm.<br/>"
            "&bull; <b>Distancia media cuadratico-extremo (&lang;r&sup2;&rang;_0^(1/2)):</b> Distancia euclidiana vectorial entre el primer y ultimo carbono de la cadena:<br/>"
            "<b>&lang;r&sup2;&rang;_0 = N &middot; l&sup2; &middot; C_&infin;</b><br/>"
            "donde l = 0.154 nm es la longitud de enlace, N es el numero de enlaces de la cadena y C_&infin; es la relacion caracteristica de Flory (rigidez conformacional intrinseca, "
            "C_&infin; &approx; 6.7 para PE y 8.5 para PS). Para una cadena con L_c = 1260 nm (DP = 5000), la distancia extremo a extremo es de solo &approx; 25 nm. "
            "La macromolecula adopta la forma de una madeja globular altamente porosa.",
            formula_style
        )]
    ]
    t_shape = Table(shape_box, colWidths=[522])
    t_shape.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F7FAFC')),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor('#CBD5E0')),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_shape)
    story.append(Spacer(1, 6))

    # =========================================================================
    # SECCION 4.7: ESTRUCTURA MOLECULAR (LINEAL, RAMIFICADA, ENTRECRUZADA, RED)
    # =========================================================================
    story.append(Paragraph("4.7 Estructura Molecular: Clasificacion Topologica (Figura 4.7 de Callister)", h1_style))
    story.append(Paragraph(
        "Las propiedades fisicas dependen drasticamente de la arquitectura geometrica y conectividad de la cadena:",
        body_style
    ))

    struct_rows = [
        [
            Paragraph("<b>Estructura</b>", table_header),
            Paragraph("<b>Descripcion Arquitectonica</b>", table_header),
            Paragraph("<b>Fuerzas y Enlaces</b>", table_header),
            Paragraph("<b>Propiedades Termomecanicas</b>", table_header),
            Paragraph("<b>Ejemplo Industrial</b>", table_header)
        ],
        [
            Paragraph("<b>Lineal</b><br/>(Figura 4.7a)", table_cell),
            Paragraph("Cadenas sencillas en hilera sin bifurcaciones covalentes.", table_cell),
            Paragraph("Covalente en la cadena; dispersion secundaria entre cadenas.", table_cell),
            Paragraph("Alto empaquetamiento, alta cristalinidad y densidad. Termoplastico reciclable.", table_cell),
            Paragraph("HDPE (&rho; = 0.96 g/cm&sup3;), PVC, Nylon 6,6.", table_cell)
        ],
        [
            Paragraph("<b>Ramificada</b><br/>(Figura 4.7b)", table_cell),
            Paragraph("Cadenas secundarias conectadas al esqueleto por reacciones de transferencia.", table_cell),
            Paragraph("Covalente en nudos de ramificacion; dispersion secundaria entre ramas.", table_cell),
            Paragraph("Baja densidad por impedimento esterico de empaquetamiento. Mas flexible, menor Tm.", table_cell),
            Paragraph("LDPE (&rho; = 0.92 g/cm&sup3;), LLDPE.", table_cell)
        ],
        [
            Paragraph("<b>Entrecruzada</b><br/>(Figura 4.7c)", table_cell),
            Paragraph("Cadenas lineales unidas transversalmente por puentes quimicos cortos.", table_cell),
            Paragraph("Puentes covalentes primarios entre cadenas (ej. enlaces disulfuro -S-S-).", table_cell),
            Paragraph("Impide el flujo viscoso plastico irreversible; elastomeros con memoria elastica.", table_cell),
            Paragraph("Caucho natural vulcanizado con azufre.", table_cell)
        ],
        [
            Paragraph("<b>Red 3D</b><br/>(Figura 4.7d)", table_cell),
            Paragraph("Monomeros polifuncionales (f &ge; 3) forman un entramado tridimensional infinito.", table_cell),
            Paragraph("Malla covalente primaria continua en todo el volumen macroscopico.", table_cell),
            Paragraph("Infusible e insoluble; degrada termicamente antes de fundir. Modulo elastico alto.", table_cell),
            Paragraph("Resinas epoxicas, Baquelita, Poliuretanos rigidos.", table_cell)
        ]
    ]
    t_struct = Table(struct_rows, colWidths=[65, 115, 115, 127, 100])
    t_struct.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F2942')),
        ('ALIGN', (0,0), (-1,0), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E0')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F7FAFC')])
    ]))
    story.append(t_struct)
    story.append(Spacer(1, 8))

    # =========================================================================
    # SECCION 4.8: CONFIGURACIONES MOLECULARES (TACTICIDAD Y CIS/TRANS)
    # =========================================================================
    story.append(Paragraph("4.8 Configuraciones Moleculares: Estereoisomerismo (Tacticidad) e Isomeria Geometrica", h1_style))
    story.append(Paragraph(
        "<b>Rigor Terminologico Esencial:</b> Una <b>conformacion</b> se altera mediante rotacion sobre enlaces simples sin romper enlaces (trans, gauche). "
        "Una <b>configuracion</b> describe la disposicion espacial fija de los enlaces atomicos y <i>solo puede modificarse rompiendo y reformando enlaces covalentes primarios</i>.",
        body_style
    ))

    story.append(Paragraph("4.8.1 Estereoisomerismo y Tacticidad en Polimeros Vinilicos [-CH2-CHR-]", h2_style))
    story.append(Paragraph(
        "En monomeros asimetricos como el propileno o el estireno, cada carbono portador del grupo R es un centro quiral. Segun la orientacion espacial del grupo colgante (Callister p. 140–141):<br/>"
        "• <b>Isotactico:</b> Todos los grupos R estan ubicados en el mismo lado del plano del esqueleto de carbono en zig-zag. "
        "La simetria estereoquimica perfecta permite que las cadenas se plieguen en helices regulares formando cristales densos (Polipropileno isotactico i-PP, T_m &approx; 165-175 &deg;C, material rigido estructural).<br/>"
        "• <b>Sindiotactico:</b> Los grupos R alternan de forma estrictamente regular a uno y otro lado del plano de la cadena. Es altamente cristalino (T_m &approx; 130 &deg;C).<br/>"
        "• <b>Atactico:</b> Los grupos R estan distribuidos de manera completamente aleatoria e irregular a lo largo de la cadena. "
        "El desorden esterico impide por completo el empaquetamiento reticular: el polimero es 100% amorfo, blando, pegajoso y gomoso (Polipropileno atactico a-PP, inutil para aplicaciones estructurales).<br/>"
        "<b>Catalisis Ziegler-Natta / Metalocenos en IQ:</b> El control de la tacticidad mediante catalizadores estereoespecificos (K. Ziegler y G. Natta, Premio Nobel 1963) permitio transformar el propileno de un residuo petroquimico pegajoso en el segundo plastico de mayor produccion mundial.",
        body_style
    ))

    story.append(Paragraph("4.8.2 Isomeria Geometrica: Cis vs. Trans en Polidienos (Poliisopreno)", h2_style))
    story.append(Paragraph(
        "Cuando el monomero contiene un enlace doble remanente en la cadena principal (ej. polimerizacion 1,4 del isopreno, CH2=C(CH3)-CH=CH2):<br/>"
        "• <b>Cis-1,4-poliisopreno (Caucho Natural):</b> El grupo -CH3 y el atomo de H estan situados del mismo lado del doble enlace C=C. "
        "Esta geometria introduce una inflexion forzada o codo de 120&deg; que dificulta el empaquetamiento cristalino; a temperatura ambiente es un elastomero flexible (T_g &approx; -70 &deg;C).<br/>"
        "• <b>Trans-1,4-poliisopreno (Gutapercha):</b> El grupo -CH3 y el atomo de H se ubican en lados opuestos del doble enlace. "
        "La cadena adopta una configuracion lineal continua en zig-zag que cristaliza facilmente, resultando en un material termoplastico rigido y duro a temperatura ambiente (T_m &approx; 65 &deg;C, utilizado en pelotas de golf y aislamientos marinos).",
        body_style
    ))

    story.append(Spacer(1, 6))

    # =========================================================================
    # SECCION 4.9: TERMOPLASTICOS VS TERMOESTABLES
    # =========================================================================
    story.append(Paragraph("4.9 Polimeros Termoplasticos vs. Termoestables: Criterio Termomecanico y Reologico", h1_style))
    story.append(Paragraph(
        "Esta distincion determina el metodo de manufactura, diseno de equipos de moldeo y viabilidad de reciclaje:",
        body_style
    ))

    t_tt_rows = [
        [
            Paragraph("<b>Propiedad</b>", table_header),
            Paragraph("<b>Polimeros Termoplasticos</b>", table_header),
            Paragraph("<b>Polimeros Termoestables (Thermosets)</b>", table_header)
        ],
        [
            Paragraph("<b>Estructura Macromolecular</b>", table_cell),
            Paragraph("Cadenas lineales o ramificadas unidas por fuerzas secundarias debiles.", table_cell),
            Paragraph("Red tridimensional infinita unida por enlaces covalentes primarios.", table_cell)
        ],
        [
            Paragraph("<b>Respuesta al Calor</b>", table_cell),
            Paragraph("Se ablandan y fluyen reversiblemente al calentarse; solidifican al enfriar.", table_cell),
            Paragraph("Se curan irreversiblemente al calentarse; no funden, degradan piroliticamente.", table_cell)
        ],
        [
            Paragraph("<b>Solubilidad en Solventes</b>", table_cell),
            Paragraph("Solubles o hinchables en solventes de parametro &delta; afin.", table_cell),
            Paragraph("Insolubles; solo pueden experimentar hinchamiento elastico limitado.", table_cell)
        ],
        [
            Paragraph("<b>Reciclabilidad</b>", table_cell),
            Paragraph("Facilmente reciclables por remolido y refundicion mecanica.", table_cell),
            Paragraph("No reciclables termicamente; requieren reciclaje quimico o relleno inerte.", table_cell)
        ],
        [
            Paragraph("<b>Procesos Industriales IQ</b>", table_cell),
            Paragraph("Extrusion, moldeo por inyeccion, soplado, termoformado.", table_cell),
            Paragraph("Moldeo por compresion, inyeccion y reaccion (RIM), pultrusion.", table_cell)
        ]
    ]
    t_tt = Table(t_tt_rows, colWidths=[102, 210, 210])
    t_tt.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F2942')),
        ('ALIGN', (0,0), (-1,0), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E0')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F7FAFC')])
    ]))
    story.append(t_tt)
    story.append(Spacer(1, 8))

    # =========================================================================
    # SECCION 4.10: COPOLIMEROS
    # =========================================================================
    story.append(Paragraph("4.10 Copolimeros: Clasificacion Arquitectonica y Elastómeros Termoplasticos (TPE)", h1_style))
    story.append(Paragraph(
        "Cuando dos o mas unidades quimicas distintas se combinan en la misma macromolecula (Callister Figura 4.9 y Tabla 4.5):<br/>"
        "• <b>Copolimero al azar (Random):</b> Las unidades A y B se distribuyen estadisticamente sin orden: -A-B-B-A-B-A-A- (ej. Caucho SBR para neumaticos).<br/>"
        "• <b>Copolimero alternado:</b> Secuencia regular estricta: -A-B-A-B-A-B-A-B-.<br/>"
        "• <b>Copolimero en bloque:</b> Bloques contiguos de homopolimero unidos extremo con extremo: -A-A-A-A-B-B-B-B- (ej. SBS tribloque: estireno-butadieno-estireno).<br/>"
        "• <b>Copolimero de injerto (Graft):</b> Ramas de homopolimero B injertadas covalentemente en una cadena principal de A (ej. HIPS: poliestireno de alto impacto).<br/>"
        "<b>Morfologia de Microfases en Bloques SBS (Ingenieria de Materiales):</b> El poliestireno es incompatible termodinamicamente con el polibutadieno (&Delta;H_mix &gt; 0). "
        "En un bloque SBS, los dominios terminales de PS se segregan formando microdominios esfericos vitreos rigidos (T_g &approx; 100 &deg;C) inmersos en una matriz elastica continua de PB (T_g &approx; -90 &deg;C). "
        "Los nodulos de PS actuan como <i>entrecruzamientos fisicos termorreversibles</i>: a temperatura ambiente se comporta como caucho vulcanizado, pero a T &gt; 100 &deg;C los dominios de PS funden y se procesa por inyeccion convencional como un termoplastico.",
        body_style
    ))

    story.append(Spacer(1, 8))

    # Page Break for Crystallinity & Crystals
    story.append(PageBreak())

    # =========================================================================
    # SECCION 4.11: CRISTALINIDAD EN POLIMEROS
    # =========================================================================
    story.append(Paragraph("4.11 Cristalinidad en Polímeros: Grado de Cristalinidad por Metodo de Densidad", h1_style))
    story.append(Paragraph(
        "A diferencia de los metales, ningun polimero de cadena sintetica es 100% cristalino. Los polimeros adoptan una morfologia <b>semicristalina</b>, "
        "donde regiones laminares de empaquetamiento regular ordenado (cristalitos) coexisten con zonas amorfas enmarañadas desordenadas.",
        body_style
    ))

    cryst_box = [
        [Paragraph(
            "<b>DEDUCCION DE LA ECUACION DE PORCENTAJE DE CRISTALINIDAD BASADA EN DENSIDAD:</b><br/>"
            "Considerando un volumen unitario compuesto por una fraccion volumetrica cristalina V_c y una fraccion amorfa V_a (V_c + V_a = 1):<br/>"
            "Masa total de la muestra: m_s = m_c + m_a  &rArr;  &rho;_s &middot; V_total = &rho;_c &middot; V_c + &rho;_a &middot; V_a.<br/>"
            "Expresando la fraccion en peso o masa cristalina (W_c = m_c / m_s) y reordenando analiticamente con las densidades especificas:<br/>"
            "<b>% Cristalinidad = [ &rho;_c &middot; (&rho;_s - &rho;_a) / [ &rho;_s &middot; (&rho;_c - &rho;_a) ] ] &times; 100</b><br/><br/>"
            "donde:<br/>"
            "&bull; &rho;_s = Densidad experimental medida de la muestra semicristalina.<br/>"
            "&bull; &rho;_c = Densidad teorica del cristal 100% perfecto (calculada de las dimensiones de la celda unitaria de rayos X, Figura 4.10).<br/>"
            "&bull; &rho;_a = Densidad de la fase 100% amorfa (medida en muestra templada ultra-rapidamente desde el fundido).<br/>"
            "Dado que las cadenas estan mas densamente empaquetadas en la red cristalina que en el estado amorfo desordenado: <b>&rho;_c &gt; &rho;_s &gt; &rho;_a</b>.",
            formula_style
        )]
    ]
    t_cryst = Table(cryst_box, colWidths=[522])
    t_cryst.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F7FAFC')),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor('#CBD5E0')),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_cryst)
    story.append(Spacer(1, 6))

    story.append(Paragraph("4.11.1 Factores Fisicoquimicos que Influyen en el Grado de Cristalinidad", h2_style))
    story.append(Paragraph(
        "1. <b>Velocidad de Enfriamiento (Cinetica de Cristalizacion):</b> Un enfriamiento lento permite a las cadenas tiempo difusional para desenmarañarse y alinearse en la red cristalina (alta cristalinidad). Un enfriamiento brusco (quench) congela las cadenas en su conformacion desordenada (predominio amorfo).<br/>"
        "2. <b>Estructura de la Cadena:</b> Polimeros lineales sencillos (PE) cristalizan hasta el 80-90%. Cadenas con ramificaciones densas (LDPE) o sustituyentes voluminosos no pueden empaquetarse facil.<br/>"
        "3. <b>Configuracion Esterica (Tacticidad):</b> Polimeros isotacticos y sindiotacticos cristalizan rapidamente; polimeros atacticos son incapaces de cristalizar (100% amorfos).<br/>"
        "4. <b>Polaridad y Puentes de Hidrogeno:</b> En poliamidas (Nylon 6,6), la fuerte atraccion electrostatica de los puentes de H intercatenarios orienta e induce cristalizacion casi instantanea.",
        body_style
    ))

    story.append(Spacer(1, 6))

    # =========================================================================
    # SECCION 4.12: CRISTALES POLIMERICOS (LAMINAS PLEGADAS Y ESFERULITAS)
    # =========================================================================
    story.append(Paragraph("4.12 Cristales Polimericos: Celda Unitaria, Laminas Plegadas y Estructura Esferulitica", h1_style))
    story.append(Paragraph(
        "A nivel nano y micrometrico, el ordenamiento cristalino macromolecular adopta tres jerarquias estructurales sucesivas (Callister p. 146–151):",
        body_style
    ))

    story.append(Paragraph("4.12.1 Celda Unitaria del Polietileno (Figura 4.10)", h2_style))
    story.append(Paragraph(
        "El polietileno cristaliza en una <b>celda unitaria ortorrombica</b> con parametros de red: a = 0.741 nm, b = 0.494 nm, c = 0.255 nm. "
        "El eje c coincide exactamente con la direccion del esqueleto en zig-zag de la cadena. Cada celda unitaria contiene el equivalente a 2 unidades repetitivas (m = 2 &times; 28.05 g/mol). "
        "Calculando la densidad teorica mediante &rho;_c = n&middot;A / (V_C &middot; N_A), se obtiene &rho;_c = 0.998 g/cm&sup3;.",
        body_style
    ))

    story.append(Paragraph("4.12.2 Modelo de Cadenas Plegadas (Folded-Chain Lamellae, Figuras 4.11 y 4.12)", h2_style))
    story.append(Paragraph(
        "Al cristalizar desde soluciones diluidas, los polimeros forman micro-plaquetas monocristalinas de 10 a 20 nm de espesor pero de varios micrometros de extension lateral. "
        "Dado que una macromolecula tiene una longitud extendida de cientos o miles de nanometros, la cadena debe <b>plegarse sobre si misma en horquilla</b> repetidamente a traves del espesor de la laminilla.",
        body_style
    ))

    story.append(Paragraph("4.12.3 Esferulitas y la Cruz de Malta (Figuras 4.13 y 4.14)", h2_style))
    story.append(Paragraph(
        "Al solidificar desde el fundido no perturbado, la cristalizacion procede mediante agregados esfericos denominados <b>esferulitas</b>:<br/>"
        "• <b>Morfologia Radial:</b> Desde un nucleo central de heterogeneidad, laminillas cristalinas plegadas crecen radialmente hacia afuera en forma de cintas espirales, "
        "separadas por material amorfo interlamelar e interconectadas por 'cadenas de amarre' (tie molecules) que confieren resistencia a la fractura.<br/>"
        "• <b>Extincion Optica (Cruz de Malta):</b> Bajo un microscopio petrografico con luz polarizada cruzada (Figura 4.14), las esferulitas exhiben un patron de extincion birrefringente en forma de <b>Cruz de Malta</b> "
        "a lo largo de los ejes vertical y horizontal, causado por la orientacion tangencial uniforme y simetrica de los ejes opticos moleculares respecto al radio de la esferulita.",
        body_style
    ))

    story.append(Spacer(1, 10))

    # =========================================================================
    # PROBLEMAS NUMERICOS RESUELTOS DEL MODULO 2
    # =========================================================================
    story.append(Paragraph("Problemas de Calculo Cuantitativo Resueltos Paso a Paso (Nivel Examen IQ)", h1_style))
    
    # Problema 1: Calculo de Mn, Mw y PDI
    story.append(Paragraph("<b>Problema 1: Determinacion de Mn, Mw, DP y Polidispersidad a partir de Datos de Fraccionamiento (Callister Ejemplo 4.1)</b>", h2_style))
    p1_text = (
        "<b>Enunciado:</b> Una muestra de poli(cloruro de vinilo) (PVC, mer = C2H3Cl, m_0 = 62.50 g/mol) se fracciono obteniendo los siguientes intervalos de masa molecular:<br/>"
        "Intervalos (g/mol): [5,000-15,000], [15,000-25,000], [25,000-35,000], [35,000-45,000].<br/>"
        "M_i medios: 10,000; 20,000; 30,000; 40,000 g/mol.<br/>"
        "Fracciones numericas (x_i): 0.15, 0.40, 0.30, 0.15 (total = 1.00).<br/>"
        "Fracciones en peso (w_i): 0.061, 0.327, 0.367, 0.245 (total = 1.00).<br/>"
        "Calcule M_n, M_w, el grado de polimerizacion promedio en numero (DP_n) y la dispersidad (&ETH;).<br/><br/>"
        "<b>Solucion Rigurosa:</b><br/>"
        "1. <i>M_n = &Sigma; (x_i &middot; M_i):</i><br/>"
        "M_n = (0.15 &times; 10,000) + (0.40 &times; 20,000) + (0.30 &times; 30,000) + (0.15 &times; 40,000)<br/>"
        "M_n = 1,500 + 8,000 + 9,000 + 6,000 = <b>24,500 g/mol</b>.<br/><br/>"
        "2. <i>M_w = &Sigma; (w_i &middot; M_i):</i><br/>"
        "M_w = (0.061 &times; 10,000) + (0.327 &times; 20,000) + (0.367 &times; 30,000) + (0.245 &times; 40,000)<br/>"
        "M_w = 610 + 6,540 + 11,010 + 9,800 = <b>27,960 g/mol</b>.<br/><br/>"
        "3. <i>Grado de Polimerizacion Promedio (DP_n):</i><br/>"
        "DP_n = M_n / m_0 = 24,500 / 62.50 = <b>392 unidades repetitivas</b>.<br/><br/>"
        "4. <i>Indice de Polidispersidad (&ETH;):</i><br/>"
        "&ETH; = M_w / M_n = 27,960 / 24,500 &approx; <b>1.141</b> (Distribucion polidispersa moderadamente estrecha)."
    )
    t_p1 = Table([[Paragraph(p1_text, body_style)]], colWidths=[522])
    t_p1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#EDF2F7')),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor('#CBD5E0')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_p1)
    story.append(Spacer(1, 6))

    # Problema 2: Porcentaje de cristalinidad
    story.append(Paragraph("<b>Problema 2: Calculo de Cristalinidad en Polietileno a partir de Mediciones Picnometricas de Densidad</b>", h2_style))
    p2_text = (
        "<b>Enunciado:</b> Se midio la densidad picnometrica de una pieza de Polietileno a 25 &deg;C obteniendo &rho;_s = 0.965 g/cm&sup3; (HDPE). "
        "De datos cristalograficos de celda unitaria de rayos X se sabe que la densidad del cristal perfecto es &rho;_c = 0.998 g/cm&sup3;, "
        "mientras que la densidad de la fase amorfa pura es &rho;_a = 0.870 g/cm&sup3;. "
        "Calcule el porcentaje volumetrico y masico de cristalinidad de la muestra.<br/><br/>"
        "<b>Solucion Rigurosa:</b><br/>"
        "Aplicando la ecuacion de cristalinidad de Callister:<br/>"
        "% Cristalinidad = [ &rho;_c &middot; (&rho;_s - &rho;_a) ] / [ &rho;_s &middot; (&rho;_c - &rho;_a) ] &times; 100<br/>"
        "1. Diferencia (&rho;_s - &rho;_a) = 0.965 - 0.870 = 0.095 g/cm&sup3;.<br/>"
        "2. Diferencia (&rho;_c - &rho;_a) = 0.998 - 0.870 = 0.128 g/cm&sup3;.<br/>"
        "3. Sustitucion:<br/>"
        "% Cristalinidad = [ 0.998 &times; 0.095 ] / [ 0.965 &times; 0.128 ] &times; 100<br/>"
        "% Cristalinidad = [ 0.09481 ] / [ 0.12352 ] &times; 100 &approx; <b>76.76 %</b>.<br/>"
        "<b>Dictamen Tecnico:</b> La muestra posee un 76.8% de fase cristalina, confirmando que se trata de un Polietileno de Alta Densidad (HDPE) "
        "apto para tuberias sometidas a presion hidrostatica interna y barreras contra vapor."
    )
    t_p2 = Table([[Paragraph(p2_text, body_style)]], colWidths=[522])
    t_p2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#EDF2F7')),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor('#CBD5E0')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_p2)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully built: {filename}")

if __name__ == "__main__":
    build_pdf()
