# Presentación Académica: Estructura, Termodinámica y Cinética de Polímeros
## Subtemas 4.1 a 4.4 de W.D. Callister | Enfoque Riguroso para Ingeniería Química

Esta aplicación web es una presentación interactiva de diapositivas en estilo **Harvard Minimalist**, diseñada para estudiar y exponer los fundamentos macromoleculares con el más alto rigor analítico y fisicoquímico. Está 100% optimizada para dispositivos móviles (gestos táctiles de deslizamiento) y computadoras de escritorio.

---

### Características Principales

- **Estilo Editorial Harvard Minimalist:** Tipografía académica refinada (*Playfair Display*, *Inter*, *JetBrains Mono*), paleta cromática sobria (*Harvard Crimson* `#A51C30`, azul pizarra y fondo marfil), libre de distracciones.
- **Figuras y Tablas Originales del Callister en Alta Resolución:**
  - **Tabla 4.1:** Parafinas y puntos de ebullición.
  - **Isómeros de Butano:** $n$-butano lineal vs. isobutano globular.
  - **Tabla 4.2:** Grupos funcionales orgánicos.
  - **Figura 4.1:** Cadena de polietileno plana vs. perspectiva tridimensional en zig-zag ($109.5^\circ$, $0.154\text{ nm}$).
  - **Reacciones 4.1 y 4.2:** Iniciación térmica y propagación por radicales libres.
  - **Figura 4.2:** Cadenas de PTFE (apantallamiento del flúor), PVC (dipolo polar) y PP (asimetría del metilo).
  - **Tabla 4.3 (Partes 1 y 2):** Los 10 polímeros de ingeniería más comunes.
- **Tipografía Matemática KaTeX:** Renderizado nítido de ecuaciones cinéticas, balances de materia y deducciones termodinámicas.
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

Para tenerlo disponible en tu teléfono mediante un enlace web público (`https://tu-usuario.github.io/materiales-polimeros`):

1. **Crea un repositorio en GitHub:**
   - Entra a [github.com/new](https://github.com/new) y crea un nuevo repositorio público (por ejemplo, `materiales-polimeros`).

2. **Sube los archivos desde tu terminal:**
   Abre una terminal PowerShell en esta carpeta (`c:\Users\madia\Documents\antigravity\MATERIALES`) y ejecuta:

   ```bash
   git init
   git add .
   git commit -m "Presentación Harvard Minimalist Polímeros Callister 4.1-4.4"
   git branch -M main
   git remote add origin https://github.com/TU_USUARIO/materiales-polimeros.git
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
