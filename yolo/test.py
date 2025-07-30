from transformers import AutoImageProcessor, AutoModelForObjectDetection
import torch
from PIL import Image
import requests
import matplotlib.pyplot as plt
import matplotlib.patches as patches

processor = AutoImageProcessor.from_pretrained("hustvl/yolos-small")
model = AutoModelForObjectDetection.from_pretrained("hustvl/yolos-small")

image = Image.open("test.jpg")  

inputs = processor(images=image, return_tensors="pt")

with torch.no_grad():
    outputs = model(**inputs)

target_sizes = torch.tensor([image.size[::-1]])  
results = processor.post_process_object_detection(outputs, threshold=0.9, target_sizes=target_sizes)[0]

plt.figure(figsize=(12, 8))
plt.imshow(image)
ax = plt.gca()

for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
    box = [round(i, 2) for i in box.tolist()]
    x, y, w, h = box
    rect = patches.Rectangle((x, y), w - x, h - y, linewidth=2, edgecolor='red', facecolor='none')
    ax.add_patch(rect)
    ax.text(x, y, f"{model.config.id2label[label.item()]}: {round(score.item(), 3)}", color='white',
            bbox=dict(facecolor='red', alpha=0.5))

plt.axis("off")
plt.show()
