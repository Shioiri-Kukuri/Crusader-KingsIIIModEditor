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
