# Presentación Académica: Estructura, Termodinámica y Cinética de Polímeros
## Subtemas 4.1 a 4.4 de W.D. Callister | Enfoque Riguroso para Ingeniería Química

🔗 **Sitio web en vivo (optimizado para celular):**  
[https://mgueldiaz10-oss.github.io/fundamentos-de-ingenieria-de-los-materiales/](https://mgueldiaz10-oss.github.io/fundamentos-de-ingenieria-de-los-materiales/)

Esta aplicación web es una presentación interactiva de diapositivas en estilo **Harvard Minimalist**, diseñada para estudiar y exponer los fundamentos macromoleculares con el más alto rigor analítico y fisicoquímico. Está 100% optimizada para dispositivos móviles (gestos táctiles de deslizamiento) y computadoras de escritorio.

---

### Características Principales

- **Capítulo 4 Completo en 30 Diapositivas:** Cobertura exhaustiva de los 12 subtemas (4.1 a 4.12) de W.D. Callister, diseñada para una clase magistral y preparación de examen de 90 minutos (hora y media).
- **Estilo Editorial Harvard Minimalist:** Tipografía académica refinada (*Playfair Display*, *Inter*, *JetBrains Mono*), paleta cromática sobria (*Harvard Crimson* `#A51C30`, azul pizarra y fondo marfil), libre de distracciones.
- **Todas las Figuras y Tablas Originales del Callister en Alta Resolución (216 DPI):**
  - **Bloque 1 (4.1 - 4.4):** Tablas 4.1, 4.2 y 4.3 (Partes 1 y 2); Figuras 4.1 (PE zig-zag) y 4.2 (PTFE, PVC, PP); Reacciones 4.1 y 4.2 (iniciación y propagación).
  - **Bloque 2 (4.5 - 4.12):** Figura 4.3 (curvas de distribución $M_n$ vs $M_w$); Figura 4.4 (resistencia vs peso molecular); Tabla 4.4 (cálculo de PVC); Figura 4.5 (cono de rotación C-C); Figura 4.6 (ovillo aleatorio y distancia $r$); Figura 4.7 (lineal, ramificado, entrecruzado, red 3D); Diagramas de Tacticidad (isotáctico, sindiotáctico, atáctico); Isómeros cis/trans de isopreno (caucho vs gutapercha); Figura 4.8 (taxonomía); Figura 4.9 (copolímeros); Tabla 4.5 (elastómeros); Figura 4.10 (celda ortorrómbica de PE); Figura 4.11 (TEM monocristal); Figura 4.12 (láminas plegadas); Figura 4.13 (esferulita); Figura 4.14 (Cruz de Malta bajo luz polarizada).
- **Documentos PDF de Estudio y Alimento para NotebookLM:**
  - `Fundamentos_Completos_Polimeros_Cap4_IQ.pdf`: Compendio maestro unificado de 15 páginas.
  - `Modulo_1_Polimeros_Estructura_Quimica_IQ.pdf`: Subtemas 4.1 a 4.4 (8 páginas).
  - `Modulo_2_Polimeros_Pesos_Estructura_Cristalinidad_IQ.pdf`: Subtemas 4.5 a 4.12 (7 páginas).
- **Guía de Podcasts y Guion de 90 Minutos:** `PROMPTS_PODCAST_NOTEBOOKLM_POLIMEROS.md` con el prompt listo para generar el Audio Overview de 2 locutores en NotebookLM y cronograma de clase minuto a minuto.
- **Controles Móviles Táctiles:** Desliza el dedo horizontalmente (*swipe*) para cambiar de diapositiva.
- **Selector de Vista Dual:**
  - *Modo Presentación:* Navegación diapositiva por diapositiva.
  - *Modo Lectura Continua:* Convierte las diapositivas en un documento continuo vertical ideal para repasar en el teléfono como libro digital.
- **Visor Zoom (Lightbox):** Toca cualquier gráfica o tabla del libro para abrirla en alta resolución a pantalla completa.

---

### Cómo Probarlo Localmente

Puedes abrirlo directamente haciendo doble clic en el archivo [`index.html`](index.html) en tu explorador de archivos, o iniciar un servidor local rápido con Python:

```bash
uv run python -m http.server 8000
```
Y abrir `http://localhost:8000` en tu navegador.

---

### Guía para Subir a tu GitHub Personal y Publicarlo en GitHub Pages

Para tenerlo disponible en tu teléfono mediante un enlace web público (`https://tu-usuario.github.io/fundamentos-de-ingenieria-de-los-materiales`):

1. **Crea un repositorio en GitHub:**
   - Entra a [github.com/new](https://github.com/new) y crea un nuevo repositorio público (por ejemplo, `fundamentos-de-ingenieria-de-los-materiales`).

2. **Sube los archivos desde tu terminal:**
   Abre una terminal PowerShell en esta carpeta (`c:\Users\madia\Documents\antigravity\MATERIALES`) y ejecuta:

   ```bash
   git init
   git add .
   git commit -m "Presentación Harvard Minimalist Polímeros Callister 4.1-4.4"
   git branch -M main
   git remote add origin https://github.com/TU_USUARIO/fundamentos-de-ingenieria-de-los-materiales.git
   git push -u origin main
   ```

3. **Activar GitHub Pages (1 Clic):**
   - En tu repositorio de GitHub, haz clic en **Settings** (Configuración) arriba a la derecha.
   - En el menú lateral izquierdo, haz clic en **Pages**.
   - Bajo **Build and deployment > Branch**, selecciona:
     - Rama: `main`
     - Carpeta: `/ (root)`
   - Haz clic en **Save** (Guardar).

En aproximadamente 1 o 2 minutos, GitHub te dará un enlace público donde la presentación estará activa y podrás abrirla en tu teléfono, compartirla o proyectarla en clase.
