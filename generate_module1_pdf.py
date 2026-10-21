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
            self.drawRightString(8.5 * inch - 45, 11 * inch - 36, "MODULO 1: SUBTEMAS 4.1 - 4.4")
            self.setStrokeColor(colors.HexColor("#CBD5E0"))
            self.setLineWidth(0.6)
            self.line(45, 11 * inch - 40, 8.5 * inch - 45, 11 * inch - 40)
        
        # Footer (all pages)
        self.setStrokeColor(colors.HexColor("#CBD5E0"))
        self.setLineWidth(0.6)
        self.line(45, 42, 8.5 * inch - 45, 42)
        self.drawString(45, 30, "Licenciatura en Ingenieria Quimica | Fundamentos de Estructura, Termodinamica y Cinetica de Polimeros")
        page_str = f"Pagina {self._pageNumber} de {page_count}"
        self.drawRightString(8.5 * inch - 45, 30, page_str)
        self.restoreState()

def build_pdf(filename="Modulo_1_Polimeros_Estructura_Quimica_IQ.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=45,
        rightMargin=45,
        topMargin=50,
        bottomMargin=50
    )
    
    styles = getSampleStyleSheet()
    
    # Custom styles
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
        textColor=colors.HexColor('#2B6CB0'),
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
        alignment=1 # Center
    )

    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7,
        leading=9,
        textColor=colors.HexColor('#2D3748')
    )
    
    table_cell_code = ParagraphStyle(
        'TableCellCode',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=6.5,
        leading=8,
        textColor=colors.HexColor('#1A202C')
    )

    story = []

    # Title & Metadata Card
    story.append(Paragraph("FUNDAMENTOS DE CIENCIA E INGENIERIA DE MATERIALES", subtitle_style))
    story.append(Paragraph("Modulo 1: Estructura, Termodinamica y Mecanismos de Reaccion en Polimeros", title_style))
    story.append(Paragraph("<b>Enfoque Riguroso para Ingenieria Quimica</b> | Basado en W.D. Callister (Capitulo 4, Subtemas 4.1 a 4.4) interconectado con Cinetica de Reactores, Fenomenos de Transporte y Termodinamica Molecular.", body_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0F2942"), spaceBefore=3, spaceAfter=8))

    # Context Card Box
    card_data = [[
        Paragraph(
            "<b>PROPOSITO ACADEMICO PARA GEMINI NOTEBOOK / NOTEBOOKLM:</b><br/>"
            "Este documento constituye una fuente tecnica de maxima profundidad analitica correspondiente al primer bloque de polimeros. "
            "Su diseno permite a los modelos de lenguaje extraer definiciones formales (IUPAC), deducciones matematicas de cinetica de polimerizacion (QSSA), "
            "balances estequiometricos de Carothers, termodinamica de conformacion molecular y criterios cuantitativos de diseno en reactores quimicos.",
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
    # SECCION 4.1: INTRODUCCION A LAS MACROMOLECULAS Y EVOLUCION DE MATERIALES
    # =========================================================================
    story.append(Paragraph("4.1 Introduccion a las Macromoleculas y Evolucion de los Materiales", h1_style))
    story.append(Paragraph(
        "Historicamente, la humanidad empleo polimeros naturales derivados de la biomasa (madera, caucho natural / poliisopreno, algodon, lana, seda, celulosa y proteinas). "
        "Sin embargo, la sintesis macromolecular a partir de materias primas petroquimicas (olefinas y aromaticos) tras la Segunda Guerra Mundial revoluciono la ingenieria de procesos. "
        "A diferencia de los metales (gobernados por enlaces metalicos deslocalizados y redes cristalinas tridimensionales periodicas) y los ceramicos (enlaces ionico-covalentes en redes de coordinacion de alto punto de fusion), "
        "los polimeros sinteticos presentan propiedades distintivas cruciales para el Ingeniero Quimico:",
        body_style
    ))

    story.append(Paragraph("&bull; <b>Naturaleza Macromolecular y Polidispersidad:</b> Mientras que una molecula de bajo peso molecular (agua, benceno, acido sulfurico) posee una masa molar univoca y fija (monodispersa), los polimeros sinteticos consisten en un ensamble estadistico de cadenas de distintas longitudes, requiriendo su caracterizacion mediante momentos estadisticos de distribucion de pesos moleculares (M_n, M_w, M_z).", bullet_style))
    story.append(Paragraph("&bull; <b>Dualidad Enlace Covalente / Interacciones Secundarias:</b> La resistencia intrinseca a lo largo del esqueleto macromolecular esta sustentada por enlaces covalentes sigma (C-C, C-O, C-N), mientras que las propiedades termomecanicas macroscopicas (cohesion, fluencia, fusion, disolucion y viscoelasticidad) estan gobernadas por fuerzas intermoleculares secundarias (dispersion de London, dipolo-dipolo, puentes de hidrogeno) y entrelazamientos fisicos.", bullet_style))
    story.append(Paragraph("&bull; <b>Resistencia Especifica e Inercia Quimica:</b> Su baja densidad (tipicamente 0.90 a 1.50 g/cm&sup3;, frente a los 7.85 g/cm&sup3; del acero) confiere una alta resistencia especifica (traccion/densidad). Ademas, su inercia electroquimica elimina los problemas de corrosion galvanica y quimica por soluciones salinas o acidos no oxidantes, convirtiendolos en materiales criticos para tuberias, reactores quimicos revestidos y membranas de separacion molecular.", bullet_style))

    story.append(Spacer(1, 6))

    # =========================================================================
    # SECCION 4.2: HIDROCARBUROS, HIBRIDACION Y TERMODINAMICA INTERMOLECULAR
    # =========================================================================
    story.append(Paragraph("4.2 Moleculas de Hidrocarburos: Hibridacion Orbital, Saturacion y Fuerzas Intermoleculares", h1_style))
    story.append(Paragraph(
        "La mayoria de los polimeros comerciales tienen como base hidrocarburos organicos. El comportamiento termodinamico, reactividad y propiedades conformacionales "
        "derivan directamente de la mecanica cuantica de los orbitales del carbono (configuracion fundamental 1s&sup2; 2s&sup2; 2p&sup2;).",
        body_style
    ))

    story.append(Paragraph("4.2.1 Geometria Orbital, Angulos de Enlace y Energias de Disociacion", h2_style))
    story.append(Paragraph(
        "Al promover un electron del orbital 2s al orbital vacio 2p_z, la hibridacion de funciones de onda genera orbitales degenerados:",
        body_style
    ))

    formula_1 = [
        [Paragraph("<b>Hibridacion sp&sup3; (Alcanos / Esqueleto Saturado de Cadenas Polimericas):</b><br/>"
                   "&bull; Geometria: Tetraedrica regular | Angulo de enlace: &theta; = 109.47&deg; (&approx; 109.5&deg;)<br/>"
                   "&bull; Longitud de enlace C-C: d = 0.154 nm (1.54 &Aring;) | Energia de disociacion: E_diss &approx; 348 kJ/mol<br/>"
                   "&bull; Simetria cilindrica axial (&sigma;): Permite rotacion torsional dependiente de la barrera termica.<br/><br/>"
                   "<b>Hibridacion sp&sup2; (Alquenos / Monomeros Vinilicos como Etileno, Estireno, Propileno):</b><br/>"
                   "&bull; Geometria: Trigonal plana coplanar | Angulo de enlace: &theta; = 120&deg;<br/>"
                   "&bull; Longitud de enlace C=C: d = 0.134 nm (1.34 &Aring;) | Energia de disociacion total: E_diss &approx; 614 kJ/mol<br/>"
                   "&bull; Estructura de enlace: 1 enlace &sigma; axial + 1 enlace &pi; lateral formado por orbitales p_z paralelos.<br/>"
                   "&bull; La densidad electronica &pi; localizada actua como un centro nucleofilico rico en electrones, susceptible a reaccionar rapidamente con radicales libres iniciadores (R&bull;) o especies electrofilicas.", formula_style)]
    ]
    t_f1 = Table(formula_1, colWidths=[522])
    t_f1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F7FAFC')),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor('#CBD5E0')),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_f1)
    story.append(Spacer(1, 4))

    story.append(Paragraph("4.2.2 Saturacion vs. Insaturacion: Criterio Termodinamico de Polimerizabilidad", h2_style))
    story.append(Paragraph(
        "Se define como <b>saturado</b> a aquel hidrocarburo donde todos los enlaces de valencia del carbono corresponden a enlaces simples &sigma; (familia de parafinas C_n H_{2n+2}). "
        "Estas moleculas son termodinamicamente estables y no pueden incorporar nuevos atomos sin ruptura previa y sustitucion (alta energia de activacion). "
        "En contraste, un hidrocarburo <b>insaturado</b> contiene dobles enlaces (alquenos, C_n H_{2n}) o triples enlaces (alquinos, C_n H_{2n-2}).<br/>"
        "<b>Analisis Termodinamico de la Reaccion de Polimerizacion (&Delta;G_p = &Delta;H_p - T&middot;&Delta;S_p):</b><br/>"
        "La conversion de un enlace doble C=C (614 kJ/mol) en dos enlaces simples C-C (2 &times; 348 = 696 kJ/mol) libera una entalpia neta exotermica "
        "de &Delta;H_p &approx; -82 a -95 kJ/mol de monomero. Sin embargo, dado que miles de moleculas independientes se unen en una sola macromolecula, "
        "se pierde una gran cantidad de grados de libertad traslacionales, resultando en &Delta;S_p &lt; 0 (&Delta;S_p &approx; -100 a -120 J/(mol&middot;K)). "
        "Por ende, existe una <b>Temperatura de Techo (Ceiling Temperature, T_c = &Delta;H_p / &Delta;S_p)</b> por encima de la cual &Delta;G_p &gt; 0 y la polimerizacion es termodinamicamente imposible (ocurre despolimerizacion termica espontanea).",
        body_style
    ))

    story.append(Paragraph("4.2.3 Isomeria Estructural y Correlacion con Propiedades de Transporte y Cohesion", h2_style))
    story.append(Paragraph(
        "Compuestos con identica formula molecular empirica pueden diferir en el orden de enlace atomico (isomeria estructural de cadena):<br/>"
        "&bull; <b>n-butano:</b> Cadena lineal no ramificada (CH3-CH2-CH2-CH3). Punto de ebullicion: T_b = -0.5 &deg;C (272.7 K).<br/>"
        "&bull; <b>isobutano (2-metilpropano):</b> Estructura ramificada cuasiesferica [CH(CH3)3]. Punto de ebullicion: T_b = -11.7 &deg;C (261.5 K).<br/>"
        "<b>Fundamento Fisicoquimico en IQ:</b> Las moleculas lineales maximizan la superficie efectiva de contacto interatomo, intensificando las fuerzas atractivas de dispersion de London. "
        "La ramificacion introduce un volumen molecular globular que reduce el area de contacto y aleja los centros electronicos promedio (r), reduciendo la cohesion intermolecular ya que el potencial de atraccion de London decae con r&macr;&sup6;.",
        body_style
    ))

    story.append(Paragraph("4.2.4 Cuantificacion de Fuerzas Intermoleculares: Densidad de Cohesion y Parametro de Hildebrand (&delta;)", h2_style))
    story.append(Paragraph(
        "En ingenieria quimica, la resistencia a la degradacion quimica, el hinchamiento en solventes y la seleccion de plastificantes se modelan mediante la "
        "<b>Densidad de Energia Cohesiva (CED)</b> y el <b>Parametro de Solubilidad de Hildebrand (&delta;)</b>:",
        body_style
    ))

    formula_2 = [
        [Paragraph("<b>Densidad de Energia Cohesiva (CED) y Parametro &delta;:</b><br/>"
                   "CED = &Delta;E_v / V_m = (&Delta;H_v - R&middot;T) / V_m<br/>"
                   "&delta; = &radic;(CED) = &radic;[(&Delta;H_v - R&middot;T) / V_m]   [Unidades: MPa^(1/2) o (cal/cm&sup3;)^(1/2)]<br/>"
                   "<b>Criterio Termodinamico de Solubilidad Polimero-Solvente (Teoria de Flory-Huggins):</b><br/>"
                   "&Delta;G_mix = &Delta;H_mix - T&middot;&Delta;S_mix &lt; 0<br/>"
                   "Debido al gigantesco tamano de las macromoleculas, la ganancia entropica de mezclado (&Delta;S_mix) es extremadamente reducida comparada con mezclas de moleculas pequenas. "
                   "Por lo tanto, la miscibilidad termodinamica espontanea exige que la entalpia de mezclado sea casi nula:<br/>"
                   "&Delta;H_mix &approx; V_total &middot; &phi;_solv &middot; &phi;_pol &middot; (&delta;_solv - &delta;_pol)&sup2;<br/>"
                   "<b>Regla de Oro en Ingenieria Quimica:</b> Ocurre disolucion o hinchamiento maximo cuando |&delta;_solv - &delta;_pol| &rarr; 0. "
                   "Si la diferencia es grande, el polimero es quimicamente inerte e insoluble en dicho fluido.", formula_style)]
    ]
    t_f2 = Table(formula_2, colWidths=[522])
    t_f2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F7FAFC')),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor('#CBD5E0')),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_f2)
    story.append(Spacer(1, 6))

    # =========================================================================
    # SECCION 4.3: LA MOLECULA POLIMERICA Y ARQUITECTURA DEL ESQUELETO
    # =========================================================================
    story.append(Paragraph("4.3 Moleculas de Polimeros: Macromoleculas, Esqueleto y Conformacion Espacial", h1_style))
    story.append(Paragraph(
        "Una molecula polimerica es una macromolecula de elevada masa molecular relativa compuesta por la reiteracion seriada de unidades estructurales denominadas unidades repetitivas.",
        body_style
    ))

    story.append(Paragraph("4.3.1 Distincion Terminologica Rigurosa: Monomero vs. Unidad Repetitiva (Mer)", h2_style))
    story.append(Paragraph(
        "&bull; <b>Monomero:</b> Molecula precursora independiente de bajo peso molecular que contiene sitios reactivos funcionales (ej. etileno gaseoso, CH2=CH2, M = 28.05 g/mol).<br/>"
        "&bull; <b>Unidad Repetitiva (Mer o Repeat Unit):</b> Grupo constitucional mas pequeno cuya repeticion sucesiva constituye la cadena. "
        "En polimeros de adicion, la masa y estequiometria del mer es exactamente identica a la del monomero (en polietileno: [-CH2-CH2-], m_0 = 28.05 g/mol). "
        "En polimeros de condensacion, la masa del mer es menor a la suma de los monomeros debido a la eliminacion estequiometrica de pequenas moleculas condensadas (ej. H2O, HCl, CH3OH).",
        body_style
    ))

    story.append(Paragraph("4.3.2 Arquitectura en Zig-Zag, Rotacion Interna y Estados Conformacionales", h2_style))
    story.append(Paragraph(
        "La representacion plana lineal a 180&deg; es una simplificacion esquematica. En la realidad molecular tridimensional, la geometria de coordinacion sp&sup3; fija el angulo C-C-C en 109.5&deg;, "
        "obligando al esqueleto de carbonos a adoptar una disposicion espacial en <b>zig-zag</b>.<br/>"
        "&bull; <b>Distancia proyectada axial por enlace:</b> d_proy = d_(C-C) &middot; sen(109.5&deg; / 2) = 0.154 nm &middot; sen(54.75&deg;) &approx; <b>0.126 nm</b>.<br/>"
        "&bull; <b>Barrera de Potencial Torsional (Conformaciones Trans vs. Gauche):</b> Alrededor de cada enlace simple &sigma; C-C, los grupos sustituyentes pueden girar. "
        "La posicion <i>trans</i> (angulo diedro &phi; = 180&deg;) maximiza la distancia interatomica y representa el estado de menor energia potencial libre. "
        "Las conformaciones <i>gauche</i> (&phi; = &plusmn;60&deg;) implican solapamiento esterico con una barrera energetica de &Delta;E &approx; 3.3 a 3.8 kJ/mol. "
        "A temperaturas ambiente y de procesamiento (donde la energia termica k_B&middot;T es comparable a &Delta;E), las cadenas experimentan fluctuaciones conformacionales continuas, "
        "adoptando la geometria termodinamica de un <b>ovillo estadistico aleatorio (random coil)</b>, cuya distancia media cuadratico-extremo es &lang;R&sup2;&rang;_0 = N &middot; l&sup2; &middot; C_&infin;, donde C_&infin; es la relacion caracteristica de Flory.",
        body_style
    ))

    story.append(Spacer(1, 6))

    # =========================================================================
    # SECCION 4.4: QUIMICA DE POLIMERIZACION Y MECANISMOS DE REACCION
    # =========================================================================
    story.append(Paragraph("4.4 La Quimica de las Moleculas Polimericas: Cinetica de Reaccion e Ingenieria de Reactores", h1_style))
    story.append(Paragraph(
        "Desde la Ingenieria de Reactores Quimicos, los procesos de sintesis se dividen en dos familias mecanisticas fundamentales con perfiles cineticos y de distribucion molecular opuestos: "
        "<b>Polimerizacion por Crecimiento en Cadena (Adicion)</b> y <b>Polimerizacion por Crecimiento en Etapas (Condensacion)</b>.",
        body_style
    ))

    story.append(Paragraph("4.4.1 Crecimiento en Cadena: Mecanismo de Radicales Libres y Deduccion Cinética QSSA", h2_style))
    story.append(Paragraph(
        "La polimerizacion radicalaria de olefinas vinilicas (CH2=CHR) comprende tres etapas elementales simultaneas:",
        body_style
    ))

    kinetics_box = [
        [Paragraph(
            "<b>1. ETAPA DE INICIACION (Termolisis homolitica del iniciador I, ej. Benzoyl Peroxide / AIBN):</b><br/>"
            "I  ---(k_d)---&gt;  2 R&bull;   [Velocidad: R_d = 2&middot;f&middot;k_d&middot;[I], donde f = factor de eficiencia radicalaria (0.3 &lt; f &lt; 0.8)]<br/>"
            "R&bull; + M  ---(k_i)---&gt;  M_1&bull;   [Dado que k_i &gt;&gt; k_d, la velocidad de iniciacion global es: R_i = 2&middot;f&middot;k_d&middot;[I]]<br/><br/>"
            "<b>2. ETAPA DE PROPAGACION (Crecimiento en cascada en microsegundos):</b><br/>"
            "M_n&bull; + M  ---(k_p)---&gt;  M_{n+1}&bull;   [Velocidad de propagacion: R_p = k_p&middot;[M&bull;]&middot;[M]]<br/><br/>"
            "<b>3. ETAPA DE TERMINACION (Desactivacion bimolecular de macro-radicales):</b><br/>"
            "&bull; Por Combinacion / Acoplamiento: M_n&bull; + M_m&bull;  ---(k_tc)---&gt;  M_{n+m} (genera una cadena inerte larga)<br/>"
            "&bull; Por Desproporcionacion: M_n&bull; + M_m&bull;  ---(k_td)---&gt;  M_n (saturado) + M_m (insaturado) (dos cadenas)<br/>"
            "Velocidad global de terminacion: R_t = 2&middot;k_t&middot;[M&bull;]&sup2;   (donde k_t = k_tc + k_td)<br/><br/>"
            "<b>DEDUCCION RIGUROSA BAJO LA HIPOTESIS DEL ESTADO CUASI-ESTACIONARIO (QSSA):</b><br/>"
            "Para macro-radicales intermedios de alta reactividad, su concentracion permanece constante en estado estacionario:<br/>"
            "d[M&bull;]/dt = R_i - R_t = 0  &rArr;  2&middot;f&middot;k_d&middot;[I] = 2&middot;k_t&middot;[M&bull;]&sup2;<br/>"
            "<b>[M&bull;] = &radic;[ (f&middot;k_d&middot;[I]) / k_t ]</b><br/><br/>"
            "Sustituyendo [M&bull;] en la velocidad de consumo de monomero (R_p):<br/>"
            "<b>R_p = - d[M]/dt = k_p &middot; [M] &middot; &radic;[ (f&middot;k_d&middot;[I]) / k_t ]</b><br/>"
            "&bull; Orden cinetico 1 con respecto a la concentracion de monomero [M].<br/>"
            "&bull; Orden cinetico 0.5 (raiz cuadrada) con respecto a la concentracion de iniciador [I].<br/><br/>"
            "<b>LONGITUD DE CADENA CINETICA (&nu;) Y GRADO DE POLIMERIZACION (X_n):</b><br/>"
            "&nu; = R_p / R_i = (k_p &middot; [M]) / [ 2 &middot; &radic;(f&middot;k_d&middot;k_t&middot;[I]) ]<br/>"
            "&bull; Si la terminacion ocurre 100% por combinacion: X_n = 2&middot;&nu;<br/>"
            "&bull; Si la terminacion ocurre 100% por desproporcionacion: X_n = &nu;",
            formula_style
        )]
    ]
    t_kin = Table(kinetics_box, colWidths=[522])
    t_kin.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F7FAFC')),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor('#CBD5E0')),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_kin)
    story.append(Spacer(1, 6))

    story.append(Paragraph("4.4.2 Crecimiento en Etapas (Condensacion) y Deduccion de la Ecuacion de Carothers", h2_style))
    story.append(Paragraph(
        "A diferencia del crecimiento en cadena, en la polimerizacion por etapas cualquier especie quimica con grupos terminales reactivos "
        "(monomero, dimero, trimero, macromolecula) puede reaccionar con cualquier otra especie en cualquier momento. Un ejemplo industrial representativo "
        "es la sintesis del <b>Nylon 6,6</b> por policondensacion de hexametilendiamina y acido adipico:<br/>"
        "n H2N-(CH2)6-NH2 + n HOOC-(CH2)4-COOH  &rarr;  [-NH-(CH2)6-NH-CO-(CH2)4-CO-]_n + 2n H2O",
        body_style
    ))

    carothers_box = [
        [Paragraph(
            "<b>DEDUCCION MATEMATICA DE LA ECUACION DE CAROTHERS PARA SISTEMAS BIFUNCIONALES (f = 2):</b><br/>"
            "Sea N_0 el numero total de moleculas monomericas iniciales cargadas al reactor a tiempo t = 0.<br/>"
            "Dado que cada molecula es bifuncional (f = 2), el numero total de grupos funcionales iniciales es 2&middot;N_0.<br/>"
            "A un tiempo de reaccion t, restan N moleculas macromoleculares en la mezcla. Cada union quimica entre dos moleculas "
            "consume 2 grupos funcionales y reduce el conteo total de moleculas en 1. Por ende, los grupos consumidos son 2&middot;(N_0 - N).<br/>"
            "Definiendo la conversion fraccionaria de grupos reactivos (p):<br/>"
            "p = [2&middot;(N_0 - N)] / (2&middot;N_0) = (N_0 - N) / N_0   &rArr;   N = N_0 &middot; (1 - p)<br/>"
            "El grado de polimerizacion promedio en numero (X_n) se define como el numero medio de unidades monomericas por cadena:<br/>"
            "<b>X_n = N_0 / N = 1 / (1 - p)</b><br/><br/>"
            "<b>TABLA DE SENSIBILIDAD CONVERSION VS. PESO MOLECULAR (IMPACTO EN REACTORES):</b><br/>"
            "&bull; p = 0.50 (50% conversion)   &rArr;  X_n = 2 (solo dimeros, producto liquido de viscosidad baja)<br/>"
            "&bull; p = 0.90 (90% conversion)   &rArr;  X_n = 10 (oligomeros sin integridad mecanica)<br/>"
            "&bull; p = 0.98 (98% conversion)   &rArr;  X_n = 50 (inicio fragil de polimero util)<br/>"
            "&bull; p = 0.99 (99% conversion)   &rArr;  X_n = 100 (resistencia mecanica estructural adecuada)<br/>"
            "&bull; p = 0.999 (99.9% conversion) &rArr; X_n = 1000 (altas prestaciones tecnicas)<br/>"
            "<b>Regla de Operacion Industrial en IQ:</b> Para alcanzar p &gt; 0.99, el reactor de policondensacion debe operar a vacio extremo "
            "(evaporadores de pelicula descendente o reactores con venteo forzado) para desplazar el equilibrio de esterificacion/amidacion retirando continuamente el agua subproducto.",
            formula_style
        )]
    ]
    t_car = Table(carothers_box, colWidths=[522])
    t_car.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F7FAFC')),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor('#CBD5E0')),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_car)
    story.append(Spacer(1, 6))

    story.append(Paragraph("4.4.3 Funcionalidad Monomérica, Polímeros Red y Punto de Gel de Carothers", h2_style))
    story.append(Paragraph(
        "La <b>funcionalidad (f)</b> cuantifica el numero de sitios de enlace covalente activo que un monomero puede formar con otros:<br/>"
        "&bull; <b>Monomeros Bifuncionales (f = 2):</b> Generan macromoleculas lineales o anillos cerrados (termoplasticos que funden y se disuelven).<br/>"
        "&bull; <b>Monomeros Polifuncionales (f &ge; 3):</b> Generan puntos de ramificacion tridimensional que interconectan las cadenas en una red macromolecular infinita continua (termoestables).",
        body_style
    ))

    gel_box = [
        [Paragraph(
            "<b>DEDUCCION DEL PUNTO CRITICO DE GELIFICACION DE CAROTHERS (p_c):</b><br/>"
            "Para un sistema con funcionalidad promedio ponderada f_prom = &Sigma; (N_i &middot; f_i) / &Sigma; N_i :<br/>"
            "Numero inicial de grupos reactivos: N_0 &middot; f_prom. Moleculas remanentes: N = N_0 - (N_0 &middot; f_prom &middot; p) / 2.<br/>"
            "X_n = N_0 / N = 2 / (2 - p &middot; f_prom)<br/>"
            "El punto de gel teorico ocurre cuando el grado de polimerizacion promedio en numero tiende a infinito (X_n &rarr; &infin;):<br/>"
            "2 - p_c &middot; f_prom = 0   &rArr;   <b>p_c = 2 / f_prom</b><br/>"
            "<b>Consecuencia Critica en Diseno de Procesos IQ:</b> En p_c se produce una transformacion de fase reologica brusca: "
            "la viscosidad se hace infinita (&eta; &rarr; &infin;). La mezcla ya no fluye ni puede bombearse. Si esto ocurre dentro de un reactor por lotes convencional, "
            "el agitador colapsa y la masa solidifica irreversiblemente, arruinando el equipo. Por eso, termoestables como la Baquelita o resinas epoxicas "
            "se formulan como prepolimeros con p &lt; p_c y el curado final se efectua in-situ dentro del molde caliente.",
            formula_style
        )]
    ]
    t_gel = Table(gel_box, colWidths=[522])
    t_gel.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F7FAFC')),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor('#CBD5E0')),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_gel)
    story.append(Spacer(1, 10))

    # Page Break for Table of Engineering Polymers
    story.append(PageBreak())

    # =========================================================================
    # TABLA TECNICA DE LOS 10 POLIMEROS FUNDAMENTALES (CALLISTER ENRIQUECIDO)
    # =========================================================================
    story.append(Paragraph("Tabla Tecnica Maestra: 10 Polimeros Fundamentales en Ingenieria", h1_style))
    story.append(Paragraph(
        "Correlacion exhaustiva de unidad repetitiva, masa molar del mer (m_0), fuerzas intermoleculares predominantes, temperaturas caracteristicas (Tg, Tm) "
        "y aplicaciones clave en diseno de plantas y procesos quimicos:",
        body_style
    ))

    headers = [
        Paragraph("<b>Polimero<br/>(Acronimo)</b>", table_header),
        Paragraph("<b>Formula Unidad Repetitiva (Mer)</b>", table_header),
        Paragraph("<b>m₀<br/>(g/mol)</b>", table_header),
        Paragraph("<b>Fuerzas Intermoleculares Dominantes</b>", table_header),
        Paragraph("<b>T_g / T_m<br/>(&deg;C)</b>", table_header),
        Paragraph("<b>Aplicacion Critica en Ingenieria Quimica / Procesos</b>", table_header)
    ]

    polymer_rows = [
        [
            Paragraph("<b>Polietileno</b><br/>(PE)", table_cell),
            Paragraph("[-CH2 - CH2-]", table_cell_code),
            Paragraph("28.05", table_cell),
            Paragraph("Dispersion de London. Cadenas apolares de alta simetria y facil plegamiento cristalino.", table_cell),
            Paragraph("-110 / 115-137", table_cell),
            Paragraph("Tuberias de gas/agua a presion (HDPE), geomembranas de lixiviacion e inertizacion de reactores.", table_cell)
        ],
        [
            Paragraph("<b>Poli(cloruro de vinilo)</b><br/>(PVC)", table_cell),
            Paragraph("[-CH2 - CH(Cl)-]", table_cell_code),
            Paragraph("62.50", table_cell),
            Paragraph("Dipolo-dipolo permanente muy fuerte debido a la electronegatividad del Cl.", table_cell),
            Paragraph("87 / 212 (dec)", table_cell),
            Paragraph("Conduccion de acidos concentrados (HCl), celda de cloro-alcali y bandejas quimicamente resistentes.", table_cell)
        ],
        [
            Paragraph("<b>Politetrafluoro-etileno</b><br/>(PTFE / Teflon)", table_cell),
            Paragraph("[-CF2 - CF2-]", table_cell_code),
            Paragraph("100.02", table_cell),
            Paragraph("London debiles por baja polarizabilidad del Fluor; apantallamiento esterico total del esqueleto.", table_cell),
            Paragraph("-97 / 327", table_cell),
            Paragraph("Empaquetaduras de valvulas criogenicas, sellos mecanicos y juntas universales para fluidos corrosivos.", table_cell)
        ],
        [
            Paragraph("<b>Polipropileno</b><br/>(PP)", table_cell),
            Paragraph("[-CH2 - CH(CH3)-]", table_cell_code),
            Paragraph("42.08", table_cell),
            Paragraph("Dispersion de London; impedimento esterico moderado del metilo colgante.", table_cell),
            Paragraph("-10 / 165-175", table_cell),
            Paragraph("Tanques de decapado acido, telas para filtros prensa y recipientes esterilizables en autoclave.", table_cell)
        ],
        [
            Paragraph("<b>Poliestireno</b><br/>(PS)", table_cell),
            Paragraph("[-CH2 - CH(C6H5)-]", table_cell_code),
            Paragraph("104.15", table_cell),
            Paragraph("London e interacciones &pi;-&pi; aromaticas. El grupo fenilo voluminoso aporta alta rigidez.", table_cell),
            Paragraph("100 / Amorfo", table_cell),
            Paragraph("Aislamiento termico criogenico (EPS), columnas empacadas de laboratorio y resinas sulfonadas de intercambio ionico.", table_cell)
        ],
        [
            Paragraph("<b>Poli(metacrilato de metilo)</b> (PMMA)", table_cell),
            Paragraph("[-CH2 - C(CH3)(COOCH3)-]", table_cell_code),
            Paragraph("100.12", table_cell),
            Paragraph("Dipolo-dipolo polar del ester + impedimento esterico severo de carbono cuaternario.", table_cell),
            Paragraph("105 / Amorfo", table_cell),
            Paragraph("Mirillas de visualizacion en reactores quimicos de presion moderada y cubiertas opticas de sensores.", table_cell)
        ],
        [
            Paragraph("<b>Baquelita</b><br/>(Fenol-Formaldehido)", table_cell),
            Paragraph("Red condensada de anillos fenolicos unidos por puentes metileno [-CH2-]", table_cell_code),
            Paragraph("Variable (Red)", table_cell),
            Paragraph("Red tridimensional infinita unida por enlaces covalentes C-C primarios + puentes de H.", table_cell),
            Paragraph("No funde (Degrada &gt;300)", table_cell),
            Paragraph("Aislantes termoelectricos de alta estabilidad, pastillas de freno y adhesivos resistentes a solventes organicos agresivos.", table_cell)
        ],
        [
            Paragraph("<b>Nylon 6,6</b><br/>(Poliamida)", table_cell),
            Paragraph("[-NH(CH2)6NH - CO(CH2)4CO-]", table_cell_code),
            Paragraph("226.32", table_cell),
            Paragraph("<b>Puentes de Hidrogeno densos</b> intercatenarios entre grupos amida N-H&middot;&middot;&middot;O=C.", table_cell),
            Paragraph("50 / 265", table_cell),
            Paragraph("Engranajes autolubricantes de plantas quimicas, mangueras hidraulicas y telas filtrantes de alta presion.", table_cell)
        ],
        [
            Paragraph("<b>Poli(tereftalato de etileno)</b> (PET)", table_cell),
            Paragraph("[-O-CH2CH2-O - CO(C6H4)CO-]", table_cell_code),
            Paragraph("192.17", table_cell),
            Paragraph("Dipolo-dipolo e interacciones &pi;-&pi; entre anillos tereftalatos rigidos en el esqueleto.", table_cell),
            Paragraph("69 / 260", table_cell),
            Paragraph("Peliculas barrera contra permeabilidad de gases (O2, CO2), tanques de presurizacion y geotextiles.", table_cell)
        ],
        [
            Paragraph("<b>Policarbonato</b><br/>(PC)", table_cell),
            Paragraph("[-O-C6H4-C(CH3)2-C6H4-O - CO-]", table_cell_code),
            Paragraph("254.28", table_cell),
            Paragraph("Dipolo-dipolo polar del carbonato + anillos de bisfenol A rigidos que impiden cristalizacion.", table_cell),
            Paragraph("145 / Amorfo", table_cell),
            Paragraph("Escudos de proteccion en plantas piloto contra explosiones, rotametros y carcasas de bombas al vacio.", table_cell)
        ]
    ]

    t_poly = Table([headers] + polymer_rows, colWidths=[70, 95, 45, 105, 60, 147])
    t_poly.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F2942')),
        ('ALIGN', (0,0), (-1,0), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E0')),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F7FAFC')])
    ]))
    story.append(t_poly)
    story.append(Spacer(1, 10))

    # =========================================================================
    # SECCION: PROBLEMAS NUMERICOS DE INGENIERIA QUIMICA RESUELTOS PASO A PASO
    # =========================================================================
    story.append(Paragraph("Ejercicios Numericos de Calculo Riguroso (Nivel Licenciatura IQ)", h1_style))
    story.append(Paragraph(
        "Tres casos cuantitativos resueltos que ilustran la aplicacion de balances estequiometricos, cineticos y termodinamicos:",
        body_style
    ))

    # Problema 1: Carothers y Punto de Gel
    story.append(Paragraph("<b>Problema 1: Prediccion Estequiometrica del Punto de Gelificacion (p_c) en Resinas Alquidicas</b>", h2_style))
    p1_text = (
        "<b>Enunciado:</b> En un reactor batch se sintetiza una resina cargando 2.0 moles de anhidrido ftalico (bifuncional, f_A = 2) "
        "y 1.0 mol de glicerol (trifuncional, f_B = 3). Calcule la funcionalidad promedio del sistema (f_prom), la conversion teorica en el punto de gel (p_c) "
        "e interprete la relevancia reologica y de seguridad operativa.<br/><br/>"
        "<b>Solucion Analitica Paso a Paso:</b><br/>"
        "1. <i>Balance molar de moleculas y grupos funcionales:</i><br/>"
        "&bull; Moles de moleculas monomericas iniciales: N_0 = 2.0 + 1.0 = 3.0 moles.<br/>"
        "&bull; Equivalentes aportados por el anhidrido ftalico: 2.0 moles &times; 2 grupos = 4.0 equivalentes de carboxilo.<br/>"
        "&bull; Equivalentes aportados por el glicerol: 1.0 mol &times; 3 grupos = 3.0 equivalentes de hidroxilo.<br/>"
        "&bull; Total de equivalentes funcionales en el reactor: E_0 = 4.0 + 3.0 = 7.0 equivalentes.<br/><br/>"
        "2. <i>Calculo de la funcionalidad promedio (f_prom):</i><br/>"
        "f_prom = (Total de equivalentes funcionales) / (Total de moles de monomero) = 7.0 / 3.0 &approx; <b>2.333</b><br/><br/>"
        "3. <i>Calculo del punto de gel critico de Carothers:</i><br/>"
        "p_c = 2 / f_prom = 2 / (7 / 3) = 6 / 7 &approx; <b>0.8571 (85.71% de avance en la conversion)</b>.<br/><br/>"
        "<b>Dictamen Tecnico de Planta:</b> Al alcanzar el 85.71% de conversion de grupos funcionales, el grado de polimerizacion promedio en numero diverge hacia infinito (X_n &rarr; &infin;). "
        "Se forma una red tridimensional que engloba todo el volumen del reactor, la viscosidad salta discontinuamente a infinito y la mezcla pierde toda fluidez. "
        "Para evitar la perdida destructiva del reactor, el protocolo de operacion exige apagar el calentamiento e inyectar inhibidores termicos antes de que la conversion supere el 80%."
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

    # Problema 2: Cinetica de Radicales Libres
    story.append(Paragraph("<b>Problema 2: Calculo de Velocidad de Polimerizacion (R_p) y Longitud Cinetica (&nu;) en un Reactor Continuo</b>", h2_style))
    p2_text = (
        "<b>Enunciado:</b> Se polimeriza estireno a 60 &deg;C en fase liquida empleando peroxido de benzoilo (I) como iniciador. "
        "Las concentraciones en el reactor homogeneo son [M] = 8.5 mol/L y [I] = 0.040 mol/L. Las constantes cineticas reportadas a 60 &deg;C son:<br/>"
        "k_d = 3.2 &times; 10&macr;&sup6; s&macr;&sup1;, f = 0.60, k_p = 176 L/(mol&middot;s), k_t = 3.6 &times; 10&sup7; L/(mol&middot;s). "
        "Calcule la concentracion estacionaria de macro-radicales [M&bull;], la velocidad instantanea de polimerizacion (R_p) y la longitud de cadena cinetica (&nu;).<br/><br/>"
        "<b>Solucion Analitica Paso a Paso:</b><br/>"
        "1. <i>Concentracion estacionaria de macro-radicales bajo la hipotesis QSSA:</i><br/>"
        "[M&bull;] = &radic;[ (f &middot; k_d &middot; [I]) / k_t ] = &radic;[ (0.60 &times; 3.2&times;10&macr;&sup6; s&macr;&sup1; &times; 0.040 mol/L) / (3.6&times;10&sup7; L/(mol&middot;s)) ]<br/>"
        "[M&bull;] = &radic;[ (7.68 &times; 10&macr;&sup8;) / (3.6 &times; 10&sup7;) ] = &radic;(2.133 &times; 10&macr;&sup1;&sup5;) &approx; <b>4.619 &times; 10&macr;&sup8; mol/L</b><br/><br/>"
        "2. <i>Velocidad volumetrica de consumo de monomero (R_p):</i><br/>"
        "R_p = k_p &middot; [M&bull;] &middot; [M] = 176 L/(mol&middot;s) &times; 4.619 &times; 10&macr;&sup8; mol/L &times; 8.5 mol/L &approx; <b>6.91 &times; 10&macr;&sup5; mol/(L&middot;s)</b> [o 0.248 mol/(L&middot;h)]<br/><br/>"
        "3. <i>Longitud de cadena cinetica (&nu;):</i><br/>"
        "Velocidad de generacion de radicales: R_i = 2&middot;f&middot;k_d&middot;[I] = 2 &times; 0.60 &times; 3.2&times;10&macr;&sup6; &times; 0.040 = 1.536 &times; 10&macr;&sup7; mol/(L&middot;s)<br/>"
        "&nu; = R_p / R_i = (6.91 &times; 10&macr;&sup5; mol/(L&middot;s)) / (1.536 &times; 10&macr;&sup7; mol/(L&middot;s)) &approx; <b>450 unidades repetitivas</b>.<br/>"
        "Dado que para el estireno a 60 &deg;C la terminacion es predominantemente por combinacion bimolecular (k_tc &approx; k_t):<br/>"
        "<b>X_n = 2 &middot; &nu; = 2 &times; 450 = 900</b>. Masa molar promedio en numero: M_n = X_n &middot; m_0 = 900 &times; 104.15 g/mol = <b>93,735 g/mol</b>."
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
    story.append(Spacer(1, 6))

    # Problema 3: Termodinámica de Solubilidad de Polímeros
    story.append(Paragraph("<b>Problema 3: Criterio Termodinamico de Solubilidad de Hildebrand y Compatibilidad con Fluidos Industriales</b>", h2_style))
    p3_text = (
        "<b>Enunciado:</b> Se debe seleccionar una tuberia para transportar tetrahidrofurano (THF, &delta; = 19.4 MPa^(1/2)) en una planta farmaceutica. "
        "Se evaluan tuberias de Polietileno (&delta;_PE = 16.2 MPa^(1/2)) y Poli(cloruro de vinilo) (&delta;_PVC = 19.8 MPa^(1/2)). "
        "Prediga mediante el criterio de calor de mezclado de Hildebrand (&Delta;H_mix) cual polimero experimentara hinchamiento / disolucion y cual resistira el solvente.<br/><br/>"
        "<b>Solucion Termodinamica:</b><br/>"
        "1. <i>Diferencia de parametros de solubilidad cuadraticos (&Delta;&delta;&sup2;):</i><br/>"
        "&bull; Para el par PVC - THF: |&delta;_THF - &delta;_PVC| = |19.4 - 19.8| = <b>0.4 MPa^(1/2)</b>  &rArr;  (&Delta;&delta;)&sup2; = 0.16 MPa.<br/>"
        "&bull; Para el par PE - THF: |&delta;_THF - &delta;_PE| = |19.4 - 16.2| = <b>3.2 MPa^(1/2)</b>  &rArr;  (&Delta;&delta;)&sup2; = 10.24 MPa.<br/><br/>"
        "2. <i>Evaluacion de la energia libre de Gibbs de mezclado (&Delta;G_mix):</i><br/>"
        "Dado que (&Delta;&delta;)&sup2;_PVC &approx; 0, el termino entalpico &Delta;H_mix es cercano a cero. La pequenisima ganancia entropica &Delta;S_mix es suficiente "
        "para que &Delta;G_mix &lt; 0. Por ende, el THF disolvera o hinchara severamente al PVC, destruyendo la integridad estructural de la tuberia.<br/>"
        "Por el contrario, para el PE, (&Delta;&delta;)&sup2; es 64 veces mayor, lo que hace que &Delta;H_mix &gt;&gt; 0, superando ampliamente el termino entropico T&middot;&Delta;S_mix. "
        "Por tanto, &Delta;G_mix &gt; 0: el PE es termodinamicamente insoluble en THF. Ademas, el caracter semicristalino del PE aporta una barrera energetica adicional "
        "(&Delta;H_fusion) que impide la penetracion del solvente en las zonas cristalinas."
    )
    t_p3 = Table([[Paragraph(p3_text, body_style)]], colWidths=[522])
    t_p3.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#EDF2F7')),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor('#CBD5E0')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_p3)
    story.append(Spacer(1, 10))

    # =========================================================================
    # SECCION: PREGUNTAS TRAMPA Y DEFENSA CONCEPTUAL ANTE EL PROFESOR
    # =========================================================================
    story.append(Paragraph("Cuestionario de Defensa Conceptual y Preguntas Tipicas de Examen en IQ", h1_style))
    story.append(Paragraph(
        "Respuestas argumentadas rigurosamente frente a preguntas inquisitivas frecuentes de comites evaluadores:",
        body_style
    ))

    q_data = [
        ("1. ¿Por que en la polimerizacion por adicion se forman cadenas de muy alto peso molecular desde el inicio (conversion < 1%), mientras que en condensacion a p = 0.90 el producto es inutil?",
         "En crecimiento en cadena, la constante de propagacion k_p es tan grande (~10²-10⁴ L/(mol·s)) que una vez iniciado un radical libre, este adiciona miles de monomeros en fracciones de milisegundo antes de terminar. A conversion baja coexisten monomeros intactos y cadenas gigantes ya muertas. En cambio, en condensacion la reactividad de los grupos funcionales es independiente del tamano de la molecula (Principio de Flory); al inicio casi todos los monomeros se consumen para formar dimeros, trimeros y oligomeros. Para que estos oligomeros se unan entre si y alcancen longitudes macromoleculares (X_n > 100), se requiere agotar estadisticamente mas del 99% de todos los extremos reactivos (p > 0.99 segun Carothers)."),
        ("2. ¿Por que el PTFE (Teflon) tiene una temperatura de fusion tan elevada (Tm = 327 °C) a pesar de que el fluor es muy electronegativo y sus fuerzas de London son bajas?",
         "El radio de van der Waals del fluor (1.47 Å) es considerablemente mayor que el del hidrogeno (1.20 Å). Al estar cada carbono del esqueleto sp³ unido a dos atomos de fluor, la repulsion esterica interatomica impide que la cadena adopte conformaciones torcidas; en su lugar, la molecula se ve forzada a formar una varilla rigida en helice cilindrica donde los atomos de fluor forman una coraza externa impenetrable. La enorme rigidez conformacional de la cadena minimiza la entropia de fusion conformacional en estado fundido (ΔS_m baja). Segun la termodinamica clasica T_m = ΔH_m / ΔS_m; al ser ΔS_m extraordinariamente pequena, la temperatura de fusion se eleva a valores excepcionales."),
        ("3. ¿Que es el efecto Trommsdorff-Norrish (efecto gel) y cual es su peligro en reactores industriales?",
         "A conversiones moderadas en polimerizaciones en masa o concentradas, el medio reaccionante se vuelve altamente viscoso por la acumulacion de macromoleculas entrelazadas. Los radicales libres macromoleculares (M_n•) ven impedida su difusion traslacional, provocando una caida abrupta de varios ordenes de magnitud en la constante de terminacion bimolecular k_t. Sin embargo, el monomero (M), al ser pequeno, sigue difundiendo libremente hacia los centros activos (k_p permanece constante). Como consecuencia de la ecuacion R_p = k_p [M] √(f k_d [I] / k_t), al colapsar k_t en el denominador, la velocidad de reaccion R_p se autoacelera violentamente. Como la polimerizacion es altamente exotermica (ΔH_p ≈ -80 kJ/mol), se genera un fenomeno de embalamiento termico (thermal runaway) que puede sobrepresurizar y destruir el reactor si el sistema de enfriamiento no esta sobredisenado.")
    ]

    for q_title, q_ans in q_data:
        q_flow = [
            Paragraph(f"<b>{q_title}</b>", h2_style),
            Paragraph(q_ans, body_style)
        ]
        story.append(KeepTogether(q_flow))
        story.append(Spacer(1, 4))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully built: {filename}")

if __name__ == "__main__":
    build_pdf()
