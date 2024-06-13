import sys
from tkinter import filedialog
from util.ParseCharacterData import ParseCharacterData
from tkinter import messagebox
import tkinter as tk


class FileOpener:
    """
    类FileOpener负责处理文件打开操作，包括选择文件、验证路径以及解析文件内容。
    它依赖于Tkinter库进行图形界面操作，并与一个GUI实例交互以更新数据和界面。
    """

    def __init__(self, gui_instance):
        """
        初始化FileOpener类的实例。

        :param gui_instance: GUI类的一个实例，用于与GUI交互和更新数据。
        """
        self.gui = gui_instance

    def open_file(self):
        """
        实现打开文件对话框，让用户选择文件。选择后，检查文件路径是否位于
        "history/characters"目录下。如果路径正确，则解析文件内容并更新GUI实例的数据。

        :return: 无直接返回值，但会通过self.gui更新filename和character_data属性，
                 并调用gui的updata_character方法来反映这些变化。
        """
        file_path = filedialog.askopenfilename()
        if not file_path:
            print("File selection cancelled.")
            return

        if "history/characters" not in file_path:
            messagebox.showerror("Error", "Please open a file located under history/characters.")
            print("Invalid path error shown after checking full path.")
            return

        parser = ParseCharacterData()
        character_data = parser.parse_characterdata(file_path)

        # 更新GUI实例的文件路径和角色数据属性
        self.gui.filename = file_path
        self.gui.character_data = character_data

        # 调用GUI类的方法来利用新数据更新UI
        self.gui.update_character(character_data)





