import sys
import tkinter as tk
from tkinter import Menu, messagebox
from common.init.InitImg import Imginit
from util.FileOpener import FileOpener
from util.FileSaver import FileSaver


class Gui:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Crusader Kings III Mod Editor")
        self.root.geometry("800x600")

        self.menu_bar = Menu(self.root)
        self.root.config(menu=self.menu_bar)

        self.filename = ""
        self.data = {}
        self.old_values = {}

        self.left_frame = None
        self.character_data = None

        # 实例化辅助类
        self.file_opener = FileOpener(self)
        self.file_saver = FileSaver(self)

        img_loader = Imginit()  # 实例化Imginit类

        self.attribute_images = img_loader.load_attribute_images("img/attribute")
        self.trait_images = img_loader.load_trait_images("img/trait")

        self.attribute_order = ["Martial", "Diplomacy", "Intrigue", "Stewardship"]

        # 创建顶部菜单栏
        self.menu_bar = Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # File菜单
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Open File", command=self.file_opener.open_file)
        self.file_menu.add_command(label="Save File", command=self.file_saver.save_file)
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

        # 新增图像部件和属性显示标签
        self.character_image_label = tk.Label(self.root)
        self.character_image_label.pack(pady=10)

        self.attributes_frame = tk.Frame(self.root, padx=10, pady=10)
        self.attributes_frame.pack(fill=tk.BOTH, expand=True)

        self.name_label = tk.Label(self.attributes_frame, text="Name: ", font=("Arial", 12))
        self.name_label.grid(row=0, column=0, sticky="w", pady=(0, 10))

        self.martial_label = tk.Label(self.attributes_frame, text="Martial: ", font=("Arial", 12))
        self.diplomacy_label = tk.Label(self.attributes_frame, text="Diplomacy: ", font=("Arial", 12))
        self.intrigue_label = tk.Label(self.attributes_frame, text="Intrigue: ", font=("Arial", 12))
        self.stewardship_label = tk.Label(self.attributes_frame, text="Stewardship: ", font=("Arial", 12))



        self.root.mainloop()

    def show_settings(self):
        """显示设置窗口（这里仅作为占位，需后续完善）"""
        print("Showing Settings...")

    def show_readme(self):
        """显示ReadMe帮助信息（这里仅作为占位，需后续完善）"""
        print("Showing ReadMe...")

    def init_edit_controls(self, character_data):
        pass





