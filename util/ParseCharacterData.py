import re
from common.models.CharacterAttributes import CharacterAttributes


class ParseCharacterData:
    def __init__(self):
        pass

    # 定义解析方法
    def parse_characterdata(self, file_path):
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

