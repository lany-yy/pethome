"""
统一样式配置
定义所有界面的颜色、字体和样式
"""

from kivy.core.text import LabelBase
CHINESE_FONT = 'Chinese'

# ==================== 颜色配置 ====================
class Colors:
    """统一颜色配置"""
    # 主色调 - 明亮的蓝色系
    PRIMARY = (0.29, 0.56, 0.85, 1)           # #4A90D9 - 主按钮、标题栏
    PRIMARY_LIGHT = (0.45, 0.68, 0.92, 1)     # #73AFF0 - 悬停状态
    PRIMARY_DARK = (0.22, 0.44, 0.70, 1)      # #3870B3 - 按下状态
    
    # 辅助色 - 绿色系（成功、添加）
    SUCCESS = (0.30, 0.75, 0.45, 1)           # #4DBF73 - 添加按钮
    SUCCESS_LIGHT = (0.45, 0.85, 0.58, 1)     # #73D994
    SUCCESS_DARK = (0.22, 0.60, 0.35, 1)      # #389959
    
    # 警告色 - 红色系（删除、危险）
    DANGER = (0.85, 0.35, 0.35, 1)            # #D95959 - 删除按钮
    DANGER_LIGHT = (0.92, 0.50, 0.50, 1)      # #EB8080
    DANGER_DARK = (0.70, 0.25, 0.25, 1)       # #B34040
    
    # 警告色 - 橙色系（提醒、注意）
    WARNING = (0.95, 0.65, 0.25, 1)           # #F2A640
    WARNING_LIGHT = (0.98, 0.78, 0.45, 1)     # #FAC773
    
    # 中性色
    GRAY_DARK = (0.25, 0.25, 0.25, 1)         # #404040 - 标题文字
    GRAY = (0.45, 0.45, 0.45, 1)              # #737373 - 普通文字
    GRAY_LIGHT = (0.65, 0.65, 0.65, 1)        # #A6A6A6 - 次要文字
    GRAY_LIGHTER = (0.85, 0.85, 0.85, 1)      # #D9D9D9 - 边框、分割线
    
    # 背景色
    BG_WHITE = (1, 1, 1, 1)                   # #FFFFFF - 卡片背景
    BG_LIGHT = (0.97, 0.97, 0.97, 1)          # #F7F7F7 - 页面背景
    BG_GRAY = (0.94, 0.94, 0.94, 1)           # #F0F0F0 - 次级背景
    
    # 文字色
    TEXT_PRIMARY = (0, 0, 0, 1)                # #000000 - 主要文字（黑色）
    TEXT_SECONDARY = (0, 0, 0, 1)              # #000000 - 次要文字（黑色）
    TEXT_HINT = (0, 0, 0, 1)                   # #000000 - 提示文字（黑色）
    TEXT_WHITE = (1, 1, 1, 1)                 # #FFFFFF - 白色文字（用于深色背景）
    
    # 特殊色
    CAT_COLOR = (1, 0.75, 0.80, 1)            # #FFC0CC - 猫咪粉色
    DOG_COLOR = (0.75, 0.85, 1, 1)            # #BFD9FF - 狗狗蓝色

# ==================== 字体配置 ====================
class Fonts:
    """统一字体配置"""
    TITLE = '24sp'        # 页面标题
    SUBTITLE = '20sp'     # 副标题
    BODY = '16sp'         # 正文
    BODY_SMALL = '14sp'   # 小号正文
    CAPTION = '12sp'      # 说明文字
    BUTTON = '16sp'       # 按钮文字

# ==================== 尺寸配置 ====================
class Sizes:
    """统一尺寸配置"""
    # 间距
    PADDING_LARGE = 20
    PADDING_MEDIUM = 15
    PADDING_SMALL = 10
    
    # 圆角
    RADIUS_LARGE = 16
    RADIUS_MEDIUM = 12
    RADIUS_SMALL = 8
    
    # 高度
    BUTTON_HEIGHT = 50
    INPUT_HEIGHT = 50
    CARD_HEIGHT = 70
    TITLE_BAR_HEIGHT = 60

# ==================== 样式辅助函数 ====================
def create_card(widget, bg_color=Colors.BG_WHITE, radius=Sizes.RADIUS_MEDIUM):
    """为控件添加卡片背景"""
    from kivy.graphics import Color, RoundedRectangle
    with widget.canvas.before:
        Color(*bg_color)
        RoundedRectangle(size=widget.size, pos=widget.pos, radius=[radius])
    widget.bind(size=lambda i, v: setattr(widget.canvas.before.children[-1], 'size', v))
    widget.bind(pos=lambda i, v: setattr(widget.canvas.before.children[-1], 'pos', v))