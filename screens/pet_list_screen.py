"""
宠物列表界面
"""

from kivy.core.text import LabelBase
CHINESE_FONT = 'Chinese'

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.metrics import dp
from kivy.graphics import Color, RoundedRectangle

from database.pet_db import PetDatabase
from utils.styles import Colors, Fonts, Sizes

class PetListScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup_ui()
    
    def setup_ui(self):
        self.main_layout = BoxLayout(orientation='vertical', padding=0, spacing=0)
        with self.main_layout.canvas.before:
            Color(*Colors.BG_LIGHT)
            self.bg_rect = RoundedRectangle(size=self.main_layout.size, pos=self.main_layout.pos)
        self.main_layout.bind(size=self._update_bg, pos=self._update_bg)
        
        # 顶部标题栏
        title_bar = BoxLayout(size_hint_y=None, height=dp(60), padding=[dp(15), dp(5), dp(15), dp(5)])
        with title_bar.canvas.before:
            Color(*Colors.PRIMARY)
            self.title_rect = RoundedRectangle(size=title_bar.size, pos=title_bar.pos)
        title_bar.bind(size=self._update_title_rect, pos=self._update_title_rect)
        
        back_btn = Button(
            text='← 返回',
            size_hint_x=0.2,
            background_color=(0, 0, 0, 0),
            font_name=CHINESE_FONT,
            font_size=Fonts.BODY,
            color=Colors.TEXT_PRIMARY
        )
        back_btn.bind(on_press=self.go_back)
        title = Label(
            text='宠物列表',
            font_size=Fonts.SUBTITLE,
            bold=True,
            color=Colors.TEXT_WHITE,
            font_name=CHINESE_FONT,
            size_hint_x=0.6
        )
        title_bar.add_widget(back_btn)
        title_bar.add_widget(title)
        title_bar.add_widget(Label(size_hint_x=0.2))
        self.main_layout.add_widget(title_bar)
        
        self.content_layout = BoxLayout(orientation='vertical', size_hint_y=0.9, padding=dp(15))
        self.main_layout.add_widget(self.content_layout)
        
        self.add_widget(self.main_layout)
    
    def _update_bg(self, instance, value):
        self.bg_rect.size = value
    
    def _update_title_rect(self, instance, value):
        self.title_rect.size = value
    
    def on_enter(self):
        self.content_layout.clear_widgets()
        
        pets = PetDatabase.get_all_pets()
        
        if not pets:
            empty_card = BoxLayout(orientation='vertical', padding=dp(30), spacing=dp(20))
            with empty_card.canvas.before:
                Color(*Colors.BG_WHITE)
                RoundedRectangle(size=empty_card.size, pos=empty_card.pos, radius=[dp(Sizes.RADIUS_MEDIUM)])
            empty_card.bind(
                size=lambda i, v: setattr(i.canvas.before.children[-1], 'size', v),
                pos=lambda i, v: setattr(i.canvas.before.children[-1], 'pos', v)
            )
            
            empty_card.add_widget(Label(
                text='🐾',
                font_size='48sp'
            ))
            empty_card.add_widget(Label(
                text='暂无宠物',
                font_size=Fonts.SUBTITLE,
                color=Colors.TEXT_SECONDARY,
                font_name=CHINESE_FONT
            ))
            empty_card.add_widget(Label(
                text='点击"添加宠物"开始记录',
                font_size=Fonts.BODY_SMALL,
                color=Colors.TEXT_HINT,
                font_name=CHINESE_FONT
            ))
            
            add_btn = Button(
                text='添加宠物',
                size_hint_y=None,
                height=dp(Sizes.BUTTON_HEIGHT),
                background_color=Colors.SUCCESS,
                font_name=CHINESE_FONT,
                font_size=Fonts.BUTTON,
                color=Colors.TEXT_WHITE
            )
            add_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'add_pet'))
            empty_card.add_widget(add_btn)
            
            self.content_layout.add_widget(empty_card)
        else:
            scroll = ScrollView()
            grid = GridLayout(cols=1, spacing=dp(12), size_hint_y=None, padding=[dp(5), dp(5), dp(5), dp(5)])
            grid.bind(minimum_height=grid.setter('height'))
            
            for pet in pets:
                pet_id, name, pet_type = pet[0], pet[1], pet[2]
                breed = pet[3] if len(pet) > 3 else ''
                
                card = BoxLayout(orientation='horizontal', padding=dp(15), spacing=dp(15), size_hint_y=None, height=dp(80))
                with card.canvas.before:
                    Color(*Colors.BG_WHITE)
                    RoundedRectangle(size=card.size, pos=card.pos, radius=[dp(Sizes.RADIUS_MEDIUM)])
                card.bind(
                    size=lambda i, v: setattr(i.canvas.before.children[-1], 'size', v),
                    pos=lambda i, v: setattr(i.canvas.before.children[-1], 'pos', v)
                )
                
                # 图标区域
                icon_bg = BoxLayout(size_hint_x=None, width=dp(50), size_hint_y=None, height=dp(50))
                with icon_bg.canvas.before:
                    Color(*Colors.CAT_COLOR if pet_type == 'cat' else Colors.DOG_COLOR)
                    RoundedRectangle(size=icon_bg.size, pos=icon_bg.pos, radius=[dp(25)])
                icon_bg.bind(
                    size=lambda i, v: setattr(i.canvas.before.children[-1], 'size', v),
                    pos=lambda i, v: setattr(i.canvas.before.children[-1], 'pos', v)
                )
                icon_bg.add_widget(Label(
                    text='🐱' if pet_type == 'cat' else '🐶',
                    font_size='24sp'
                ))
                card.add_widget(icon_bg)
                
                # 信息区域
                info = BoxLayout(orientation='vertical', spacing=dp(5), size_hint_x=0.7)
                info.add_widget(Label(
                    text=name,
                    font_size=Fonts.BODY,
                    bold=True,
                    color=Colors.TEXT_PRIMARY,
                    font_name=CHINESE_FONT,
                    halign='left',
                    valign='middle'
                ))
                info.children[0].bind(size=info.children[0].setter('text_size'))
                
                type_text = '猫咪' if pet_type == 'cat' else '狗狗'
                if breed:
                    type_text += f' · {breed}'
                info.add_widget(Label(
                    text=type_text,
                    font_size=Fonts.BODY_SMALL,
                    color=Colors.TEXT_SECONDARY,
                    font_name=CHINESE_FONT,
                    halign='left',
                    valign='middle'
                ))
                info.children[0].bind(size=info.children[0].setter('text_size'))
                card.add_widget(info)
                
                # 箭头
                arrow = Label(
                    text='›',
                    font_size='24sp',
                    color=Colors.GRAY_LIGHT,
                    size_hint_x=None,
                    width=dp(30)
                )
                card.add_widget(arrow)
                
                btn = Button(background_color=(0, 0, 0, 0), size_hint=(1, 1))
                btn.bind(on_press=lambda x, pid=pet_id: self.view_pet(pid))
                card.add_widget(btn)
                
                grid.add_widget(card)
            
            scroll.add_widget(grid)
            self.content_layout.add_widget(scroll)
    
    def view_pet(self, pet_id):
        self.manager.pet_id = pet_id
        self.manager.current = 'pet_detail'
    
    def go_back(self, instance):
        self.manager.current = 'main'