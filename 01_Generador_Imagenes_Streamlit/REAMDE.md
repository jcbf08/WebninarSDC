# Generador de Imágenes Publicitarias con IA (Streamlit)


App de ejemplo para crear **creatividades publicitarias** con IA y aplicar **overlays** (headline, subheadline, CTA y logo) desde una interfaz en Streamlit.


https://github.com/<tu-org>/<tu-repo>


## 🚀 Características
- Proveedor soportado:
- **OpenAI** (`gpt-image-1`)
- Control de **tamaño** (1:1, 3:2, 2:3) y variaciones.
- Campos de **brief creativo** (producto, target, tono, estilo, colores).
- **Negative prompt** y notas extra.
- **Overlay** de textos y **logo** con posición configurable.
- Descarga de cada imagen y **ZIP** con todas las salidas.


## 🧩 Requisitos
- Python 3.10+
- Dependencias en `requirements.txt`
- Credenciales: `OPENAI_API_KEY`


> Puedes definir la credencial como variable de entorno o en `st.secrets`.


## 📦 Instalación


```bash
# Clona el repo
git clone https://github.com/<tu-org>/<tu-repo>.git
cd <tu-repo>


# Crea y activa un entorno (opcional pero recomendado)
python -m venv .venv
source .venv/bin/activate


# Instala dependencias
pip install -r requirements.txt