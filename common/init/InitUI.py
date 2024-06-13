import sys
import tkinter as tk
from tkinter import Menu, messagebox
from common.init.InitImg import Imginit
from util.FileOpener import FileOpener


class Gui:
    def __init__(self):
        """
        初始化GUI类，设置窗口、菜单、基本布局及初始化图像资源。
        """
        self.root = tk.Tk()
        self.root.title("Crusader Kings III Mod Editor")
        self.root.geometry("800x600")

        self.menu_bar = Menu(self.root)
        self.root.config(menu=self.menu_bar)

        self.filename = ""
        self.data = {}
        self.old_values = {}
        self.character_data = None

        FONT_SIZE = 12



        # 初始化FileOpener实例
        self.file_opener = FileOpener(self)

        # 初始化编辑器主界面框架
        self.editor_frame = tk.Frame(self.root, padx=10, pady=10)
        self.editor_frame.pack(fill=tk.BOTH, expand=True)

        # 图像部件
        self.character_image_label = tk.Label(self.editor_frame)
        self.character_image_label.pack(pady=10)

        # 属性显示标签
        self.attributes_frame = tk.Frame(self.editor_frame, padx=10, pady=10)
        self.attributes_frame.pack(fill=tk.BOTH, expand=True)

        # 初始化菜单
        self.setup_menus()

        # 初始化图像资源
        img_loader = Imginit()
        self.attribute_images = img_loader.load_attribute_images("img/attribute")
        self.trait_images = img_loader.load_trait_images("img/trait")
        self.attribute_order = ["Martial", "Diplomacy", "Intrigue", "Stewardship"]

        # 界面布局占位符
        self.name_label = tk.Label(self.attributes_frame, text="Name: ", font=("Arial", FONT_SIZE))
        self.name_label.grid(row=0, column=0, sticky="w", pady=(0, 10))

        # 初始化FileOpener实例
        self.file_opener = FileOpener(self)
        self.root.mainloop()

    def setup_menus(self):
        """设置GUI的菜单项。"""
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Open File", command=self.file_opener.open_file)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        self.settings_menu = Menu(self.menu_bar, tearoff=0)
        self.settings_menu.add_command(label="Settings", command=self.show_settings)
        self.menu_bar.add_cascade(label="Settings", menu=self.settings_menu)

        self.help_menu = Menu(self.menu_bar, tearoff=0)
        self.help_menu.add_command(label="ReadMe", command=self.show_readme)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)

    def show_settings(self):
        """显示设置窗口。"""
        print("Showing Settings...")

    def show_readme(self):
        """显示帮助文档。"""
        print("Showing ReadMe...")

    def on_attribute_change(self, attribute, new_value):
        """
        处理属性值变更的回调函数。
        :param attribute: 变更的属性名称。
        :param new_value: 新的属性值。
        """
        print(f"{attribute} changed to {new_value}")
        # 这里可以添加实际处理逻辑，比如更新数据模型或验证输入
        self.character_data.set_attribute(attribute, int(new_value))  # 假设有一个set_attribute方法

    def display_traits(self, traits_list, trait_frame_placeholder):

        if trait_frame_placeholder.grid_slaves():
            for child in trait_frame_placeholder.winfo_children():
                child.destroy()

        row_index = 0
        max_cols = len(traits_list)
        if max_cols > 0:
            trait_frame_placeholder.grid_columnconfigure(0, weight=1)  # 设置列可扩展

        for trait_name in traits_list:
            capitalized_trait_name = trait_name.capitalize()
            if capitalized_trait_name in self.trait_images:
                print(f"{capitalized_trait_name} trait image")
                img_label = tk.Label(trait_frame_placeholder, image=self.trait_images[capitalized_trait_name])
                img_label.image = self.trait_images[capitalized_trait_name]  # 防止图像被垃圾回收
                img_label.grid(row=row_index, column=0, sticky="w", pady=(row_index * 10, 0))

                if max_cols > 1:
                    # 如果有多列，调整列宽以适应图片
                    trait_frame_placeholder.columnconfigure(row_index % max_cols, weight=1)

                row_index += 1
            else:
                print(f"No image for trait: {capitalized_trait_name}")

        # 强制刷新
        self.root.update()

    def update_character(self, character_data):
        """
        更新界面以显示新加载的角色数据。
        :param character_data: 包含角色信息的对象。
        """
        if character_data is None:
            return

        self.character_data = character_data

        # 更新图像和基本信息
        # 使用默认占位符图像路径
        default_image_path = "img/PlaceholderHead.png"  # 确保这个路径是正确默认图像路径
        self.update_character_image(default_image_path)
        self.name_label.config(text=f"Name: {character_data.name}")

        # 更新左侧属性信息
        self.update_left_side(character_data)

        # 更新右侧属性数值和特质
        self.update_right_side(character_data)

    def update_character_image(self, image_path):
        """更新角色图像。使用固定默认图像或占位符图像。"""
        try:
            self.character_image = tk.PhotoImage(file=image_path)
            self.character_image_label.config(image=self.character_image)
        except Exception as e:
            print(f"Error loading default image: {e}", file=sys.stderr)
            messagebox.showerror("Error", "Failed to load default image.")

    def update_left_side(self, character_data):
        """更新左侧属性面板的信息。"""
        # 更新宗教、文化等信息
        self.update_info_label("Religion:", character_data.religion)
        self.update_info_label("Culture:", character_data.culture)
        self.update_birth_death(character_data.birth_date, character_data.death_date)

    def update_info_label(self, label_text, value):
        """创建或更新左侧属性面板的文本标签。"""
        tk.Label(self.attributes_frame, text=f"{label_text} {value}", anchor="w", justify=tk.LEFT).grid(
            row=len(self.attributes_frame.winfo_children()), column=0, sticky="w", pady=(0, 10))

    def update_birth_death(self, birth_date, death_date):
        """更新出生和死亡日期。"""
        birth_death_frame = tk.Frame(self.attributes_frame)
        birth_death_frame.grid(row=len(self.attributes_frame.winfo_children()), column=0, sticky="w", pady=(0, 10))

        tk.Label(birth_death_frame, text=f"Birth Date: {birth_date}", anchor="w", justify=tk.LEFT).pack(side=tk.LEFT,
                                                                                                        padx=(0, 10))
        tk.Label(birth_death_frame, text=f"Death Date: {death_date}", anchor="w", justify=tk.LEFT).pack(side=tk.LEFT)

    def update_right_side(self, character_data):
        """更新右侧属性数值和特质。"""
        for index, (attr, value) in enumerate([
            ("Martial", character_data.martial),
            ("Diplomacy", character_data.diplomacy),
            ("Intrigue", character_data.intrigue),
            ("Stewardship", character_data.stewardship),
        ]):
            self.create_attribute_entry(attr, value, index)

        # 特质显示
        print("Before calling display_traits")

        # 在属性数值下方创建特质显示区域
        self.trait_frame = tk.Frame(self.editor_frame, padx=20, pady=20)  # 增加与左侧容器的水平间距
        self.trait_frame.pack(side=tk.RIGHT, anchor=tk.N, fill=tk.BOTH)  # 调整布局以适应右侧

        # 调用特质显示方法，现在在新的trait_frame中
        self.display_traits(character_data.traits, self.trait_frame)

        print("After calling display_traits")

    def create_attribute_entry(self, attribute, value, index):
        """为属性创建输入框。"""
        if attribute in self.attribute_images:
            img_label = tk.Label(self.attributes_frame, image=self.attribute_images[attribute])
            img_label.image = self.attribute_images[attribute]  # 防止图像被垃圾回收
            img_label.grid(row=index, column=1, sticky="w", pady=(index * 10, 0))

            value_var = tk.StringVar(value=str(value))
            tk.Entry(self.attributes_frame, textvariable=value_var, width=5).grid(row=index, column=2, sticky="e",
                                                                                  pady=(index * 10, 0))

            # 绑定回调
            value_var.trace("w",
                            lambda *args, attr_=attribute, var=value_var: self.on_attribute_change(attr_, var.get()))