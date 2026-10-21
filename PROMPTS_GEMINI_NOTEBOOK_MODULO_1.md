# GUÍA DE PROMPTS RIGUROSOS PARA GEMINI NOTEBOOK / NOTEBOOKLM
## Módulo 1: Estructura, Termodinámica y Mecanismos de Polimerización (Subtemas 4.1 a 4.4)
### Licenciatura en Ingeniería Química | Basado en W.D. Callister y Principios de Procesos Químicos

---

## 1. PROMPT MAESTRO DE CONFIGURACIÓN (System Prompt para NotebookLM)
> **Instrucciones de uso:** Copia y pega este prompt al iniciar tu interacción en el chat de NotebookLM una vez que hayas subido el archivo `Modulo_1_Polimeros_Estructura_Quimica_IQ.pdf`. Este prompt calibra el tono, el nivel de exigencia académica y la perspectiva de Ingeniería Química.

```text
Actúa como un Catedrático Titular y Doctor en Ciencia de Materiales e Ingeniería de Reactores de Polimerización, evaluando a un estudiante de nivel avanzado de la Licenciatura en Ingeniería Química.

DIRECTRICES OBLIGATORIAS DE RESPUESTA:
1. RIGOR FÍSICO-QUÍMICO Y MATEMÁTICO: Queda terminantemente prohibido dar explicaciones simplistas, superficiales o meramente divulgativas. Cada concepto debe conectarse con sus fundamentos termodinámicos (energía libre de Gibbs, entalpía de enlace, entropía conformacional, teoría de Flory-Huggins, densidad de energía cohesiva), cinéticos (velocidades de reacción, aproximación QSSA, constantes de velocidad, órdenes de reacción) y de fenómenos de transporte/reología.
2. DEDUCCIONES Y BALANCES EXPLÍCITOS: Siempre que se mencione una ecuación (como la velocidad de polimerización Rp, longitud de cadena cinética ν, o la ecuación de Carothers y el punto de gel pc), debes desglosar la deducción matemática completa a partir de balances de materia y principios estequiométricos/cinéticos, definiendo cada variable y sus unidades en el Sistema Internacional.
3. CONEXIÓN DIRECTA CON PLANTAS QUÍMICAS: Relaciona cada fenómeno microscópico o estructural con su impacto en operaciones y equipos de ingeniería química (reactores CSTR, PFR, reactores batch, desvolatilizadores a vacío, ensuciamiento/fouling, riesgo de embalamiento térmico por efecto Trommsdorff, y compatibilidad de materiales con solventes y ácidos).
4. PRECISIÓN TERMINOLÓGICA IUPAC: Mantén una distinción inflexible entre conceptos análogos (monómero vs. mer; conformación vs. configuración; termoplástico vs. termoestable; polidispersidad vs. monodispersidad).
5. FORMATO DE SALIDA: Emplea notación matemática clara en LaTeX ($...$ y $$...$$), esquemas de flujo o tablas comparativas cuando resulte pertinente, y resalta las implicaciones operativas en recuadros de análisis crítico.
```

---

## 2. PROMPT ESPECÍFICO — SUBTEMA 4.1: INTRODUCCIÓN A LAS MACROMOLÉCULAS Y EVOLUCIÓN
> **Objetivo:** Analizar la naturaleza macromolecular desde el balance de enlaces y la termodinámica de polidispersidad frente a metales y cerámicos.

```text
Con base en la fuente cargada, realiza un análisis comparativo riguroso entre polímeros sintéticos, metales y cerámicos desde la óptica de la Ingeniería Química:

1. Explica por qué, a diferencia de sustancias de bajo peso molecular que poseen masa molar unívoca, los polímeros sintéticos son intrínsecamente polidispersos y cómo esto condiciona sus propiedades reológicas y mecánicas.
2. Analiza la dualidad estructural: ¿cuál es la función de los enlaces covalentes sigma de la cadena principal frente a las interacciones secundarias (London, dipolo-dipolo, puentes de hidrógeno) en los fenómenos de fluencia viscosa y solubilidad?
3. Fundamenta mediante balances de densidad y resistencia específica por qué los polímeros han sustituido al acero y a los cerámicos en el diseño de reactores químicos revestidos, tuberías de transporte de electrolitos corrosivos y membranas de separación molecular.
```

---

## 3. PROMPT ESPECÍFICO — SUBTEMA 4.2: HIDROCARBUROS, HIBRIDACIÓN Y TERMODINÁMICA INTERMOLECULAR
> **Objetivo:** Dominar la mecánica cuántica de los enlaces C-C, termodinámica de polimerización (entalpía vs. entropía) y el parámetro de solubilidad de Hildebrand.

```text
Analiza con rigor fisicoquímico las moléculas de hidrocarburos como base estructural de los polímeros:

1. Compara las hibridaciones orbitales sp³ y sp² del carbono en términos de:
   - Geometría espacial y ángulos de enlace.
   - Longitud y energía de disociación de enlace (kJ/mol).
   - Movilidad rotacional: explica por qué el enlace sigma sp³ permite torsión conformacional mientras que el enlace pi sp² la bloquea rígidamente.
2. Desarrolla la termodinámica de la polimerización por adición (ΔGp = ΔHp - T·ΔSp):
   - ¿Por qué la conversión de C=C a C-C es exotérmica (ΔHp < 0)?
   - ¿Por qué el cambio entrópico es severamente negativo (ΔSp < 0)?
   - Deduce analíticamente la ecuación de la Temperatura de Techo (Ceiling Temperature, Tc) y explica qué ocurre operacionalmente en un reactor si se supera este valor.
3. Isomería y Fuerzas de London:
   - Explica por qué el n-butano hierve a -0.5 °C mientras que el isobutano hierve a -11.7 °C a partir del potencial de Lennard-Jones y la dependencia r⁻⁶ de las fuerzas de dispersión.
4. Criterio de Solubilidad de Hildebrand:
   - Define la Densidad de Energía Cohesiva (CED) y el parámetro δ.
   - Aplica la teoría de Flory-Huggins para justificar por qué la entalpía de mezclado ΔHmix ≈ V·φ₁·φ₂·(δ₁ - δ₂)² determina la compatibilidad química o insolubilidad de un polímero frente a solventes industriales.
```

---

## 4. PROMPT ESPECÍFICO — SUBTEMA 4.3: LA MOLÉCULA POLIMÉRICA Y ARQUITECTURA DEL ESQUELETO
> **Objetivo:** Clarificar la geometría molecular 3D, el concepto de mer, las barreras de rotación interna (trans vs. gauche) y el modelo de ovillo estadístico.

```text
Examina la arquitectura espacial de las macromoléculas con base en el documento técnico:

1. Establece la distinción termodinámica y estequiométrica rigurosa entre "monómero" y "unidad repetitiva (mer)", contrastando el caso del polietileno (adición) frente al Nylon 6,6 (policondensación).
2. Geometría en zig-zag:
   - Demuestra matemáticamente que la distancia proyectada por enlace C-C sp³ a lo largo del eje macromolecular es d_proy = 0.154 nm · sen(54.75°) ≈ 0.126 nm, y no 0.154 nm.
3. Barreras Torsionales y Conformación:
   - Grafica conceptualmente el perfil de energía potencial frente al ángulo diedro de rotación φ.
   - Explica la diferencia de energía libre entre el estado trans (anti) y los estados gauche (+60° y -60°).
   - Explica por qué a temperatura ambiente la cadena se comporta como un "ovillo estadístico aleatorio" (random coil) y define el significado físico de la relación característica de Flory (C_∞).
```

---

## 5. PROMPT ESPECÍFICO — SUBTEMA 4.4: CINÉTICA DE POLIMERIZACIÓN, CAROTHERS Y GELIFICACIÓN
> **Objetivo:** Resolver y explicar los modelos matemáticos de reactores de polimerización (QSSA para radicales libres, Carothers para condensación y punto de gel pc).

```text
Actúa como experto en ingeniería de la reacción química y desarrolla las siguientes deducciones analíticas completas:

1. CINÉTICA DE CRECIMIENTO EN CADENA POR RADICALES LIBRES:
   - Plantea los mecanismos elementales de Iniciación (térmica con eficiencia f), Propagación y Terminación (combinación vs. desproporción).
   - Aplica la Hipótesis del Estado Cuasi-Estacionario (QSSA) para los macro-radicales [M•] y deduce formalmente que:
     Rp = kp · [M] · √((f · kd · [I]) / kt)
   - Deduce la expresión de la longitud de cadena cinética (ν) y explica cómo calcular el grado de polimerización Xn según el mecanismo de terminación dominante.
   - Explica el Efecto Trommsdorff-Norrish (efecto gel): ¿por qué colapsa kt mientras kp permanece casi constante, y cuál es el riesgo de embalamiento térmico en el reactor?

2. CINÉTICA DE CRECIMIENTO EN ETAPAS Y ECUACIÓN DE CAROTHERS:
   - Deduce paso a paso la ecuación de Carothers para sistemas bifuncionales estequiométricos: Xn = 1 / (1 - p).
   - Construye una tabla de análisis de sensibilidad que relacione la conversión p (0.50, 0.90, 0.95, 0.98, 0.99, 0.999) con Xn.
   - ¿Qué exigencias de diseño impone esta relación sobre el control estequiométrico y los sistemas de desvolatilización a alto vacío en reactores industriales de policondensación?

3. PUNTO DE GEL DE CAROTHERS:
   - Deduce la expresión del punto crítico de gelificación: pc = 2 / f_prom.
   - Resuelve el caso de una mezcla con 2 moles de monómero bifuncional y 1 mol de monómero trifuncional.
   - Describe la discontinuidad reológica en pc (viscosidad infinita) y cómo condiciona la operación de moldeo o apagado de la reacción.
```

---

## 6. PROMPT PARA SIMULACIÓN DE EXAMEN ORAL / DEFENSA ANTE EL PROFESOR
> **Objetivo:** Entrenar activamente respondiendo preguntas trampa y cuestionamientos de examen típicos de profesores de Ingeniería Química.

```text
Inicia una simulación de EXAMEN ORAL RIGUROSO sobre el Módulo 1 (Callister 4.1 a 4.4).

REGLAS DE LA SIMULACIÓN:
1. Hazme UNA SOLA PREGUNTA a la vez. No me des la respuesta de inmediato.
2. La pregunta debe ser de alto nivel analítico, orientada a evaluar si comprendo la fisicoquímica y los cálculos de ingeniería (por ejemplo: preguntas trampa sobre por qué conversiones del 90% en condensación no sirven, cómo afecta la rigidez conformacional del PTFE a su punto de fusión Tm = 327 °C, o cómo predecir si un polímero resistirá un solvente usando parámetros de Hildebrand).
3. Espera a que yo responda.
4. Tras mi respuesta, evalúame con una calificación del 0 al 10, señalando con precisión quirúrgica:
   - Lo que estuvo conceptualmente correcto.
   - Las omisiones técnicas o falta de rigor en balances/mecanismos.
   - La respuesta modelo que dejaría al profesor plenamente satisfecho.
5. Luego formula la siguiente pregunta.

Comienza ahora con la Pregunta 1.
```
