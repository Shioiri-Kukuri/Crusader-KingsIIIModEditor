
import tkinter as tk
from tkinter import  Menu



class Gui:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Crusader Kings III Mod Editor")
        self.root.geometry("800x600")

        self.menu_bar = Menu(self.root)
        self.root.config(menu=self.menu_bar)

        self.filename = ""  # 添加文件路径存储属性
        self.data = {}  # 用于存储解析后的数据
        self.old_values = {}  # 用于存储属性修改前的值

        self.left_frame = None

        # 初始化character_data为None，将在open_file中根据文件内容进行赋值
        self.character_data = None

        # 初始化存放于相对路径的img/attributes文件夹下的图片
        self.attribute_images = load_attribute_images("img/attribute")

        # 初始化性格特质图片
        self.trait_images = load_trait_images("img/trait")

        # 初始化有序属性列
        self.attribute_order = ["Martial", "Diplomacy", "Intrigue", "Stewardship"]

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

        # 初始化编辑控件
        self.init_edit_controls(self.character_data)
        self.root.mainloop()


