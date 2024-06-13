import os
from PIL import ImageTk, Image
import tkinter as tk

class Imginit:
    ATTRIBUTE_IMAGES_PATH = "img/attribute"
    TRAIT_IMAGES_PATH = "img/trait"
    ATTRIBUTE_ORDER = ["Martial", "Diplomacy", "Intrigue", "Stewardship"]


    def __init__(self):
        pass  # 可以保留此方法为空，或移除，因为这里不执行任何操作

    def load_trait_images(self):
        """
            加载特质图片并存储在字典中。

            :param folder_path: 包含特质图片的文件夹路径。
            :return: 一部字典，键为特质名称（大写），值为对应的ImageTk.PhotoImage对象。
        """
        trait_images = {}
        folder_path = self.TRAIT_IMAGES_PATH
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

    def load_attribute_images(self):
        """
            加载属性图片至字典。

            :param attribute_folder: 包含属性图片的文件夹路径。
            :return: 一个字典，键为属性名称，值为对应的ImageTk.PhotoImage对象。
        """
        images = {}
        attribute_folder = self.ATTRIBUTE_IMAGES_PATH
        for attribute in self.ATTRIBUTE_ORDER:
            img_path = os.path.join(attribute_folder, f"{attribute}.png")
            try:
                img = ImageTk.PhotoImage(file=img_path)
                images[attribute] = img
            except Exception as e:
                print(f"Failed to load image for {attribute}: {e}")
        return images



