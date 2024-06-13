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
    def display_traits(self, traits_list, trait_frame):
        """
        在界面上显示特质图片。

        :param traits_list: 要显示的特质名称列表。
        :param trait_frame_placeholder: Tkinter Frame对象，用于放置特质图片标签。
        """
        COLS = 4  # 每行特质数
        ROWS = 3  # 最大行数

        # 清空之前的内容
        for widget in trait_frame.winfo_children():
            widget.destroy()

        for idx, trait_name in enumerate(traits_list[:COLS * ROWS]):  # 限制显示的特质数量
            row = idx // COLS
            col = idx % COLS
            capitalized_trait_name = trait_name.capitalize()

            if capitalized_trait_name in self.trait_images:
                img_label = tk.Label(trait_frame, image=self.trait_images[capitalized_trait_name], padx=5, pady=5)
                img_label.image = self.trait_images[capitalized_trait_name]
                img_label.grid(row=row, column=col, sticky="w", pady=(0, 10))

            # 配置列宽和行高以适应特质图片
            trait_frame.columnconfigure(col, weight=1)
            trait_frame.rowconfigure(row, weight=1)