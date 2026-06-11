"""
宠物详情界面
"""

from kivy.core.text import LabelBase
CHINESE_FONT = 'Chinese'

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.metrics import dp
from kivy.graphics import Color, RoundedRectangle

from database.pet_db import PetDatabase
from utils.styles import Colors, Fonts, Sizes

class PetDetailScreen(Screen):
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
        self.title_bar = BoxLayout(size_hint_y=None, height=dp(60), padding=[dp(15), dp(5), dp(15), dp(5)])
        with self.title_bar.canvas.before:
            Color(*Colors.PRIMARY)
            self.title_rect = RoundedRectangle(size=self.title_bar.size, pos=self.title_bar.pos)
        self.title_bar.bind(size=self._update_title_rect, pos=self._update_title_rect)
        
        self.back_btn = Button(
            text='← 返回',
            size_hint_x=0.2,
            background_color=(0, 0, 0, 0),
            font_name=CHINESE_FONT,
            font_size=Fonts.BODY,
            color=Colors.TEXT_PRIMARY
        )
        self.back_btn.bind(on_press=self.go_back)
        self.title = Label(
            text='宠物详情',
            font_size=Fonts.SUBTITLE,
            bold=True,
            color=Colors.TEXT_WHITE,
            font_name=CHINESE_FONT,
            size_hint_x=0.6
        )
        self.title_bar.add_widget(self.back_btn)
        self.title_bar.add_widget(self.title)
        self.title_bar.add_widget(Label(size_hint_x=0.2))
        self.main_layout.add_widget(self.title_bar)
        
        self.content_layout = BoxLayout(orientation='vertical', size_hint_y=0.9, padding=dp(15))
        self.main_layout.add_widget(self.content_layout)
        
        self.add_widget(self.main_layout)
    
    def _update_bg(self, instance, value):
        self.bg_rect.size = value
    
    def _update_title_rect(self, instance, value):
        self.title_rect.size = value
    
    def on_enter(self):
        if hasattr(self.manager, 'pet_id') and self.manager.pet_id:
            self.pet_id = self.manager.pet_id
            self.show_detail()
        else:
            self.manager.current = 'main'
    
    def show_detail(self):
        self.content_layout.clear_widgets()
        
        pet = PetDatabase.get_pet_by_id(self.pet_id)
        if not pet:
            self.manager.current = 'main'
            return
        
        name, pet_type, breed, birthday, gender = pet[1], pet[2], pet[3], pet[4], pet[5]
        self.title.text = name
        
        scroll = ScrollView()
        content = BoxLayout(orientation='vertical', spacing=dp(15), size_hint_y=None, padding=[dp(5), dp(5), dp(5), dp(5)])
        content.bind(minimum_height=content.setter('height'))
        
        # 基本信息卡片
        info_card = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15), size_hint_y=None, height=dp(200))
        with info_card.canvas.before:
            Color(*Colors.BG_WHITE)
            RoundedRectangle(size=info_card.size, pos=info_card.pos, radius=[dp(Sizes.RADIUS_MEDIUM)])
        info_card.bind(
            size=lambda i, v: setattr(i.canvas.before.children[-1], 'size', v),
            pos=lambda i, v: setattr(i.canvas.before.children[-1], 'pos', v)
        )
        
        # 头部：图标和名称
        header = BoxLayout(orientation='horizontal', spacing=dp(15))
        icon_bg = BoxLayout(size_hint_x=None, width=dp(60), size_hint_y=None, height=dp(60))
        with icon_bg.canvas.before:
            Color(*Colors.CAT_COLOR if pet_type == 'cat' else Colors.DOG_COLOR)
            RoundedRectangle(size=icon_bg.size, pos=icon_bg.pos, radius=[dp(30)])
        icon_bg.bind(
            size=lambda i, v: setattr(i.canvas.before.children[-1], 'size', v),
            pos=lambda i, v: setattr(i.canvas.before.children[-1], 'pos', v)
        )
        icon_bg.add_widget(Label(
            text='🐱' if pet_type == 'cat' else '🐶',
            font_size='28sp'
        ))
        header.add_widget(icon_bg)
        
        name_info = BoxLayout(orientation='vertical', spacing=dp(5))
        name_info.add_widget(Label(
            text=name,
            font_size=Fonts.SUBTITLE,
            bold=True,
            color=Colors.TEXT_PRIMARY,
            font_name=CHINESE_FONT,
            halign='left'
        ))
        name_info.children[0].bind(size=name_info.children[0].setter('text_size'))
        type_text = '猫咪' if pet_type == 'cat' else '狗狗'
        name_info.add_widget(Label(
            text=type_text,
            font_size=Fonts.BODY_SMALL,
            color=Colors.TEXT_SECONDARY,
            font_name=CHINESE_FONT,
            halign='left'
        ))
        name_info.children[0].bind(size=name_info.children[0].setter('text_size'))
        header.add_widget(name_info)
        info_card.add_widget(header)
        
        # 详细信息
        details = BoxLayout(orientation='vertical', spacing=dp(8))
        if breed:
            details.add_widget(self._create_info_row('品种', breed))
        if birthday:
            details.add_widget(self._create_info_row('生日', birthday))
        if gender:
            gender_text = '公' if gender == 'male' else '母'
            details.add_widget(self._create_info_row('性别', gender_text))
        info_card.add_widget(details)
        content.add_widget(info_card)
        
        # 功能按钮
        btn_grid = BoxLayout(orientation='vertical', spacing=dp(12), size_hint_y=None, height=dp(180))
        
        vaccine_btn = self._create_action_button('疫苗记录', Colors.PRIMARY, self.go_vaccine)
        weight_btn = self._create_action_button('体重记录', Colors.SUCCESS, self.go_weight)
        delete_btn = self._create_action_button('删除宠物', Colors.DANGER, self.delete_pet)
        
        btn_grid.add_widget(vaccine_btn)
        btn_grid.add_widget(weight_btn)
        btn_grid.add_widget(delete_btn)
        content.add_widget(btn_grid)
        
        scroll.add_widget(content)
        self.content_layout.add_widget(scroll)
    
    def _create_info_row(self, label, value):
        row = BoxLayout(spacing=dp(10))
        row.add_widget(Label(
            text=f'{label}：',
            font_size=Fonts.BODY_SMALL,
            color=Colors.TEXT_SECONDARY,
            font_name=CHINESE_FONT,
            size_hint_x=0.3,
            halign='right'
        ))
        row.children[0].bind(size=row.children[0].setter('text_size'))
        row.add_widget(Label(
            text=value,
            font_size=Fonts.BODY_SMALL,
            color=Colors.TEXT_PRIMARY,
            font_name=CHINESE_FONT,
            halign='left'
        ))
        row.children[0].bind(size=row.children[0].setter('text_size'))
        return row
    
    def _create_action_button(self, text, color, callback):
        btn = Button(
            text=text,
            size_hint_y=None,
            height=dp(Sizes.BUTTON_HEIGHT),
            background_color=color,
            font_name=CHINESE_FONT,
            font_size=Fonts.BUTTON,
            color=Colors.TEXT_WHITE
        )
        btn.bind(on_press=callback)
        return btn
    
    def go_vaccine(self, instance):
        self.manager.current = 'vaccine'
    
    def go_weight(self, instance):
        self.manager.current = 'weight'
    
    def delete_pet(self, instance):
        content = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        content.add_widget(Label(
            text='确定要删除这只宠物吗？',
            font_name=CHINESE_FONT,
            font_size=Fonts.BODY,
            color=Colors.TEXT_PRIMARY
        ))
        
        btn_row = BoxLayout(spacing=dp(15))
        cancel_btn = Button(
            text='取消',
            background_color=Colors.GRAY,
            font_name=CHINESE_FONT,
            color=Colors.TEXT_WHITE
        )
        cancel_btn.bind(on_press=lambda x: self._popup.dismiss())
        
        confirm_btn = Button(
            text='删除',
            background_color=Colors.DANGER,
            font_name=CHINESE_FONT,
            color=Colors.TEXT_WHITE
        )
        confirm_btn.bind(on_press=self.confirm_delete)
        
        btn_row.add_widget(cancel_btn)
        btn_row.add_widget(confirm_btn)
        content.add_widget(btn_row)
        
        self._popup = Popup(
            title='确认删除',
            content=content,
            size_hint=(0.6, 0.35),
            title_font=CHINESE_FONT,
            background_color=Colors.BG_WHITE
        )
        self._popup.open()
    
    def confirm_delete(self, instance):
        PetDatabase.delete_pet(self.pet_id)
        self._popup.dismiss()
        self.manager.current = 'pet_list'
    
    def go_back(self, instance):
        self.manager.current = 'pet_list'