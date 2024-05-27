import sys
import tkinter as tk
from tkinter import filedialog, Menu
from tkinter import messagebox
import os
from PIL import ImageTk,Image
import re



#本项目旨在为Crusader Kings III（CKIII）游戏的Mod制作提供一个便捷、直观的图形化编辑工具。
# 我们计划运用Python图形用户界面库，如Tkinter或PyQt，构建一款小型的Crusader Kings III Mod编辑器。
# 该编辑器的核心功能是将复杂的Mod代码以图文并茂的形式呈现，支持用户进行可视化操作，极大提升Mod编辑的易用性和效率。

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

#加载特质图片
def load_trait_images(folder_path):
    # 加载特质图片并返回字典，键为特质名称，值为对应的图片对象
    trait_images = {}
    for filename in os.listdir(folder_path):
        if filename.startswith("60px-Trait_") and filename.endswith(".png"):
            trait_name = filename[len("60px-Trait_"):-len(".png")]  # 提取特质名称
            print(f"Attempting to load trait image for '{trait_name}'")
            img_path = os.path.join(folder_path, filename)
            try:
                image = ImageTk.PhotoImage(Image.open(img_path))  # 使用 PIL.Image.open 来打开图片
                trait_images[trait_name.capitalize()] = image  # 存储图片对象到字典，特质名首字母大写
                print(f"Loaded trait image for '{trait_name}' successfully.")
            except IOError as e:
                print(f"Failed to load trait image for '{trait_name}': {e}")
    return trait_images


#定义解析方法
def parse_character_data(file_path):
    attributes = CharacterAttributes()
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

        # 调整属性匹配，使其更灵活地处理前后空白和注释
        for attr in ['name', 'martial', 'diplomacy', 'intrigue', 'stewardship', 'religion', 'culture']:
            # 此处使用更严格的匹配来确保匹配到完整的属性值直到遇到注释开始、下一个属性或者块结束
            pattern_str = attr + r'\s*=\s*([^#=]+?)[\s#}]'
            pattern = re.compile(pattern_str)
            match = pattern.search(content)
            if match:
                raw_value = match.group(1).strip()  # 分割并去除空白

                # 对于name属性特别处理，去除可能的引号
                if attr == 'name':
                    raw_value = raw_value.strip('\'"')  # 去除引号

                value = raw_value

                # 对于数值属性的处理逻辑保持不变
                if attr in ['martial', 'diplomacy', 'intrigue', 'stewardship']:
                    try:
                        value = int(value)
                    except ValueError:
                        print(f"Warning: Unable to convert '{raw_value}' for attribute '{attr}' to integer.")

                setattr(attributes, attr, value)

        # 特性(trait)匹配保持不变
        trait_pattern = re.compile('trait\s*=\s*([\w_]+)')
        traits = trait_pattern.findall(content)
        attributes.traits = traits

        # 精简日期匹配逻辑，确保只匹配必要的信息
        date_pattern = re.compile(r'(\d+)\.(\d+)\.(\d+)\s*=\s*\{\s*(birth|death)\s*=\s*yes\s*\}')
        dates = date_pattern.findall(content)
        for date_match in dates:
            year, month, day, event_type = date_match
            if event_type == 'birth':
                attributes.birth_date = f"{year}.{month}.{day}"
            elif event_type == 'death':
                attributes.death_date = f"{year}.{month}.{day}"

    return attributes

def load_attribute_images(attribute_folder):
    images = {}
    for attribute in ["Martial", "Diplomacy", "Intrigue", "Stewardship"]:
        img_path = os.path.join(attribute_folder, rf"{attribute}.png")
        print(f"Attempting to load: {img_path}")
        try:
            img = tk.PhotoImage(file=img_path)
            images[attribute] = img
        except Exception as e:
            print(f"Failed to load image for {attribute}: {e}")
    return images

class CrusaderKingsIIIEditor:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Crusader Kings III Mod Editor")
        self.root.geometry("800x600")

        self.menu_bar = Menu(self.root)
        self.root.config(menu=self.menu_bar)

        self.left_frame = None

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
        religion_label = tk.Label(left_frame, text=f"Religion: {character_data.religion}", anchor="w", justify=tk.LEFT)
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

                value_label = tk.Label(right_frame, text=value, anchor="e")
                value_label.grid(row=index, column=1, sticky="e", pady=(index * 10, 0))  # 与图片对齐

        # 处理特质布局
        self.display_traits(character_data.traits, self.trait_frame_placeholder)  # 传递trait_frame的占位符

        # 设置Grid的权重，使左右两侧自适应窗口大小
        self.attributes_frame.columnconfigure(0, weight=1)
        self.attributes_frame.columnconfigure(1, weight=1)



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
