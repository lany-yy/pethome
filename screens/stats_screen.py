"""
健康统计界面
"""

from kivy.core.text import LabelBase
CHINESE_FONT = 'Chinese'

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner, SpinnerOption
from kivy.metrics import dp
from kivy.graphics import Color, RoundedRectangle

from database.pet_db import PetDatabase
from utils.styles import Colors, Fonts, Sizes

class ChineseSpinnerOption(SpinnerOption):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_name = CHINESE_FONT

class StatsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pet_id = None
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
            text='健康统计',
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
        self.load_stats()
    
    def load_stats(self):
        pets = PetDatabase.get_all_pets()
        
        if not pets:
            empty_card = BoxLayout(orientation='vertical', padding=dp(30), spacing=dp(15), size_hint_y=None, height=dp(150))
            with empty_card.canvas.before:
                Color(*Colors.BG_WHITE)
                RoundedRectangle(size=empty_card.size, pos=empty_card.pos, radius=[dp(Sizes.RADIUS_MEDIUM)])
            empty_card.bind(
                size=lambda i, v: setattr(i.canvas.before.children[-1], 'size', v),
                pos=lambda i, v: setattr(i.canvas.before.children[-1], 'pos', v)
            )
            
            empty_card.add_widget(Label(
                text='暂无宠物数据',
                font_size=Fonts.BODY,
                color=Colors.TEXT_SECONDARY,
                font_name=CHINESE_FONT
            ))
            empty_card.add_widget(Label(
                text='请先添加宠物',
                font_size=Fonts.BODY_SMALL,
                color=Colors.TEXT_HINT,
                font_name=CHINESE_FONT
            ))
            self.content_layout.add_widget(empty_card)
            return
        
        scroll = ScrollView()
        content = BoxLayout(orientation='vertical', spacing=dp(20), size_hint_y=None, padding=[dp(5), dp(5), dp(5), dp(5)])
        content.bind(minimum_height=content.setter('height'))
        
        # 整体统计卡片
        overall_card = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15), size_hint_y=None, height=dp(220))
        with overall_card.canvas.before:
            Color(*Colors.BG_WHITE)
            RoundedRectangle(size=overall_card.size, pos=overall_card.pos, radius=[dp(Sizes.RADIUS_MEDIUM)])
        overall_card.bind(
            size=lambda i, v: setattr(i.canvas.before.children[-1], 'size', v),
            pos=lambda i, v: setattr(i.canvas.before.children[-1], 'pos', v)
        )
        
        overall_card.add_widget(Label(
            text='整体统计概览',
            font_size=Fonts.SUBTITLE,
            bold=True,
            color=Colors.TEXT_PRIMARY,
            font_name=CHINESE_FONT
        ))
        
        stats = PetDatabase.get_overall_stats()
        stats_grid = GridLayout(cols=2, spacing=dp(15), size_hint_y=None, height=dp(120))
        
        stats_items = [
            ('宠物总数', stats['total_pets'], Colors.PRIMARY),
            ('疫苗记录', stats['total_vaccines'], Colors.SUCCESS),
            ('体重记录', stats['total_weights'], Colors.WARNING),
            ('待办提醒', stats['pending_reminders'], Colors.DANGER)
        ]
        
        for label, value, color in stats_items:
            stat_card = BoxLayout(orientation='vertical', padding=dp(10), size_hint_y=None, height=dp(55))
            with stat_card.canvas.before:
                Color(*color)
                RoundedRectangle(size=stat_card.size, pos=stat_card.pos, radius=[dp(Sizes.RADIUS_SMALL)])
            stat_card.bind(
                size=lambda i, v: setattr(i.canvas.before.children[-1], 'size', v),
                pos=lambda i, v: setattr(i.canvas.before.children[-1], 'pos', v)
            )
            stat_card.add_widget(Label(
                text=str(value),
                font_size=Fonts.TITLE,
                bold=True,
                color=Colors.TEXT_WHITE,
                font_name=CHINESE_FONT
            ))
            stat_card.add_widget(Label(
                text=label,
                font_size=Fonts.CAPTION,
                color=Colors.TEXT_WHITE,
                font_name=CHINESE_FONT
            ))
            stats_grid.add_widget(stat_card)
        
        overall_card.add_widget(stats_grid)
        content.add_widget(overall_card)
        
        # 宠物类型分布
        type_card = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15), size_hint_y=None, height=dp(150))
        with type_card.canvas.before:
            Color(*Colors.BG_WHITE)
            RoundedRectangle(size=type_card.size, pos=type_card.pos, radius=[dp(Sizes.RADIUS_MEDIUM)])
        type_card.bind(
            size=lambda i, v: setattr(i.canvas.before.children[-1], 'size', v),
            pos=lambda i, v: setattr(i.canvas.before.children[-1], 'pos', v)
        )
        
        type_card.add_widget(Label(
            text='宠物类型分布',
            font_size=Fonts.SUBTITLE,
            bold=True,
            color=Colors.TEXT_PRIMARY,
            font_name=CHINESE_FONT
        ))
        
        cat_count = sum(1 for p in pets if p[2] == 'cat')
        dog_count = sum(1 for p in pets if p[2] == 'dog')
        total = cat_count + dog_count
        
        type_grid = GridLayout(cols=2, spacing=dp(15))
        
        if total > 0:
            cat_percent = (cat_count / total) * 100
            dog_percent = (dog_count / total) * 100
            
            cat_bar = BoxLayout(orientation='vertical', spacing=dp(5))
            cat_bar.add_widget(Label(
                text=f'猫咪',
                font_size=Fonts.BODY_SMALL,
                color=Colors.TEXT_PRIMARY,
                font_name=CHINESE_FONT
            ))
            cat_bg = BoxLayout(size_hint_y=None, height=dp(20))
            with cat_bg.canvas.before:
                Color(*Colors.GRAY_LIGHTER)
                RoundedRectangle(size=cat_bg.size, pos=cat_bg.pos, radius=[dp(10)])
            cat_bg.bind(
                size=lambda i, v: setattr(i.canvas.before.children[-1], 'size', v),
                pos=lambda i, v: setattr(i.canvas.before.children[-1], 'pos', v)
            )
            
            cat_fill = BoxLayout(size_hint_x=cat_percent / 100, size_hint_y=1)
            with cat_fill.canvas.before:
                Color(*Colors.CAT_COLOR)
                RoundedRectangle(size=cat_fill.size, pos=cat_fill.pos, radius=[dp(10)])
            cat_fill.bind(
                size=lambda i, v: setattr(i.canvas.before.children[-1], 'size', v),
                pos=lambda i, v: setattr(i.canvas.before.children[-1], 'pos', v)
            )
            cat_bg.add_widget(cat_fill)
            cat_bar.add_widget(cat_bg)
            cat_bar.add_widget(Label(
                text=f'{cat_count} 只 ({cat_percent:.1f}%)',
                font_size=Fonts.CAPTION,
                color=Colors.TEXT_SECONDARY,
                font_name=CHINESE_FONT
            ))
            type_grid.add_widget(cat_bar)
            
            dog_bar = BoxLayout(orientation='vertical', spacing=dp(5))
            dog_bar.add_widget(Label(
                text=f'狗狗',
                font_size=Fonts.BODY_SMALL,
                color=Colors.TEXT_PRIMARY,
                font_name=CHINESE_FONT
            ))
            dog_bg = BoxLayout(size_hint_y=None, height=dp(20))
            with dog_bg.canvas.before:
                Color(*Colors.GRAY_LIGHTER)
                RoundedRectangle(size=dog_bg.size, pos=dog_bg.pos, radius=[dp(10)])
            dog_bg.bind(
                size=lambda i, v: setattr(i.canvas.before.children[-1], 'size', v),
                pos=lambda i, v: setattr(i.canvas.before.children[-1], 'pos', v)
            )
            
            dog_fill = BoxLayout(size_hint_x=dog_percent / 100, size_hint_y=1)
            with dog_fill.canvas.before:
                Color(*Colors.DOG_COLOR)
                RoundedRectangle(size=dog_fill.size, pos=dog_fill.pos, radius=[dp(10)])
            dog_fill.bind(
                size=lambda i, v: setattr(i.canvas.before.children[-1], 'size', v),
                pos=lambda i, v: setattr(i.canvas.before.children[-1], 'pos', v)
            )
            dog_bg.add_widget(dog_fill)
            dog_bar.add_widget(dog_bg)
            dog_bar.add_widget(Label(
                text=f'{dog_count} 只 ({dog_percent:.1f}%)',
                font_size=Fonts.CAPTION,
                color=Colors.TEXT_SECONDARY,
                font_name=CHINESE_FONT
            ))
            type_grid.add_widget(dog_bar)
        else:
            type_grid.add_widget(Label(
                text='暂无数据',
                font_size=Fonts.BODY_SMALL,
                color=Colors.TEXT_HINT,
                font_name=CHINESE_FONT
            ))
        
        type_card.add_widget(type_grid)
        content.add_widget(type_card)
        
        # 单宠物统计
        content.add_widget(Label(
            text='宠物详情统计',
            font_size=Fonts.SUBTITLE,
            bold=True,
            color=Colors.TEXT_PRIMARY,
            font_name=CHINESE_FONT
        ))
        
        for pet in pets:
            pet_id, name, pet_type, _ = pet[0], pet[1], pet[2], pet[3]
            pet_stats = PetDatabase.get_pet_statistics(pet_id)
            
            pet_card = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(10), size_hint_y=None, height=dp(120))
            with pet_card.canvas.before:
                Color(*Colors.BG_WHITE)
                RoundedRectangle(size=pet_card.size, pos=pet_card.pos, radius=[dp(Sizes.RADIUS_MEDIUM)])
            pet_card.bind(
                size=lambda i, v: setattr(i.canvas.before.children[-1], 'size', v),
                pos=lambda i, v: setattr(i.canvas.before.children[-1], 'pos', v)
            )
            
            header = BoxLayout(orientation='horizontal', spacing=dp(10))
            icon_bg = BoxLayout(size_hint_x=None, width=dp(40), size_hint_y=None, height=dp(40))
            with icon_bg.canvas.before:
                Color(*Colors.CAT_COLOR if pet_type == 'cat' else Colors.DOG_COLOR)
                RoundedRectangle(size=icon_bg.size, pos=icon_bg.pos, radius=[dp(20)])
            icon_bg.bind(
                size=lambda i, v: setattr(i.canvas.before.children[-1], 'size', v),
                pos=lambda i, v: setattr(i.canvas.before.children[-1], 'pos', v)
            )
            icon_bg.add_widget(Label(
                text='🐱' if pet_type == 'cat' else '🐶',
                font_size='18sp'
            ))
            header.add_widget(icon_bg)
            
            info = BoxLayout(orientation='vertical', spacing=dp(3))
            info.add_widget(Label(
                text=name,
                font_size=Fonts.BODY,
                bold=True,
                color=Colors.TEXT_PRIMARY,
                font_name=CHINESE_FONT
            ))
            info.add_widget(Label(
                text='猫咪' if pet_type == 'cat' else '狗狗',
                font_size=Fonts.BODY_SMALL,
                color=Colors.TEXT_SECONDARY,
                font_name=CHINESE_FONT
            ))
            header.add_widget(info)
            pet_card.add_widget(header)
            
            stats_row = GridLayout(cols=3, spacing=dp(15))
            stats_row.add_widget(BoxLayout(orientation='vertical', spacing=dp(2)))
            stats_row.children[0].add_widget(Label(
                text=f'{pet_stats["vaccine_count"]}',
                font_size=Fonts.SUBTITLE,
                bold=True,
                color=Colors.SUCCESS,
                font_name=CHINESE_FONT
            ))
            stats_row.children[0].add_widget(Label(
                text='疫苗次数',
                font_size=Fonts.CAPTION,
                color=Colors.TEXT_SECONDARY,
                font_name=CHINESE_FONT
            ))
            
            stats_row.add_widget(BoxLayout(orientation='vertical', spacing=dp(2)))
            stats_row.children[0].add_widget(Label(
                text=f'{pet_stats["weight_count"]}',
                font_size=Fonts.SUBTITLE,
                bold=True,
                color=Colors.WARNING,
                font_name=CHINESE_FONT
            ))
            stats_row.children[0].add_widget(Label(
                text='体重记录',
                font_size=Fonts.CAPTION,
                color=Colors.TEXT_SECONDARY,
                font_name=CHINESE_FONT
            ))
            
            stats_row.add_widget(BoxLayout(orientation='vertical', spacing=dp(2)))
            stats_row.children[0].add_widget(Label(
                text=f'{pet_stats["pending_reminders"]}',
                font_size=Fonts.SUBTITLE,
                bold=True,
                color=Colors.DANGER if pet_stats["pending_reminders"] > 0 else Colors.SUCCESS,
                font_name=CHINESE_FONT
            ))
            stats_row.children[0].add_widget(Label(
                text='待办提醒',
                font_size=Fonts.CAPTION,
                color=Colors.TEXT_SECONDARY,
                font_name=CHINESE_FONT
            ))
            
            pet_card.add_widget(stats_row)
            content.add_widget(pet_card)
        
        scroll.add_widget(content)
        self.content_layout.add_widget(scroll)
    
    def go_back(self, instance):
        self.manager.current = 'main'