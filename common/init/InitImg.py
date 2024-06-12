import os
from PIL import ImageTk, Image

class Imginit:
    def __init__(self):
        pass  # 可以保留此方法为空，或移除，因为这里不执行任何操作

    def load_trait_images(self, folder_path):
        trait_images = {}
        for filename in os.listdir(folder_path):
            if filename.startswith("60px-Trait_") and filename.endswith(".png"):
                trait_name = filename[len("60px-Trait_"):-len(".png")]
                img_path = os.path.join(folder_path, filename)
                try:
                    image = ImageTk.PhotoImage(Image.open(img_path))
                    trait_images[trait_name.capitalize()] = image
                except IOError as e:
                    print(f"Failed to load trait image for '{trait_name}': {e}")
        return trait_images

    def load_attribute_images(self, attribute_folder):
        images = {}
        for attribute in ["Martial", "Diplomacy", "Intrigue", "Stewardship"]:
            img_path = os.path.join(attribute_folder, rf"{attribute}.png")
            try:
                img = ImageTk.PhotoImage(file=img_path)
                images[attribute] = img
            except Exception as e:
                print(f"Failed to load image for {attribute}: {e}")
        return images