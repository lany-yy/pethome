"""
宠物种类管理界面
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

class PetTypesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup_ui()
    
    def setup_ui(self):
        self.main_layout = BoxLayout(orientation='vertical', padding=0, spacing=0)
        
        # 顶部标题栏 - 使用 PRIMARY 背景色
        top_bar = BoxLayout(size_hint_y=None, height=dp(Sizes.TITLE_BAR_HEIGHT), padding=dp(Sizes.PADDING_MEDIUM), spacing=dp(Sizes.PADDING_SMALL))
        with top_bar.canvas.before:
            Color(*Colors.PRIMARY)
            RoundedRectangle(size=top_bar.size, pos=top_bar.pos, radius=[0])
        top_bar.bind(size=lambda i, v: setattr(top_bar.canvas.before.children[-1], 'size', v))
        top_bar.bind(pos=lambda i, v: setattr(top_bar.canvas.before.children[-1], 'pos', v))
        
        back_btn = Button(
            text='返回',
            size_hint_x=0.2,
            background_color=(0, 0, 0, 0),
            font_name=CHINESE_FONT,
            font_size=Fonts.BUTTON,
            color=Colors.TEXT_PRIMARY
        )
        back_btn.bind(on_press=self.go_back)
        title = Label(
            text='宠物种类管理',
            font_size=Fonts.SUBTITLE,
            color=Colors.TEXT_WHITE,
            font_name=CHINESE_FONT,
            bold=True,
            size_hint_x=0.6
        )
        top_bar.add_widget(back_btn)
        top_bar.add_widget(title)
        top_bar.add_widget(Label(size_hint_x=0.2))
        self.main_layout.add_widget(top_bar)
        
        # 内容区域 - 使用浅色背景
        self.content_layout = BoxLayout(orientation='vertical', size_hint_y=1, padding=dp(Sizes.PADDING_MEDIUM), spacing=dp(Sizes.PADDING_SMALL))
        with self.content_layout.canvas.before:
            Color(*Colors.BG_LIGHT)
            RoundedRectangle(size=self.content_layout.size, pos=self.content_layout.pos, radius=[0])
        self.content_layout.bind(size=lambda i, v: setattr(self.content_layout.canvas.before.children[-1], 'size', v))
        self.content_layout.bind(pos=lambda i, v: setattr(self.content_layout.canvas.before.children[-1], 'pos', v))
        self.main_layout.add_widget(self.content_layout)
        
        self.add_widget(self.main_layout)
    
    def on_enter(self):
        self.show_types_list()
    
    def show_types_list(self):
        self.content_layout.clear_widgets()
        
        scroll = ScrollView()
        main_content = BoxLayout(orientation='vertical', spacing=dp(Sizes.PADDING_MEDIUM), size_hint_y=None, padding=dp(Sizes.PADDING_SMALL))
        main_content.bind(minimum_height=main_content.setter('height'))
        
        # 添加卡片 - 使用白色背景和圆角
        add_card = BoxLayout(orientation='vertical', padding=dp(Sizes.PADDING_LARGE), spacing=dp(Sizes.PADDING_MEDIUM), size_hint_y=None, height=dp(200))
        with add_card.canvas.before:
            Color(*Colors.BG_WHITE)
            RoundedRectangle(size=add_card.size, pos=add_card.pos, radius=[dp(Sizes.RADIUS_MEDIUM)])
        add_card.bind(size=lambda i, v: setattr(add_card.canvas.before.children[-1], 'size', v))
        add_card.bind(pos=lambda i, v: setattr(add_card.canvas.before.children[-1], 'pos', v))
        
        add_card.add_widget(Label(
            text='添加新种类',
            font_size=Fonts.SUBTITLE,
            bold=True,
            font_name=CHINESE_FONT,
            color=Colors.TEXT_PRIMARY
        ))
        
        name_row = BoxLayout(spacing=dp(Sizes.PADDING_SMALL), size_hint_y=None, height=dp(Sizes.INPUT_HEIGHT))
        name_label = Label(
            text='种类名称',
            font_size=Fonts.BODY,
            size_hint_x=0.25,
            halign='right',
            font_name=CHINESE_FONT,
            color=Colors.TEXT_SECONDARY
        )
        name_label.bind(size=name_label.setter('text_size'))
        self.name_input = TextInput(
            hint_text='请输入种类名称',
            size_hint_x=0.75,
            font_name=CHINESE_FONT,
            font_size=Fonts.BODY,
            multiline=False,
            background_color=Colors.BG_GRAY,
            foreground_color=Colors.TEXT_PRIMARY,
            hint_text_color=Colors.TEXT_HINT
        )
        name_row.add_widget(name_label)
        name_row.add_widget(self.name_input)
        add_card.add_widget(name_row)
        
        desc_row = BoxLayout(spacing=dp(Sizes.PADDING_SMALL), size_hint_y=None, height=dp(Sizes.INPUT_HEIGHT))
        desc_label = Label(
            text='描述',
            font_size=Fonts.BODY,
            size_hint_x=0.25,
            halign='right',
            font_name=CHINESE_FONT,
            color=Colors.TEXT_SECONDARY
        )
        desc_label.bind(size=desc_label.setter('text_size'))
        self.desc_input = TextInput(
            hint_text='请输入描述（可选）',
            size_hint_x=0.75,
            font_name=CHINESE_FONT,
            font_size=Fonts.BODY,
            multiline=False,
            background_color=Colors.BG_GRAY,
            foreground_color=Colors.TEXT_PRIMARY,
            hint_text_color=Colors.TEXT_HINT
        )
        desc_row.add_widget(desc_label)
        desc_row.add_widget(self.desc_input)
        add_card.add_widget(desc_row)
        
        add_btn = Button(
            text='添加种类',
            size_hint_y=None,
            height=dp(Sizes.BUTTON_HEIGHT),
            background_color=Colors.SUCCESS,
            font_name=CHINESE_FONT,
            font_size=Fonts.BUTTON,
            color=Colors.TEXT_WHITE
        )
        add_btn.bind(on_press=self.add_type)
        add_card.add_widget(add_btn)
        
        main_content.add_widget(add_card)
        
        main_content.add_widget(Label(
            text='现有种类',
            font_size=Fonts.SUBTITLE,
            bold=True,
            font_name=CHINESE_FONT,
            color=Colors.TEXT_PRIMARY,
            size_hint_y=None,
            height=dp(40)
        ))
        
        types = PetDatabase.get_all_pet_types()
        
        if not types:
            main_content.add_widget(Label(
                text='暂无种类',
                font_size=Fonts.BODY_SMALL,
                color=Colors.TEXT_HINT,
                font_name=CHINESE_FONT,
                size_hint_y=None,
                height=dp(40)
            ))
        else:
            types_grid = GridLayout(cols=1, spacing=dp(Sizes.PADDING_SMALL), size_hint_y=None, row_default_height=dp(Sizes.CARD_HEIGHT))
            types_grid.bind(minimum_height=types_grid.setter('height'))
            
            for pet_type in types:
                type_id, name, description = pet_type[0], pet_type[1], pet_type[2]
                
                # 种类卡片 - 使用白色背景和圆角
                card = BoxLayout(orientation='horizontal', padding=dp(Sizes.PADDING_MEDIUM), spacing=dp(Sizes.PADDING_MEDIUM), size_hint_y=None, height=dp(Sizes.CARD_HEIGHT))
                with card.canvas.before:
                    Color(*Colors.BG_WHITE)
                    RoundedRectangle(size=card.size, pos=card.pos, radius=[dp(Sizes.RADIUS_SMALL)])
                card.bind(size=lambda i, v: setattr(card.canvas.before.children[-1], 'size', v))
                card.bind(pos=lambda i, v: setattr(card.canvas.before.children[-1], 'pos', v))
                
                info_layout = BoxLayout(orientation='vertical', size_hint_x=0.7)
                info_layout.add_widget(Label(
                    text=name,
                    font_size=Fonts.BODY,
                    bold=True,
                    font_name=CHINESE_FONT,
                    color=Colors.TEXT_PRIMARY
                ))
                if description:
                    info_layout.add_widget(Label(
                        text=description,
                        font_size=Fonts.BODY_SMALL,
                        color=Colors.TEXT_SECONDARY,
                        font_name=CHINESE_FONT
                    ))
                
                delete_btn = Button(
                    text='删除',
                    size_hint_x=0.2,
                    background_color=Colors.DANGER,
                    font_name=CHINESE_FONT,
                    font_size=Fonts.BODY_SMALL,
                    color=Colors.TEXT_WHITE
                )
                delete_btn.bind(on_press=lambda x, tid=type_id: self.delete_type(tid))
                
                card.add_widget(info_layout)
                card.add_widget(delete_btn)
                
                types_grid.add_widget(card)
            
            main_content.add_widget(types_grid)
        
        scroll.add_widget(main_content)
        self.content_layout.add_widget(scroll)
    
    def add_type(self, instance):
        name = self.name_input.text.strip()
        description = self.desc_input.text.strip()
        
        if not name:
            self.show_error('请输入种类名称')
            return
        
        success = PetDatabase.add_pet_type(name, description)
        
        if success:
            self.name_input.text = ''
            self.desc_input.text = ''
            self.show_types_list()
        else:
            self.show_error('该种类已存在')
    
    def delete_type(self, type_id):
        confirm_popup = Popup(
            title='确认删除',
            content=BoxLayout(orientation='vertical', spacing=dp(Sizes.PADDING_SMALL), padding=dp(Sizes.PADDING_MEDIUM)),
            size_hint=(0.5, 0.3),
            title_font=CHINESE_FONT,
            title_color=Colors.TEXT_PRIMARY,
            separator_color=Colors.PRIMARY
        )
        
        confirm_popup.content.add_widget(Label(
            text='确定要删除这个种类吗？',
            font_name=CHINESE_FONT,
            font_size=Fonts.BODY,
            color=Colors.TEXT_PRIMARY
        ))
        
        btn_layout = BoxLayout(spacing=dp(Sizes.PADDING_SMALL))
        cancel_btn = Button(
            text='取消',
            background_color=Colors.GRAY,
            font_name=CHINESE_FONT,
            font_size=Fonts.BUTTON,
            color=Colors.TEXT_WHITE
        )
        cancel_btn.bind(on_press=lambda x: confirm_popup.dismiss())
        
        delete_btn = Button(
            text='删除',
            background_color=Colors.DANGER,
            font_name=CHINESE_FONT,
            font_size=Fonts.BUTTON,
            color=Colors.TEXT_WHITE
        )
        delete_btn.bind(on_press=lambda x: self.confirm_delete(type_id, confirm_popup))
        
        btn_layout.add_widget(cancel_btn)
        btn_layout.add_widget(delete_btn)
        confirm_popup.content.add_widget(btn_layout)
        
        confirm_popup.open()
    
    def confirm_delete(self, type_id, popup):
        PetDatabase.delete_pet_type(type_id)
        popup.dismiss()
        self.show_types_list()
    
    def show_error(self, message):
        popup = Popup(
            title='错误',
            content=Label(text=message, font_name=CHINESE_FONT, font_size=Fonts.BODY, color=Colors.TEXT_PRIMARY),
            size_hint=(0.6, 0.3),
            title_font=CHINESE_FONT,
            title_color=Colors.DANGER,
            separator_color=Colors.DANGER
        )
        popup.open()
    
    def go_back(self, instance):
        self.manager.current = 'main'