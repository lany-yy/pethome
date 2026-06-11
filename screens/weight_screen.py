"""
体重记录界面
"""

from kivy.core.text import LabelBase
CHINESE_FONT = 'Chinese'

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.metrics import dp
from kivy.graphics import Color, RoundedRectangle

from database.pet_db import PetDatabase
from utils.styles import Colors, Fonts, Sizes

class WeightScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pet_id = None
        self.setup_ui()
    
    def setup_ui(self):
        self.main_layout = BoxLayout(orientation='vertical', padding=0, spacing=0)
        
        # 顶部标题栏 - 使用主色调背景
        top_bar = BoxLayout(size_hint_y=None, height=dp(Sizes.TITLE_BAR_HEIGHT), spacing=dp(10))
        with top_bar.canvas.before:
            Color(*Colors.PRIMARY)
            RoundedRectangle(size=top_bar.size, pos=top_bar.pos, radius=[0])
        top_bar.bind(size=lambda i, v: setattr(top_bar.canvas.before.children[-1], 'size', v))
        top_bar.bind(pos=lambda i, v: setattr(top_bar.canvas.before.children[-1], 'pos', v))
        
        back_btn = Button(
            text='返回',
            size_hint_x=0.18,
            background_color=(0, 0, 0, 0),
            font_name=CHINESE_FONT,
            font_size=Fonts.BUTTON,
            color=Colors.TEXT_PRIMARY
        )
        back_btn.bind(on_press=self.go_back)
        title = Label(
            text='体重记录',
            font_size=Fonts.TITLE,
            color=Colors.TEXT_WHITE,
            font_name=CHINESE_FONT,
            bold=True
        )
        top_bar.add_widget(back_btn)
        top_bar.add_widget(title)
        top_bar.add_widget(Label(size_hint_x=0.18))
        self.main_layout.add_widget(top_bar)
        
        self.content_layout = BoxLayout(orientation='vertical', size_hint_y=0.9, padding=dp(Sizes.PADDING_MEDIUM))
        # 设置背景色
        with self.content_layout.canvas.before:
            Color(*Colors.BG_LIGHT)
            RoundedRectangle(size=self.content_layout.size, pos=self.content_layout.pos, radius=[0])
        self.content_layout.bind(size=lambda i, v: setattr(self.content_layout.canvas.before.children[-1], 'size', v))
        self.content_layout.bind(pos=lambda i, v: setattr(self.content_layout.canvas.before.children[-1], 'pos', v))
        self.main_layout.add_widget(self.content_layout)
        
        self.add_widget(self.main_layout)
    
    def on_enter(self):
        self.content_layout.clear_widgets()
        
        if hasattr(self.manager, 'pet_id') and self.manager.pet_id:
            self.pet_id = self.manager.pet_id
            self.show_weight_form()
        else:
            self.show_pet_selection()
    
    def show_pet_selection(self):
        layout = BoxLayout(orientation='vertical', padding=dp(Sizes.PADDING_MEDIUM), spacing=dp(Sizes.PADDING_SMALL))
        
        layout.add_widget(Label(
            text='请选择宠物',
            font_size=Fonts.SUBTITLE,
            font_name=CHINESE_FONT,
            bold=True,
            color=Colors.TEXT_PRIMARY
        ))
        
        pets = PetDatabase.get_all_pets()
        
        if not pets:
            layout.add_widget(Label(
                text='暂无宠物',
                font_size=Fonts.BODY,
                color=Colors.TEXT_HINT,
                font_name=CHINESE_FONT
            ))
            add_btn = Button(
                text='添加宠物',
                size_hint_y=0.1,
                background_color=Colors.SUCCESS,
                font_name=CHINESE_FONT,
                font_size=Fonts.BUTTON,
                color=Colors.TEXT_WHITE
            )
            add_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'add_pet'))
            layout.add_widget(add_btn)
        else:
            pet_grid = GridLayout(cols=1, spacing=dp(Sizes.PADDING_SMALL), size_hint_y=None, row_default_height=dp(Sizes.CARD_HEIGHT))
            pet_grid.bind(minimum_height=pet_grid.setter('height'))
            
            for pet in pets:
                pet_id, name, pet_type = pet[0], pet[1], pet[2]
                pet_type_text = '🐱' if pet_type == 'cat' else '🐶'
                
                btn = Button(
                    text=f'{pet_type_text} {name}',
                    font_name=CHINESE_FONT,
                    font_size=Fonts.BODY,
                    background_color=Colors.BG_WHITE,
                    color=Colors.TEXT_PRIMARY
                )
                btn.bind(on_press=lambda x, pid=pet_id: self.select_pet(pid))
                pet_grid.add_widget(btn)
            
            scroll = ScrollView()
            scroll.add_widget(pet_grid)
            layout.add_widget(scroll)
        
        self.content_layout.add_widget(layout)
    
    def select_pet(self, pet_id):
        self.pet_id = pet_id
        self.manager.pet_id = pet_id
        self.show_weight_form()
    
    def show_weight_form(self):
        self.content_layout.clear_widgets()
        
        pet = PetDatabase.get_pet_by_id(self.pet_id)
        pet_name = pet[1] if pet else '未知宠物'
        
        scroll = ScrollView()
        main_content = BoxLayout(orientation='vertical', spacing=dp(Sizes.PADDING_MEDIUM), size_hint_y=None, padding=dp(Sizes.PADDING_SMALL))
        main_content.bind(minimum_height=main_content.setter('height'))
        
        # 宠物信息卡片
        pet_info_card = BoxLayout(orientation='horizontal', padding=dp(Sizes.PADDING_MEDIUM), size_hint_y=None, height=dp(50))
        with pet_info_card.canvas.before:
            Color(*Colors.BG_GRAY)
            RoundedRectangle(size=pet_info_card.size, pos=pet_info_card.pos, radius=[dp(Sizes.RADIUS_SMALL)])
        pet_info_card.bind(size=lambda i, v: setattr(pet_info_card.canvas.before.children[-1], 'size', v))
        pet_info_card.bind(pos=lambda i, v: setattr(pet_info_card.canvas.before.children[-1], 'pos', v))
        pet_info_card.add_widget(Label(
            text=f'当前宠物：{pet_name}',
            font_size=Fonts.BODY,
            font_name=CHINESE_FONT,
            color=Colors.TEXT_SECONDARY
        ))
        main_content.add_widget(pet_info_card)
        
        # 表单卡片
        form_card = BoxLayout(orientation='vertical', padding=dp(Sizes.PADDING_LARGE), spacing=dp(Sizes.PADDING_MEDIUM), size_hint_y=None, height=dp(320))
        with form_card.canvas.before:
            Color(*Colors.BG_WHITE)
            RoundedRectangle(size=form_card.size, pos=form_card.pos, radius=[dp(Sizes.RADIUS_MEDIUM)])
        form_card.bind(size=lambda i, v: setattr(form_card.canvas.before.children[-1], 'size', v))
        form_card.bind(pos=lambda i, v: setattr(form_card.canvas.before.children[-1], 'pos', v))
        
        form_card.add_widget(Label(
            text='添加体重记录',
            font_size=Fonts.SUBTITLE,
            bold=True,
            font_name=CHINESE_FONT,
            color=Colors.TEXT_PRIMARY
        ))
        
        weight_row = BoxLayout(spacing=dp(Sizes.PADDING_MEDIUM), size_hint_y=None, height=dp(Sizes.INPUT_HEIGHT))
        weight_label = Label(
            text='体重 (kg)',
            font_size=Fonts.BODY,
            size_hint_x=0.3,
            halign='right',
            font_name=CHINESE_FONT,
            color=Colors.TEXT_SECONDARY
        )
        weight_label.bind(size=weight_label.setter('text_size'))
        self.weight_input = TextInput(
            hint_text='请输入体重',
            size_hint_x=0.7,
            font_name=CHINESE_FONT,
            font_size=Fonts.BODY,
            multiline=False,
            background_color=Colors.BG_GRAY,
            foreground_color=Colors.TEXT_PRIMARY
        )
        weight_row.add_widget(weight_label)
        weight_row.add_widget(self.weight_input)
        form_card.add_widget(weight_row)
        
        date_row = BoxLayout(spacing=dp(Sizes.PADDING_MEDIUM), size_hint_y=None, height=dp(Sizes.INPUT_HEIGHT))
        date_label = Label(
            text='记录日期',
            font_size=Fonts.BODY,
            size_hint_x=0.3,
            halign='right',
            font_name=CHINESE_FONT,
            color=Colors.TEXT_SECONDARY
        )
        date_label.bind(size=date_label.setter('text_size'))
        self.date_input = TextInput(
            hint_text='YYYY-MM-DD',
            size_hint_x=0.7,
            font_name=CHINESE_FONT,
            font_size=Fonts.BODY,
            multiline=False,
            background_color=Colors.BG_GRAY,
            foreground_color=Colors.TEXT_PRIMARY
        )
        date_row.add_widget(date_label)
        date_row.add_widget(self.date_input)
        form_card.add_widget(date_row)
        
        add_btn = Button(
            text='添加记录',
            size_hint_y=None,
            height=dp(Sizes.BUTTON_HEIGHT),
            background_color=Colors.SUCCESS,
            font_name=CHINESE_FONT,
            font_size=Fonts.BUTTON,
            color=Colors.TEXT_WHITE
        )
        add_btn.bind(on_press=self.save_weight)
        form_card.add_widget(add_btn)
        
        main_content.add_widget(form_card)
        
        main_content.add_widget(Label(
            text='历史记录',
            font_size=Fonts.BODY,
            bold=True,
            font_name=CHINESE_FONT,
            color=Colors.TEXT_PRIMARY,
            size_hint_y=None,
            height=dp(40)
        ))
        
        self.show_history(main_content)
        
        scroll.add_widget(main_content)
        self.content_layout.add_widget(scroll)
    
    def show_history(self, parent_layout):
        weights = PetDatabase.get_weight_history(self.pet_id)
        
        if not weights:
            parent_layout.add_widget(Label(
                text='暂无体重记录',
                font_size=Fonts.BODY_SMALL,
                color=Colors.TEXT_HINT,
                font_name=CHINESE_FONT
            ))
            return
        
        history_grid = GridLayout(cols=1, spacing=dp(Sizes.PADDING_SMALL), size_hint_y=None, row_default_height=dp(Sizes.CARD_HEIGHT))
        history_grid.bind(minimum_height=history_grid.setter('height'))
        
        for weight in weights:
            card = BoxLayout(orientation='horizontal', padding=dp(Sizes.PADDING_SMALL), spacing=dp(Sizes.PADDING_MEDIUM), size_hint_y=None, height=dp(Sizes.CARD_HEIGHT))
            with card.canvas.before:
                Color(*Colors.BG_WHITE)
                RoundedRectangle(size=card.size, pos=card.pos, radius=[dp(Sizes.RADIUS_SMALL)])
            card.bind(size=lambda i, v: setattr(card.canvas.before.children[-1], 'size', v))
            card.bind(pos=lambda i, v: setattr(card.canvas.before.children[-1], 'pos', v))
            
            card.add_widget(Label(
                text=f'{weight[1]} kg',
                font_size=Fonts.BODY,
                bold=True,
                font_name=CHINESE_FONT,
                color=Colors.TEXT_PRIMARY,
                size_hint_x=0.35
            ))
            card.add_widget(Label(
                text=f'记录日期：{weight[0]}',
                font_size=Fonts.BODY_SMALL,
                color=Colors.TEXT_SECONDARY,
                font_name=CHINESE_FONT
            ))
            
            history_grid.add_widget(card)
        
        parent_layout.add_widget(history_grid)
    
    def save_weight(self, instance):
        weight_text = self.weight_input.text.strip()
        date = self.date_input.text.strip()
        
        if not weight_text:
            self.show_error('请输入体重')
            return
        
        try:
            weight = float(weight_text)
        except ValueError:
            self.show_error('请输入有效的体重数值')
            return
        
        if not date:
            self.show_error('请输入记录日期')
            return
        
        PetDatabase.add_weight(self.pet_id, weight, date)
        
        self.weight_input.text = ''
        self.date_input.text = ''
        
        self.show_weight_form()
    
    def show_error(self, message):
        popup = Popup(
            title='错误',
            content=Label(text=message, font_name=CHINESE_FONT, color=Colors.TEXT_PRIMARY),
            size_hint=(0.6, 0.3),
            title_font=CHINESE_FONT,
            title_color=Colors.TEXT_PRIMARY
        )
        popup.open()
    
    def go_back(self, instance):
        self.manager.current = 'main'