import sys
from tkinter import filedialog
from util.ParseCharacterData import ParseCharacterData
from tkinter import messagebox
import tkinter as tk

class FileOpener:
    def __init__(self, gui_instance):
        self.gui = gui_instance

    def open_file(self):
        """实现打开文件功能，并检查文件路径是否符合要求"""
        file_path: str = filedialog.askopenfilename()
        print(f"Sele" f"cted file path: {file_path}")

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
        parser: ParseCharacterData = ParseCharacterData()
        print(f"Calling method: {parser.parse_characterdata.__qualname__}")
        character_data = parser.parse_characterdata(file_path)

        self.gui.filename = file_path  # 通过gui实例更新文件路径
        self.gui.character_data = character_data  # 更新gui实例的character_data

        # 设置通用头像
        image_path = "img/PlaceholderHead.png"
        try:
            self.character_image = tk.PhotoImage(file=image_path)
            self.character_image_label.config(image=self.character_image)
        except Exception as e:
            print(f"Error loading image: {e}", file=sys.stderr)
            messagebox.showerror("Error", f"Failed to load image: {e}")
            return

        # 初始化左右两侧的Frame
        left_frame = tk.Frame(self.attributes_frame, padx=10, pady=10)
        right_frame = tk.Frame(self.attributes_frame, padx=10, pady=10)
        left_frame.grid(row=0, column=0, sticky="nsew")  # 左侧Frame
        right_frame.grid(row=0, column=1, sticky="nsew")  # 右侧Frame

        # 在left_frame中预留一个位置用于稍后添加特质图片展示
        self.trait_frame_placeholder = tk.Frame(left_frame, padx=10, pady=10)  # 预留空间
        self.trait_frame_placeholder.grid(row=len(character_data.traits) + 3, column=0, sticky="w")

        # 左侧Frame中的内容布局
        self.name_label.config(text=f"Name: {character_data.name}")
        self.name_label.grid(row=0, column=0, sticky="w", pady=(0, 10))

        row_index = 1  # 初始化行索引
        religion_label = tk.Label(left_frame, text=f"Religion: {character_data.religion}", anchor="w",
                                  justify=tk.LEFT)
        religion_label.grid(row=row_index, column=0, sticky="w", pady=(0, 10))
        row_index += 1  # 增加行索引

        culture_label = tk.Label(left_frame, text=f"Culture: {character_data.culture}", anchor="w", justify=tk.LEFT)
        culture_label.grid(row=row_index, column=0, sticky="w", pady=(0, 10))
        row_index += 1  # 增加行索引

        birth_death_frame = tk.Frame(left_frame)
        birth_death_frame.grid(row=row_index, column=0, sticky="w", pady=(0, 10))

        birth_label = tk.Label(birth_death_frame, text=f"Birth Date: {character_data.birth_date}", anchor="w",
                               justify=tk.LEFT)
        birth_label.pack(side=tk.LEFT, padx=(0, 10))

        death_label = tk.Label(birth_death_frame, text=f"Death Date: {character_data.death_date}", anchor="w",
                               justify=tk.LEFT)
        death_label.pack(side=tk.LEFT)

        # 右侧Frame中的属性布局
        for index, (attr, value) in enumerate([
            ("Martial", character_data.martial),
            ("Diplomacy", character_data.diplomacy),
            ("Intrigue", character_data.intrigue),
            ("Stewardship", character_data.stewardship),
        ]):
            if attr in self.attribute_images:
                img_label = tk.Label(right_frame, image=self.attribute_images[attr])
                img_label.image = self.attribute_images[attr]
                img_label.grid(row=index, column=0, sticky="w", pady=(index * 10, 0))  # 根据行号调整间距

                value_var = tk.StringVar(value=str(value))  # 注意转换为字符串绑定
                value_entry = tk.Entry(right_frame, textvariable=value_var, width=5)
                value_entry.grid(row=index, column=1, sticky="e", pady=(index * 10, 0))  # 与图片对齐

                # 立即绑定attr的当前值到lambda函数中
                value_var.trace("w",
                                lambda *args, attr_=attr, var=value_var: self.on_attribute_change(attr_, var.get()))

        # 处理特质布局
        self.display_traits(character_data.traits, self.trait_frame_placeholder)  # 传递trait_frame的占位符

        # 设置Grid的权重，使左右两侧自适应窗口大小
        self.attributes_frame.columnconfigure(0, weight=1)
        self.attributes_frame.columnconfigure(1, weight=1)