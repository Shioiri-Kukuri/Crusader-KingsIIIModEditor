import sys
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from common.init.InitUI import Gui
from util.ParseCharacterData import ParseCharacterData as parse_character_data



#本项目旨在为Crusader Kings III（CKIII）游戏的Mod制作提供一个便捷、直观的图形化编辑工具。
# 我们计划运用Python图形用户界面库，如Tkinter或PyQt，构建一款小型的Crusader Kings III Mod编辑器。
# 该编辑器的核心功能是将复杂的Mod代码以图文的形式呈现，支持用户进行可视化操作，极大提升Mod编辑的易用性和效率。
class CrusaderKingsIIIEditor:
    def __init__(self):
        app = Gui()  # 实例化Gui类，这将自动运行GUI的主循环


    # 更新display_traits函数以适应新的布局
    def display_traits(self, traits_list, trait_frame_placeholder):
        """显示角色的特质图片"""
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



    def save_to_file(self):
        """将内存中的数据保存回文件，根据属性值更新文本"""
        with open(self.filename, 'r+', encoding='utf-8') as file:
            content = file.read()
            # 假设简单替换，实际情况可能需要更复杂的解析逻辑
            for key, value in self.data.items():
                content = content.replace(f"{key}: {self.old_values[key]}", f"{key}: {value}")
            # 将指针移到文件开头并截断文件后写入新内容
            file.seek(0)
            file.truncate()
            file.write(content)
            print("File saved after attribute change.")

    def on_attribute_change(self, attribute, new_value):
        print(
            f"Attribute change triggered for '{attribute}', Old Value: {self.data.get(attribute)}, New Value: {new_value}")
        """属性更改时的回调处理"""
        if attribute in self.data:
            old_value = self.data[attribute]
            if old_value != new_value:  # 检查值是否真的改变了
                self.old_values[attribute] = old_value  # 更新旧值
                self.data[attribute] = new_value

        print("File saved after attribute change.")



    def update_data_and_old_values(self, character_data):
        print("Updating data and old values...")
        """更新内存中的数据和旧值映射"""
        self.data = {
            "name": character_data.name,
            "martial": character_data.martial,
            "diplomacy": character_data.diplomacy,
            "intrigue": character_data.intrigue,
            "stewardship": character_data.stewardship,
            "birth_date": character_data.birth_date,
            "death_date": character_data.death_date,
        }
        self.old_values = self.data.copy()
        print(f"Data updated. Data: {self.data}, Old Values: {self.old_values}")

if __name__ == "__main__":
    CrusaderKingsIIIEditor()
