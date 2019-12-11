import torch
from torchvision import models, transforms
from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
import json


def recognize(fns):
    model = models.googlenet(pretrained=True)
    model.eval()
    normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                     std=[0.229, 0.224, 0.225])
    class_idx = json.load(open("imagenet_class_index.json", "r"))
    idx2label = [class_idx[str(k)][1] for k in range(len(class_idx))]

    transformer = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        normalize,
    ])

    with torch.no_grad():
        ims = [Image.open(f).convert("RGB") for f in fns]
        img_tsr = []
        for i in ims:
            img_tsr.append(transformer(i))
        img_tsr = torch.stack(img_tsr)
        pred = model(img_tsr)
        _, pred = torch.max(pred, dim=1)
        pred = pred.numpy()
        pred = [idx2label[i] for i in pred]

        return pred

# pred = recognize(["images/1.png","images/2.png","images/3.jpg","images/4.jpg","images/5.jpg","images/6.jpg"])
# print(pred)
