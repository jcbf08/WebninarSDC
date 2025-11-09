import os
import base64
from io import BytesIO
from datetime import datetime

import streamlit as st
from PIL import Image

try:
    from openai import OpenAI
except Exception as e:
    st.error("No se pudo importar 'openai'. Verifica instalación.")
    raise e


# ---- Helpers ----
def build_prompt(product, audience, value_prop, cta, tone, style, brand_colors, brand_constraints, must_not):
    parts = [
        f"Create a high-quality advertising image for: {product}.",
        f"Target audience: {audience}.",
        f"Unique value proposition: {value_prop}.",
        f"Primary call-to-action text: {cta}. Ensure legible typography.",
        f"Tonal direction: {tone}.",
        f"Visual style: {style}.",
        "Composition must include clear focus on product, balanced layout, clean readability."
    ]
    if brand_colors.strip():
        parts.append(f"Brand color palette: {brand_colors}.")
    if brand_constraints.strip():
        parts.append(f"Brand constraints: {brand_constraints}.")
    if must_not.strip():
        parts.append(f"Do not include: {must_not}.")
    return " ".join(parts)


def b64_to_image(b64_str):
    data = base64.b64decode(b64_str)
    return Image.open(BytesIO(data)).convert("RGBA")


def paste_logo(img, logo, position="bottom_right", scale=0.17):
    img = img.convert("RGBA")
    logo = logo.convert("RGBA")

    w, h = img.size
    new_w = int(w * scale)
    ratio = new_w / logo.width
    logo = logo.resize((new_w, int(logo.height * ratio)))

    pad = int(w * 0.02)
    positions = {
        "top_left": (pad, pad),
        "top_right": (w - logo.width - pad, pad),
        "bottom_left": (pad, h - logo.height - pad),
        "bottom_right": (w - logo.width - pad, h - logo.height - pad)
    }
    xy = positions.get(position, positions["bottom_right"])

    composed = Image.new("RGBA", img.size)
    composed.paste(img, (0, 0))
    composed.paste(logo, xy, logo)
    return composed.convert("RGB")


def img_to_bytes(img, fmt="PNG"):
    buffer = BytesIO()
    img.save(buffer, format=fmt)
    return buffer.getvalue()


# ---- UI ----
st.set_page_config(page_title="Generador Publicitario DALL·E 3", page_icon="🎨")
st.title("🎨 Generador de Imágenes Publicitarias con DALL·E 3")

with st.sidebar:
    st.subheader("API Key")
    api_key = st.text_input("OPENAI_API_KEY", type="password", value=os.getenv("OPENAI_API_KEY", ""))
    size = st.selectbox("Tamaño", ["1024x1024", "1024x1792", "1792x1024"])
    quality = st.selectbox("Calidad", ["standard", "hd"])
    n_images = st.slider("Variantes a generar", 1, 4, 1)

    st.markdown("---")
    st.subheader("Logo (Opcional)")
    logo_file = st.file_uploader("Subir logo (PNG/JPG)", type=["png", "jpg", "jpeg"])
    position = st.selectbox("Posición", ["bottom_right", "bottom_left", "top_right", "top_left"])
    scale = st.slider("Tamaño logo", 0.05, 0.40, 0.17, 0.01)

st.markdown("### Brief Publicitario")

product = st.text_input("Producto/Servicio")
audience = st.text_input("Público Objetivo")
value_prop = st.text_area("Propuesta de Valor")
cta = st.text_input("CTA (Texto)")
tone = st.selectbox("Tono", ["Inspirador", "Directo", "Premium", "Divertido", "Tecnológico"])
style = st.selectbox("Estilo", ["Realista", "Minimalista", "Ilustración", "E-commerce Clean"])
brand_colors = st.text_input("Colores de Marca (opcional)")
brand_constraints = st.text_input("Restricciones de marca (opcional)")
must_not = st.text_input("Evitar (opcional)")

generate = st.button("🚀 Generar")

# ---- Llamada a OpenAI ----
if generate:
    if not api_key:
        st.error("Debes ingresar tu OPENAI_API_KEY")
        st.stop()

    prompt = build_prompt(product, audience, value_prop, cta, tone, style, brand_colors, brand_constraints, must_not)
    client = OpenAI(api_key=api_key)

    with st.spinner("Generando imágenes..."):
        resp = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size=size,
            quality=quality,
            n=n_images,
            response_format="b64_json"   # ← CORRECCIÓN CLAVE
        )

    dt = datetime.now().strftime("%Y%m%d_%H%M%S")

    for i, data in enumerate(resp.data, start=1):
        b64 = getattr(data, "b64_json", None)
        if not b64:
            st.warning(f"No se recibió imagen para variante {i}.")
            continue

        img = b64_to_image(b64)

        if logo_file is not None:
            try:
                logo = Image.open(logo_file)
                img = paste_logo(img, logo, position, scale)
            except:
                st.warning("No se pudo superponer el logo.")

        st.image(img, caption=f"Variante {i}", use_column_width=True)

        colA, colB = st.columns(2)
        with colA:
            st.download_button("⬇️ PNG", data=img_to_bytes(img, "PNG"), file_name=f"ad_{dt}_{i}.png")
        with colB:
            st.download_button("⬇️ JPG", data=img_to_bytes(img.convert("RGB"), "JPEG"), file_name=f"ad_{dt}_{i}.jpg")

st.caption("⚖️ Usa contenido responsablemente y valida claims de marca.")
