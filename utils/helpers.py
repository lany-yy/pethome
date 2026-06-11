"""
工具函数模块
"""

from datetime import datetime, date

def format_date(date_str):
    """格式化日期字符串"""
    try:
        if date_str:
            return datetime.strptime(date_str, '%Y-%m-%d').strftime('%Y年%m月%d日')
    except:
        pass
    return date_str

def get_age(birthday_str):
    """计算年龄"""
    try:
        if birthday_str:
            birthday = datetime.strptime(birthday_str, '%Y-%m-%d')
            today = date.today()
            age = today.year - birthday.year
            if (today.month, today.day) < (birthday.month, birthday.day):
                age -= 1
            return age
    except:
        pass
    return None

def validate_date(date_str):
    """验证日期格式"""
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False