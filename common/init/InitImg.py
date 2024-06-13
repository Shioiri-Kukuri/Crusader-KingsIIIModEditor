import os
from PIL import ImageTk, Image
import tkinter as tk

class Imginit:
    def __init__(self):
        pass  # 可以保留此方法为空，或移除，因为这里不执行任何操作

    def load_trait_images(self, folder_path):
        """
            加载特质图片并存储在字典中。

            :param folder_path: 包含特质图片的文件夹路径。
            :return: 一部字典，键为特质名称（大写），值为对应的ImageTk.PhotoImage对象。
        """
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
        """
            加载属性图片至字典。

            :param attribute_folder: 包含属性图片的文件夹路径。
            :return: 一个字典，键为属性名称，值为对应的ImageTk.PhotoImage对象。
        """
        images = {}
        for attribute in ["Martial", "Diplomacy", "Intrigue", "Stewardship"]:
            img_path = os.path.join(attribute_folder, rf"{attribute}.png")
            try:
                img = ImageTk.PhotoImage(file=img_path)
                images[attribute] = img
            except Exception as e:
                print(f"Failed to load image for {attribute}: {e}")
        return images

    # 更新display_traits函数以适应新的布局
    def display_traits(self, traits_list, trait_frame_placeholder):
        """
        在界面上显示特质图片。

        :param traits_list: 要显示的特质名称列表。
        :param trait_frame_placeholder: Tkinter Frame对象，用于放置特质图片标签。
        """
        for index, trait in enumerate(traits_list, start=1):
            trait_capitalized = trait.capitalize()
            if trait_capitalized in self.trait_images:
                print(f"Displaying trait image for '{trait_capitalized}'")

                # 直接使用已经加载的PhotoImage对象，无需通过PIL再次处理
                trait_photo_image = self.trait_images[trait_capitalized]

                trait_img_label = tk.Label(trait_frame_placeholder, image=trait_photo_image, bd=0)
                trait_img_label.image = trait_photo_image  # 防止图片被垃圾回收
                trait_img_label.pack(side=tk.LEFT, padx=(0, 5))

                print(f"Displayed trait image for '{trait_capitalized}' successfully.")
            else:
                print(
                    f"No image found for trait '{trait_capitalized}'. Keys in trait_images: {list(self.trait_images.keys())}")