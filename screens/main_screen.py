"""
主界面
"""

from kivy.core.text import LabelBase
CHINESE_FONT = 'Chinese'

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.metrics import dp
from kivy.graphics import Color, RoundedRectangle

from utils.styles import Colors, Fonts, Sizes

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup_ui()
    
    def setup_ui(self):
        # 主布局 - 浅灰背景
        main_layout = BoxLayout(orientation='vertical', padding=0, spacing=0)
        with main_layout.canvas.before:
            Color(*Colors.BG_LIGHT)
            self.bg_rect = RoundedRectangle(size=main_layout.size, pos=main_layout.pos)
        main_layout.bind(size=self._update_bg, pos=self._update_bg)
        
        # 顶部标题栏 - 主色背景
        title_bar = BoxLayout(size_hint_y=None, height=dp(70), padding=[dp(20), dp(10), dp(20), dp(10)])
        with title_bar.canvas.before:
            Color(*Colors.PRIMARY)
            self.title_rect = RoundedRectangle(size=title_bar.size, pos=title_bar.pos)
        title_bar.bind(size=self._update_title_rect, pos=self._update_title_rect)
        
        title = Label(
            text='宠物管家',
            font_size=Fonts.TITLE,
            bold=True,
            color=Colors.TEXT_WHITE,
            font_name=CHINESE_FONT
        )
        title_bar.add_widget(title)
        main_layout.add_widget(title_bar)
        
        # 内容区域
        content = BoxLayout(orientation='vertical', padding=dp(25), spacing=dp(20))
        
        # 欢迎信息卡片
        welcome_card = BoxLayout(orientation='vertical', padding=dp(20), size_hint_y=None, height=dp(80), spacing=dp(5))
        with welcome_card.canvas.before:
            Color(*Colors.BG_WHITE)
            RoundedRectangle(size=welcome_card.size, pos=welcome_card.pos, radius=[dp(Sizes.RADIUS_MEDIUM)])
        welcome_card.bind(
            size=lambda i, v: setattr(welcome_card.canvas.before.children[-1], 'size', v),
            pos=lambda i, v: setattr(welcome_card.canvas.before.children[-1], 'pos', v)
        )
        
        welcome_card.add_widget(Label(
            text='欢迎使用宠物管家',
            font_size=Fonts.SUBTITLE,
            bold=True,
            color=Colors.TEXT_PRIMARY,
            font_name=CHINESE_FONT
        ))
        welcome_card.add_widget(Label(
            text='轻松管理您的爱宠信息',
            font_size=Fonts.BODY_SMALL,
            color=Colors.TEXT_SECONDARY,
            font_name=CHINESE_FONT
        ))
        content.add_widget(welcome_card)
        
        # 功能按钮网格
        grid = GridLayout(cols=2, spacing=dp(15), size_hint_y=0.7)
        
        buttons = [
            ('宠物列表', 'pet_list', Colors.PRIMARY),
            ('添加宠物', 'add_pet', Colors.SUCCESS),
            ('宠物种类', 'pet_types', Colors.WARNING),
            ('寄养管理', 'foster', Colors.PRIMARY_LIGHT),
            ('今日提醒', 'reminder', Colors.DANGER_LIGHT),
            ('健康统计', 'stats', Colors.SUCCESS_LIGHT)
        ]
        
        for text, screen_name, bg_color in buttons:
            # 使用 RelativeLayout 确保按钮覆盖整个卡片
            btn_rel = RelativeLayout(size_hint_y=None, height=dp(70))
            
            # 卡片背景
            btn_card = BoxLayout(orientation='vertical', padding=dp(10), size_hint=(1, 1))
            with btn_card.canvas.before:
                Color(*bg_color)
                RoundedRectangle(size=btn_card.size, pos=btn_card.pos, radius=[dp(Sizes.RADIUS_MEDIUM)])
            btn_card.bind(
                size=lambda i, v: setattr(i.canvas.before.children[-1], 'size', v),
                pos=lambda i, v: setattr(i.canvas.before.children[-1], 'pos', v)
            )
            
            btn_card.add_widget(Label(
                text=text,
                font_size=Fonts.BUTTON,
                bold=True,
                color=Colors.TEXT_WHITE,
                font_name=CHINESE_FONT
            ))
            
            btn_rel.add_widget(btn_card)
            
            # 透明按钮覆盖整个卡片区域
            btn = Button(
                background_color=(0, 0, 0, 0),
                size_hint=(1, 1)
            )
            btn.bind(on_press=lambda x, s=screen_name: self.go_to_screen(s))
            btn_rel.add_widget(btn)
            
            grid.add_widget(btn_rel)
        
        content.add_widget(grid)
        
        # 底部信息
        footer = Label(
            text='宠物管家 v1.0.0',
            font_size=Fonts.CAPTION,
            color=Colors.TEXT_HINT,
            font_name=CHINESE_FONT,
            size_hint_y=None,
            height=dp(30)
        )
        content.add_widget(footer)
        
        main_layout.add_widget(content)
        self.add_widget(main_layout)
    
    def _update_bg(self, instance, value):
        self.bg_rect.size = value
    
    def _update_title_rect(self, instance, value):
        self.title_rect.size = value
    
    def go_to_screen(self, screen_name):
        print(f"Navigating to: {screen_name}")
        self.manager.current = screen_name