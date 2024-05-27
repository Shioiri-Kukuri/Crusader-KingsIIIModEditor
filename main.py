import tkinter as tk
from tkinter import filedialog, Menu
from tkinter import messagebox
import os
import re


#"main.py"为主程序,主要功能为翻译文件和文件图形化
#
#
#

#定义需要解析文件的结构体
class CharacterAttributes:
    def __init__(self):
        self.name = ""
        self.martial = None
        self.diplomacy = None
        self.intrigue = None
        self.stewardship = None
        self.religion = ""
        self.culture = ""
        self.traits = []
        self.birth_date = None
        self.death_date = None


#定义解析方法
def parse_character_data(file_path):
    attributes = CharacterAttributes()
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        # 匹配name、martial、diplomacy等可修改的属性
        for attr in ['name', 'martial', 'diplomacy', 'intrigue', 'stewardship', 'religion', 'culture']:
            pattern = re.compile(f'{attr}\s*=\s*(["\']?)(.*?)(\\1)?')
            match = pattern.search(content)
            if match:
                value = match.group(2).strip()
                if attr in ['martial', 'diplomacy', 'intrigue', 'stewardship']:
                    # 检查值是否为空或仅包含空白字符
                    if value and value.strip():
                        value = int(value)  # 将这些属性转换为整数
                    else:
                        print(f"Warning: Empty or whitespace-only value found for attribute '{attr}', skipping conversion.")
                setattr(attributes, attr, value)

        # 匹配traits
        trait_pattern = re.compile('trait\s*=\s*([\w_]+)')
        traits = trait_pattern.findall(content)
        attributes.traits = traits

        # 匹配出生和死亡日期
        date_pattern = re.compile(r'(\d+)\.(\d+)\.(\d+)\s*=\s*\{\s*(birth|death)\s*=\s*yes\s*\}')
        dates = date_pattern.findall(content)
        for date in dates:
            year, month, day, event_type = map(int, date)
            if event_type == 1:  # birth
                attributes.birth_date = f"{year}.{month}.{day}"
            elif event_type == 2:  # death
                attributes.death_date = f"{year}.{month}.{day}"

    return attributes


class CrusaderKingsIIIEditor:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Crusader Kings III Mod Editor")
        self.root.geometry("800x600")  # 添加这行代码以设置窗口大小为800x600像素

        # 创建顶部菜单栏
        self.menu_bar = Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # File菜单
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Open File", command=self.open_file)
        self.file_menu.add_command(label="Save File", command=self.save_file)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        # Edit菜单
        self.edit_menu = Menu(self.menu_bar, tearoff=0)
        self.edit_menu.add_command(label="Settings", command=self.show_settings)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)

        # Help菜单
        self.help_menu = Menu(self.menu_bar, tearoff=0)
        self.help_menu.add_command(label="ReadMe", command=self.show_readme)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)

        # 简单占位符，用于后续添加编辑器主界面
        self.editor_frame = tk.Frame(self.root, padx=10, pady=10)
        self.editor_frame.pack(fill=tk.BOTH, expand=True)

        self.root.mainloop()

    #打开文件
    def open_file(self):
        """实现打开文件功能，并检查文件路径是否符合要求"""
        file_path = filedialog.askopenfilename()
        print(f"Selected file path: {file_path}")

        if not file_path:
            print("File selection cancelled.")
            return

        print("Checking file path...")
        target_subpath = "history/characters"
        if target_subpath not in file_path:
            messagebox.showerror("Error", "Please open a file located under history/characters.")
            print("Invalid path error shown after checking full path.")
            return

        print("Valid path detected. Continuing with file processing...")
        character_data = parse_character_data(file_path)

        # 打印解析到的数据到控制台
        print(f"Name: {character_data.name}")
        print(f"Martial: {character_data.martial}")
        print(f"Diplomacy: {character_data.diplomacy}")
        print(f"Intrigue: {character_data.intrigue}")
        print(f"Stewardship: {character_data.stewardship}")
        print(f"Religion: {character_data.religion}")
        print(f"Culture: {character_data.culture}")
        print(f"Traits: {', '.join(character_data.traits)}")
        print(f"Birth Date: {character_data.birth_date}")
        print(f"Death Date: {character_data.death_date}")


    def save_file(self):
        """实现保存文件功能"""
        file_path = filedialog.asksaveasfilename()
        print(f"Saving file to: {file_path}")

    def show_settings(self):
        """显示设置窗口（这里仅作为占位，需后续完善）"""
        print("Showing Settings...")

    def show_readme(self):
        """显示ReadMe帮助信息（这里仅作为占位，需后续完善）"""
        print("Showing ReadMe...")

if __name__ == "__main__":
    CrusaderKingsIIIEditor()