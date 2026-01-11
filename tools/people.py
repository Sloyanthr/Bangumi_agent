# 基础搜索
def search_person_by_name(name: str):
    """搜索现实中的人物 (声优, 监督, 原作者)"""
    pass

def search_character_by_name(name: str):
    """搜索虚拟角色 (例如: 搜索 '御坂美琴')"""
    pass

# 角色详情
def get_character_profile(character_id: int):
    """获取角色的详细档案 (介绍, 性别, 身高, 出演过的动画)"""
    pass

# 动画 -> 人的映射
def get_anime_cast_list(subject_id: int):
    """获取某部动画的配音表 (角色名 -> 声优名 的对应关系)"""
    pass

def get_anime_staff_list(subject_id: int):
    """获取某部动画的幕后制作表 (只筛选监督, 脚本, 音乐, 制作公司)"""
    pass

# 人 -> 动画的映射 (进阶)
def get_person_works(person_id: int):
    """查询某位声优或监督最近参与的作品 (例如: 宫崎骏做过哪些动画?)"""
    pass