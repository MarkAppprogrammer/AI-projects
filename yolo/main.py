from transformers import YolosImageProcessor, YolosForObjectDetection
from PIL import Image
import torch
import requests

# url = "http://images.cocodataset.org/val2017/000000039769.jpg"
path = "test.jpg"
image = Image.open(path)

model = YolosForObjectDetection.from_pretrained('hustvl/yolos-tiny')
image_processor = YolosImageProcessor.from_pretrained("hustvl/yolos-tiny")

inputs = image_processor(images=image, return_tensors="pt")
outputs = model(**inputs)

logits = outputs.logits
bboxes = outputs.pred_boxes


target_sizes = torch.tensor([image.size[::-1]])
results = image_processor.post_process_object_detection(outputs, threshold=0.9, target_sizes=target_sizes)[0]
for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
    box = [round(i, 2) for i in box.tolist()]
    print(
        f"Detected {model.config.id2label[label.item()]} with confidence "
        f"{round(score.item(), 3)} at location {box}"
    )


from PIL import Image, ImageDraw, ImageFont

def draw_boxes(image_path, results, model):
    image = Image.open(image_path).convert("RGB")
    draw = ImageDraw.Draw(image)

    # font = ImageFont.truetype("arial.ttf", size=12)
    font = ImageFont.load_default()

    for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
        box = [round(i, 2) for i in box.tolist()]
        class_name = model.config.id2label[label.item()]
        confidence = round(score.item(), 2)

        draw.rectangle(box, outline="red", width=2)

        text = f"{class_name} {confidence}"
        draw.text((box[0], box[1] - 10), text, fill="red", font=font)

    image.save("output.jpg")
    print("Annotated image saved as output.jpg")

draw_boxes(path, results, model)