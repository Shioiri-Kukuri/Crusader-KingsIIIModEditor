
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