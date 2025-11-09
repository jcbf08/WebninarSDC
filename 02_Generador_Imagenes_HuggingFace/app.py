import os
import io
import streamlit as st
from PIL import Image

# IMPORT CORRECTO del cliente y el error (opcional)
from huggingface_hub import InferenceClient
from huggingface_hub.errors import HfHubHTTPError  # <- FIX del import

st.set_page_config(page_title="HF SD 2.1 - Mínimo", page_icon="🛰️", layout="centered")
st.title("🛰️ Stable Diffusion 2.1 (Hugging Face) - Mínimo funcional")
st.caption("Modelo: stabilityai/stable-diffusion-2-1 via InferenceClient")

# --- Token HF ---
default_token = os.getenv("HF_TOKEN", "")
hf_token = st.text_input("HF_TOKEN (scope: read)", type="password", value=default_token)
if not hf_token:
    st.info("Ingresa tu HF_TOKEN o configúralo como variable de entorno HF_TOKEN.")
model_id = "stabilityai/stable-diffusion-2-1"

# --- Prompt por defecto (tu ejemplo) ---
prompt = st.text_area(
    "Prompt",
    value="An astronaut riding a unicorn in outer space holding a Coca-Cola, highly detailed, cinematic lighting",
    height=90
)

col_a, col_b = st.columns(2)
with col_a:
    steps = st.slider("num_inference_steps", 10, 60, 30, 1)
with col_b:
    guidance = st.slider("guidance_scale", 1.0, 15.0, 7.5, 0.5)

go = st.button("🚀 Generar imagen", type="primary", disabled=not hf_token or not prompt.strip())

@st.cache_resource(show_spinner=False)
def get_client(token: str):
    # Usa el router nuevo automáticamente (no pongas manualmente api-inference)
    return InferenceClient(model=model_id, token=token)

def ensure_rgb(img: Image.Image) -> Image.Image:
    return img.convert("RGB") if img.mode != "RGB" else img

if go:
    try:
        client = get_client(hf_token)
        with st.spinner("Generando con Hugging Face…"):
            # text_to_image devuelve un PIL.Image
            img: Image.Image = client.text_to_image(
                prompt=prompt,
                num_inference_steps=steps,
                guidance_scale=guidance,
            )

        img = ensure_rgb(img)
        st.image(img, caption="Resultado", use_column_width=True)

        # Descargas
        buf_png = io.BytesIO()
        img.save(buf_png, format="PNG")
        st.download_button("⬇️ Descargar PNG", data=buf_png.getvalue(),
                           file_name="resultado.png", mime="image/png")

        buf_jpg = io.BytesIO()
        img.save(buf_jpg, format="JPEG")
        st.download_button("⬇️ Descargar JPG", data=buf_jpg.getvalue(),
                           file_name="resultado.jpg", mime="image/jpeg")

    except HfHubHTTPError as e:
        st.error(f"HF Hub HTTP Error: {e}")
        st.info(
            "Consejos:\n"
            "- Verifica tu HF_TOKEN (scope: read).\n"
            "- Confirma que el modelo exista y no sea privado: stabilityai/stable-diffusion-2-1.\n"
            "- Si usas Spaces, añade HF_TOKEN como secreto/variable de entorno."
        )
    except Exception as e:
        st.error(f"Error al generar: {e}")
        st.info(
            "Si antes veías 410/404:\n"
            "- No uses 'api-inference.huggingface.co' manualmente; InferenceClient usa el router nuevo.\n"
            "- Asegura versión reciente de huggingface_hub.\n"
            "- Revisa conexión de red / límites de cuota."
        )
