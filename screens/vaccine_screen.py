"""
疫苗记录界面
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

class VaccineScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pet_id = None
        self.setup_ui()
    
    def setup_ui(self):
        self.main_layout = BoxLayout(orientation='vertical', padding=0, spacing=0)
        
        # 顶部标题栏 - 使用 PRIMARY 颜色
        top_bar = BoxLayout(size_hint_y=None, height=dp(Sizes.TITLE_BAR_HEIGHT), padding=dp(Sizes.PADDING_MEDIUM), spacing=dp(Sizes.PADDING_SMALL))
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
            text='疫苗记录',
            font_size=Fonts.TITLE,
            color=Colors.TEXT_WHITE,
            font_name=CHINESE_FONT,
            bold=True
        )
        top_bar.add_widget(back_btn)
        top_bar.add_widget(title)
        top_bar.add_widget(Label(size_hint_x=0.18))
        self.main_layout.add_widget(top_bar)
        
        self.content_layout = BoxLayout(orientation='vertical', size_hint_y=0.9, padding=dp(Sizes.PADDING_MEDIUM), spacing=dp(Sizes.PADDING_SMALL))
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
            self.show_vaccine_form()
        else:
            self.show_pet_selection()
    
    def show_pet_selection(self):
        layout = BoxLayout(orientation='vertical', padding=dp(Sizes.PADDING_MEDIUM), spacing=dp(Sizes.PADDING_MEDIUM))
        
        layout.add_widget(Label(
            text='请选择宠物',
            font_size=Fonts.SUBTITLE,
            font_name=CHINESE_FONT,
            bold=True,
            color=Colors.TEXT_PRIMARY,
            size_hint_y=None,
            height=dp(Sizes.BUTTON_HEIGHT)
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
        self.show_vaccine_form()
    
    def show_vaccine_form(self):
        self.content_layout.clear_widgets()
        
        pet = PetDatabase.get_pet_by_id(self.pet_id)
        pet_name = pet[1] if pet else '未知宠物'
        
        scroll = ScrollView()
        main_content = BoxLayout(orientation='vertical', spacing=dp(Sizes.PADDING_MEDIUM), size_hint_y=None, padding=dp(Sizes.PADDING_SMALL))
        main_content.bind(minimum_height=main_content.setter('height'))
        
        # 宠物信息卡片 - 使用 BG_GRAY 背景色
        pet_info_card = BoxLayout(orientation='horizontal', padding=dp(Sizes.PADDING_MEDIUM), size_hint_y=None, height=dp(Sizes.CARD_HEIGHT))
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
        
        # 表单卡片 - 使用 BG_WHITE 背景色
        form_card = BoxLayout(orientation='vertical', padding=dp(Sizes.PADDING_LARGE), spacing=dp(Sizes.PADDING_MEDIUM), size_hint_y=None, height=dp(400))
        with form_card.canvas.before:
            Color(*Colors.BG_WHITE)
            RoundedRectangle(size=form_card.size, pos=form_card.pos, radius=[dp(Sizes.RADIUS_MEDIUM)])
        form_card.bind(size=lambda i, v: setattr(form_card.canvas.before.children[-1], 'size', v))
        form_card.bind(pos=lambda i, v: setattr(form_card.canvas.before.children[-1], 'pos', v))
        
        form_card.add_widget(Label(
            text='添加疫苗记录',
            font_size=Fonts.SUBTITLE,
            bold=True,
            font_name=CHINESE_FONT,
            color=Colors.TEXT_PRIMARY,
            size_hint_y=None,
            height=dp(40)
        ))
        
        vaccine_row = BoxLayout(spacing=dp(Sizes.PADDING_SMALL), size_hint_y=None, height=dp(Sizes.INPUT_HEIGHT))
        vaccine_label = Label(
            text='疫苗类型',
            font_size=Fonts.BODY,
            size_hint_x=0.25,
            halign='right',
            font_name=CHINESE_FONT,
            color=Colors.TEXT_SECONDARY
        )
        vaccine_label.bind(size=vaccine_label.setter('text_size'))
        self.vaccine_spinner = Spinner(
            text='选择疫苗',
            values=('狂犬疫苗', '三联疫苗', '四联疫苗', '钩端螺旋体疫苗', '其他'),
            size_hint_x=0.75,
            font_name=CHINESE_FONT,
            font_size=Fonts.BODY,
            option_cls=ChineseSpinnerOption,
            background_color=Colors.BG_GRAY
        )
        vaccine_row.add_widget(vaccine_label)
        vaccine_row.add_widget(self.vaccine_spinner)
        form_card.add_widget(vaccine_row)
        
        date_row = BoxLayout(spacing=dp(Sizes.PADDING_SMALL), size_hint_y=None, height=dp(Sizes.INPUT_HEIGHT))
        date_label = Label(
            text='接种日期',
            font_size=Fonts.BODY,
            size_hint_x=0.25,
            halign='right',
            font_name=CHINESE_FONT,
            color=Colors.TEXT_SECONDARY
        )
        date_label.bind(size=date_label.setter('text_size'))
        self.date_input = TextInput(
            hint_text='YYYY-MM-DD',
            size_hint_x=0.75,
            font_name=CHINESE_FONT,
            font_size=Fonts.BODY,
            multiline=False,
            background_color=Colors.BG_GRAY,
            foreground_color=Colors.TEXT_PRIMARY,
            hint_text_color=Colors.TEXT_HINT
        )
        date_row.add_widget(date_label)
        date_row.add_widget(self.date_input)
        form_card.add_widget(date_row)
        
        period_row = BoxLayout(spacing=dp(Sizes.PADDING_SMALL), size_hint_y=None, height=dp(Sizes.INPUT_HEIGHT))
        period_label = Label(
            text='下次提醒',
            font_size=Fonts.BODY,
            size_hint_x=0.25,
            halign='right',
            font_name=CHINESE_FONT,
            color=Colors.TEXT_SECONDARY
        )
        period_label.bind(size=period_label.setter('text_size'))
        self.period_spinner = Spinner(
            text='选择周期',
            values=('1年', '2年', '3年', '无需提醒'),
            size_hint_x=0.75,
            font_name=CHINESE_FONT,
            font_size=Fonts.BODY,
            option_cls=ChineseSpinnerOption,
            background_color=Colors.BG_GRAY
        )
        period_row.add_widget(period_label)
        period_row.add_widget(self.period_spinner)
        form_card.add_widget(period_row)
        
        # 添加按钮 - 使用 SUCCESS 颜色
        add_btn = Button(
            text='添加记录',
            size_hint_y=None,
            height=dp(Sizes.BUTTON_HEIGHT),
            background_color=Colors.SUCCESS,
            font_name=CHINESE_FONT,
            font_size=Fonts.BUTTON,
            color=Colors.TEXT_WHITE
        )
        add_btn.bind(on_press=self.save_vaccine)
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
        vaccines = PetDatabase.get_vaccines(self.pet_id)
        
        if not vaccines:
            parent_layout.add_widget(Label(
                text='暂无疫苗记录',
                font_size=Fonts.BODY_SMALL,
                color=Colors.TEXT_HINT,
                font_name=CHINESE_FONT,
                size_hint_y=None,
                height=dp(Sizes.CARD_HEIGHT)
            ))
            return
        
        history_grid = GridLayout(cols=1, spacing=dp(Sizes.PADDING_SMALL), size_hint_y=None, row_default_height=dp(100))
        history_grid.bind(minimum_height=history_grid.setter('height'))
        
        for vac in vaccines:
            # 历史记录卡片 - 使用 BG_WHITE 背景色
            card = BoxLayout(orientation='vertical', padding=dp(Sizes.PADDING_MEDIUM), size_hint_y=None, height=dp(100))
            with card.canvas.before:
                Color(*Colors.BG_WHITE)
                RoundedRectangle(size=card.size, pos=card.pos, radius=[dp(Sizes.RADIUS_SMALL)])
            card.bind(size=lambda i, v: setattr(card.canvas.before.children[-1], 'size', v))
            card.bind(pos=lambda i, v: setattr(card.canvas.before.children[-1], 'pos', v))
            
            card.add_widget(Label(
                text=vac[1],
                font_size=Fonts.BODY,
                bold=True,
                font_name=CHINESE_FONT,
                color=Colors.TEXT_PRIMARY,
                size_hint_y=None,
                height=dp(30)
            ))
            card.add_widget(Label(
                text=f'接种日期：{vac[2]}',
                font_size=Fonts.BODY_SMALL,
                color=Colors.TEXT_SECONDARY,
                font_name=CHINESE_FONT,
                size_hint_y=None,
                height=dp(25)
            ))
            if vac[3]:
                card.add_widget(Label(
                    text=f'下次提醒：{vac[3]}',
                    font_size=Fonts.BODY_SMALL,
                    color=Colors.TEXT_SECONDARY,
                    font_name=CHINESE_FONT,
                    size_hint_y=None,
                    height=dp(25)
                ))
            
            history_grid.add_widget(card)
        
        parent_layout.add_widget(history_grid)
    
    def save_vaccine(self, instance):
        vaccine_type = self.vaccine_spinner.text
        date = self.date_input.text.strip()
        period = self.period_spinner.text
        
        if vaccine_type == '选择疫苗':
            self.show_error('请选择疫苗类型')
            return
        if not date:
            self.show_error('请输入接种日期')
            return
        
        next_reminder = self.calculate_next_reminder(date, period)
        
        PetDatabase.add_vaccine(self.pet_id, vaccine_type, date, next_reminder)
        
        self.date_input.text = ''
        self.vaccine_spinner.text = '选择疫苗'
        self.period_spinner.text = '选择周期'
        
        self.show_vaccine_form()
    
    def calculate_next_reminder(self, date_str, period):
        if period == '无需提醒':
            return None
        
        import re
        match = re.search(r'(\d+)年', period)
        if match:
            years = int(match.group(1))
            parts = date_str.split('-')
            if len(parts) == 3:
                year = int(parts[0]) + years
                return f'{year}-{parts[1]}-{parts[2]}'
        return None
    
    def show_error(self, message):
        content = BoxLayout(orientation='vertical', padding=dp(Sizes.PADDING_MEDIUM))
        content.add_widget(Label(
            text=message,
            font_name=CHINESE_FONT,
            font_size=Fonts.BODY,
            color=Colors.TEXT_PRIMARY
        ))
        
        popup = Popup(
            title='错误',
            content=content,
            size_hint=(0.6, 0.3),
            title_font=CHINESE_FONT,
            title_color=Colors.TEXT_WHITE,
            separator_color=Colors.DANGER
        )
        popup.open()
    
    def go_back(self, instance):
        self.manager.current = 'main'