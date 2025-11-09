# Generador de Imágenes Publicitarias — Stable Diffusion 2.1 (Hugging Face)

Usa `stabilityai/stable-diffusion-2-1` vía **Hugging Face Inference API**.
https://huggingface.co/stabilityai/stable-diffusion-2-1

## Requisitos
- Token de Hugging Face: crea uno en https://huggingface.co/settings/tokens
- Define `HUGGINGFACE_API_TOKEN` o usa `st.secrets`.

## Pasos
1) `pip install -r requirements.txt`
2) Exporta `HUGGINGFACE_API_TOKEN` (o usa `.streamlit/secrets.toml`)
3) `streamlit run app.py`

## Parámetros
- `width/height`: 512–1024
- `num_inference_steps`: 10–60
- `guidance_scale`: 1–15
- `seed`: -1 aleatorio; si das un número, fija reproducibilidad (se incrementa por variante)
- `negative_prompt`: para excluir elementos no deseados

## Notas
- SD2.1 no escribe texto perfecto; considera el CTA como zona visual.
- Puedes superponer un logo local luego (branding rápido sin re-render).
