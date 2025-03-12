import gradio as gr
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")


def generate_caption(image):
    if image is None:
        return "Пожалуйста, загрузите изображение."
    try:
        raw_image = Image.fromarray(image).convert("RGB")
        inputs = processor(raw_image, return_tensors="pt")
        out = model.generate(**inputs)
        caption = processor.decode(out[0], skip_special_tokens=True)
        return f"Описание: {caption}"
    except Exception as e:
        return f"Ошибка обработки изображения: {str(e)}"


css = """
.gradio-container {
    background-color: #f0f0f0;
    padding: 20px;
    border-radius: 10px;
}
"""

with gr.Blocks(css=css) as demo:
    gr.Markdown("# Сервис описания изображений")
    with gr.Row():
        img_input = gr.Image(label="Загрузите изображение", type="numpy")
        text_output = gr.Textbox(label="Текстовое описание")
    btn = gr.Button("Сгенерировать описание")
    btn.click(generate_caption, inputs=img_input, outputs=text_output)

demo.launch()
