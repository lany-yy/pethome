"""
添加宠物界面
"""

from kivy.core.text import LabelBase
CHINESE_FONT = 'Chinese'

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner, SpinnerOption
from kivy.uix.popup import Popup
from kivy.metrics import dp
from kivy.graphics import Color, RoundedRectangle

from database.pet_db import PetDatabase
from utils.styles import Colors, Fonts, Sizes

class ChineseSpinnerOption(SpinnerOption):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_name = CHINESE_FONT

class AddPetScreen(Screen):
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
            text='添加宠物',
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
        
        # 表单区域
        scroll = ScrollView()
        form = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15), size_hint_y=None)
        form.bind(minimum_height=form.setter('height'))
        
        # 表单卡片
        form_card = BoxLayout(orientation='vertical', padding=dp(25), spacing=dp(20), size_hint_y=None, height=dp(450))
        with form_card.canvas.before:
            Color(*Colors.BG_WHITE)
            RoundedRectangle(size=form_card.size, pos=form_card.pos, radius=[dp(Sizes.RADIUS_MEDIUM)])
        form_card.bind(
            size=lambda i, v: setattr(i.canvas.before.children[-1], 'size', v),
            pos=lambda i, v: setattr(i.canvas.before.children[-1], 'pos', v)
        )
        
        # 宠物名称
        name_row = self._create_input_row('宠物名称', '请输入宠物名称')
        self.name_input = name_row.children[0]
        form_card.add_widget(name_row)
        
        # 宠物类型
        type_row = BoxLayout(spacing=dp(15), size_hint_y=None, height=dp(Sizes.INPUT_HEIGHT))
        type_label = Label(
            text='宠物类型',
            font_size=Fonts.BODY,
            size_hint_x=0.25,
            halign='right',
            color=Colors.TEXT_SECONDARY,
            font_name=CHINESE_FONT
        )
        type_label.bind(size=type_label.setter('text_size'))
        self.type_spinner = Spinner(
            text='请选择',
            values=('猫咪', '狗狗'),
            size_hint_x=0.75,
            font_name=CHINESE_FONT,
            font_size=Fonts.BODY,
            option_cls=ChineseSpinnerOption,
            background_color=Colors.BG_GRAY,
            color=Colors.TEXT_PRIMARY
        )
        type_row.add_widget(type_label)
        type_row.add_widget(self.type_spinner)
        form_card.add_widget(type_row)
        
        # 品种
        breed_row = self._create_input_row('品种', '请输入品种（可选）')
        self.breed_input = breed_row.children[0]
        form_card.add_widget(breed_row)
        
        # 生日
        birthday_row = self._create_input_row('生日', 'YYYY-MM-DD（可选）')
        self.birthday_input = birthday_row.children[0]
        form_card.add_widget(birthday_row)
        
        # 性别
        gender_row = BoxLayout(spacing=dp(15), size_hint_y=None, height=dp(Sizes.INPUT_HEIGHT))
        gender_label = Label(
            text='性别',
            font_size=Fonts.BODY,
            size_hint_x=0.25,
            halign='right',
            color=Colors.TEXT_SECONDARY,
            font_name=CHINESE_FONT
        )
        gender_label.bind(size=gender_label.setter('text_size'))
        self.gender_spinner = Spinner(
            text='请选择',
            values=('公', '母'),
            size_hint_x=0.75,
            font_name=CHINESE_FONT,
            font_size=Fonts.BODY,
            option_cls=ChineseSpinnerOption,
            background_color=Colors.BG_GRAY,
            color=Colors.TEXT_PRIMARY
        )
        gender_row.add_widget(gender_label)
        gender_row.add_widget(self.gender_spinner)
        form_card.add_widget(gender_row)
        
        form.add_widget(form_card)
        
        # 提交按钮
        submit_btn = Button(
            text='添加宠物',
            size_hint_y=None,
            height=dp(Sizes.BUTTON_HEIGHT),
            background_color=Colors.SUCCESS,
            font_name=CHINESE_FONT,
            font_size=Fonts.BUTTON,
            color=Colors.TEXT_WHITE
        )
        submit_btn.bind(on_press=self.add_pet)
        form.add_widget(submit_btn)
        
        scroll.add_widget(form)
        self.main_layout.add_widget(scroll)
        self.add_widget(self.main_layout)
    
    def _update_bg(self, instance, value):
        self.bg_rect.size = value
    
    def _update_title_rect(self, instance, value):
        self.title_rect.size = value
    
    def _create_input_row(self, label_text, hint_text):
        row = BoxLayout(spacing=dp(15), size_hint_y=None, height=dp(Sizes.INPUT_HEIGHT))
        label = Label(
            text=label_text,
            font_size=Fonts.BODY,
            size_hint_x=0.25,
            halign='right',
            color=Colors.TEXT_SECONDARY,
            font_name=CHINESE_FONT
        )
        label.bind(size=label.setter('text_size'))
        input_field = TextInput(
            hint_text=hint_text,
            size_hint_x=0.75,
            font_name=CHINESE_FONT,
            font_size=Fonts.BODY,
            multiline=False,
            background_color=Colors.BG_GRAY,
            foreground_color=Colors.TEXT_PRIMARY,
            hint_text_color=Colors.TEXT_HINT,
            padding=[dp(10), dp(10), dp(10), dp(10)]
        )
        row.add_widget(label)
        row.add_widget(input_field)
        return row
    
    def add_pet(self, instance):
        name = self.name_input.text.strip()
        pet_type = self.type_spinner.text
        breed = self.breed_input.text.strip()
        birthday = self.birthday_input.text.strip()
        gender = self.gender_spinner.text
        
        if not name:
            self.show_error('请输入宠物名称')
            return
        if pet_type == '请选择':
            self.show_error('请选择宠物类型')
            return
        
        type_value = 'cat' if pet_type == '猫咪' else 'dog'
        gender_value = 'male' if gender == '公' else 'female' if gender == '母' else None
        
        PetDatabase.add_pet(name, type_value, breed, birthday, gender_value)
        
        self.name_input.text = ''
        self.type_spinner.text = '请选择'
        self.breed_input.text = ''
        self.birthday_input.text = ''
        self.gender_spinner.text = '请选择'
        
        self.show_success()
    
    def show_error(self, message):
        content = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        content.add_widget(Label(
            text=message,
            font_name=CHINESE_FONT,
            font_size=Fonts.BODY,
            color=Colors.DANGER
        ))
        ok_btn = Button(
            text='确定',
            size_hint_y=None,
            height=dp(40),
            background_color=Colors.PRIMARY,
            font_name=CHINESE_FONT,
            color=Colors.TEXT_WHITE
        )
        ok_btn.bind(on_press=lambda x: self._popup.dismiss())
        content.add_widget(ok_btn)
        
        self._popup = Popup(
            title='提示',
            content=content,
            size_hint=(0.6, 0.3),
            title_font=CHINESE_FONT,
            background_color=Colors.BG_WHITE
        )
        self._popup.open()
    
    def show_success(self):
        content = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        content.add_widget(Label(
            text='添加成功！',
            font_name=CHINESE_FONT,
            font_size=Fonts.BODY,
            color=Colors.SUCCESS
        ))
        ok_btn = Button(
            text='确定',
            size_hint_y=None,
            height=dp(40),
            background_color=Colors.PRIMARY,
            font_name=CHINESE_FONT,
            color=Colors.TEXT_WHITE
        )
        ok_btn.bind(on_press=lambda x: self._popup.dismiss())
        content.add_widget(ok_btn)
        
        self._popup = Popup(
            title='成功',
            content=content,
            size_hint=(0.6, 0.3),
            title_font=CHINESE_FONT,
            background_color=Colors.BG_WHITE
        )
        self._popup.open()
    
    def go_back(self, instance):
        self.manager.current = 'main'