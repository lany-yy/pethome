"""
今日提醒界面
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
from datetime import date
from kivy.graphics import Color, RoundedRectangle

from database.pet_db import PetDatabase
from utils.styles import Colors, Fonts, Sizes

class ChineseSpinnerOption(SpinnerOption):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_name = CHINESE_FONT

class ReminderScreen(Screen):
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
            text='今日提醒',
            font_size=Fonts.SUBTITLE,
            bold=True,
            color=Colors.TEXT_WHITE,
            font_name=CHINESE_FONT,
            size_hint_x=0.6
        )
        add_btn = Button(
            text='添加提醒',
            size_hint_x=0.2,
            background_color=(0, 0, 0, 0),
            font_name=CHINESE_FONT,
            font_size=Fonts.BODY,
            color=Colors.TEXT_PRIMARY
        )
        add_btn.bind(on_press=self.show_add_reminder_popup)
        title_bar.add_widget(back_btn)
        title_bar.add_widget(title)
        title_bar.add_widget(add_btn)
        self.main_layout.add_widget(title_bar)
        
        self.content_layout = BoxLayout(orientation='vertical', size_hint_y=0.9, padding=dp(15))
        self.main_layout.add_widget(self.content_layout)
        
        self.add_widget(self.main_layout)
    
    def _update_bg(self, instance, value):
        self.bg_rect.size = value
    
    def _update_title_rect(self, instance, value):
        self.title_rect.size = value
    
    def on_enter(self):
        self.load_reminders()
    
    def load_reminders(self):
        self.content_layout.clear_widgets()
        
        reminders = PetDatabase.get_all_reminders()
        
        if not reminders:
            empty_card = BoxLayout(orientation='vertical', padding=dp(30), spacing=dp(15), size_hint_y=None, height=dp(150))
            with empty_card.canvas.before:
                Color(*Colors.BG_WHITE)
                RoundedRectangle(size=empty_card.size, pos=empty_card.pos, radius=[dp(Sizes.RADIUS_MEDIUM)])
            empty_card.bind(
                size=lambda i, v: setattr(i.canvas.before.children[-1], 'size', v),
                pos=lambda i, v: setattr(i.canvas.before.children[-1], 'pos', v)
            )
            
            empty_card.add_widget(Label(
                text='今日没有待办事项',
                font_size=Fonts.BODY,
                color=Colors.TEXT_SECONDARY,
                font_name=CHINESE_FONT
            ))
            empty_card.add_widget(Label(
                text='所有毛孩子都健健康康的！',
                font_size=Fonts.BODY_SMALL,
                color=Colors.TEXT_HINT,
                font_name=CHINESE_FONT
            ))
            self.content_layout.add_widget(empty_card)
        else:
            scroll = ScrollView()
            grid = GridLayout(cols=1, spacing=dp(12), size_hint_y=None)
            grid.bind(minimum_height=grid.setter('height'))
            
            for reminder in reminders:
                reminder_id, pet_id, title, due_date, reminder_type, is_completed, created_at = reminder
                
                pets = PetDatabase.get_all_pets()
                pet_name = '未知宠物'
                for pet in pets:
                    if pet[0] == pet_id:
                        pet_name = pet[1]
                        break
                
                card = BoxLayout(orientation='horizontal', padding=dp(15), spacing=dp(15), size_hint_y=None, height=dp(80))
                with card.canvas.before:
                    bg_color = Colors.BG_GRAY if is_completed else Colors.BG_WHITE
                    Color(*bg_color)
                    RoundedRectangle(size=card.size, pos=card.pos, radius=[dp(Sizes.RADIUS_MEDIUM)])
                card.bind(
                    size=lambda i, v: setattr(i.canvas.before.children[-1], 'size', v),
                    pos=lambda i, v: setattr(i.canvas.before.children[-1], 'pos', v)
                )
                
                info_layout = BoxLayout(orientation='vertical', spacing=dp(5), size_hint_x=0.7)
                info_layout.add_widget(Label(
                    text=title,
                    font_size=Fonts.BODY,
                    bold=True,
                    color=Colors.TEXT_PRIMARY if not is_completed else Colors.TEXT_HINT,
                    font_name=CHINESE_FONT,
                    markup=True
                ))
                info_layout.add_widget(Label(
                    text=f'宠物：{pet_name} | 日期：{due_date}',
                    font_size=Fonts.BODY_SMALL,
                    color=Colors.TEXT_SECONDARY,
                    font_name=CHINESE_FONT
                ))
                
                delete_btn = Button(
                    text='删除',
                    size_hint_x=0.18,
                    background_color=Colors.DANGER,
                    font_name=CHINESE_FONT,
                    font_size=Fonts.BODY_SMALL,
                    color=Colors.TEXT_WHITE
                )
                delete_btn.bind(on_press=lambda x, rid=reminder_id: self.delete_reminder(rid))
                
                card.add_widget(info_layout)
                card.add_widget(delete_btn)
                grid.add_widget(card)
            
            scroll.add_widget(grid)
            self.content_layout.add_widget(scroll)
    
    def show_add_reminder_popup(self, instance):
        content = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15), size_hint_y=None, height=dp(350))
        
        content.add_widget(Label(
            text='添加提醒',
            font_size=Fonts.SUBTITLE,
            bold=True,
            color=Colors.TEXT_PRIMARY,
            font_name=CHINESE_FONT
        ))
        
        pets = PetDatabase.get_all_pets()
        pet_names = [pet[1] for pet in pets]
        
        pet_row = BoxLayout(spacing=dp(10), size_hint_y=None, height=dp(Sizes.INPUT_HEIGHT))
        pet_row.add_widget(Label(
            text='选择宠物',
            font_size=Fonts.BODY,
            size_hint_x=0.25,
            halign='right',
            color=Colors.TEXT_SECONDARY,
            font_name=CHINESE_FONT
        ))
        self.pet_spinner = Spinner(
            text='请选择宠物' if pet_names else '暂无宠物',
            values=pet_names if pet_names else [],
            size_hint_x=0.75,
            font_name=CHINESE_FONT,
            font_size=Fonts.BODY,
            option_cls=ChineseSpinnerOption,
            background_color=Colors.BG_GRAY
        )
        pet_row.add_widget(self.pet_spinner)
        content.add_widget(pet_row)
        
        title_row = BoxLayout(spacing=dp(10), size_hint_y=None, height=dp(Sizes.INPUT_HEIGHT))
        title_row.add_widget(Label(
            text='提醒标题',
            font_size=Fonts.BODY,
            size_hint_x=0.25,
            halign='right',
            color=Colors.TEXT_SECONDARY,
            font_name=CHINESE_FONT
        ))
        self.title_input = TextInput(
            hint_text='请输入提醒标题',
            size_hint_x=0.75,
            font_name=CHINESE_FONT,
            font_size=Fonts.BODY,
            background_color=Colors.BG_GRAY
        )
        title_row.add_widget(self.title_input)
        content.add_widget(title_row)
        
        date_row = BoxLayout(spacing=dp(10), size_hint_y=None, height=dp(Sizes.INPUT_HEIGHT))
        date_row.add_widget(Label(
            text='提醒日期',
            font_size=Fonts.BODY,
            size_hint_x=0.25,
            halign='right',
            color=Colors.TEXT_SECONDARY,
            font_name=CHINESE_FONT
        ))
        self.date_input = TextInput(
            hint_text=f'{date.today().isoformat()}',
            size_hint_x=0.75,
            font_name=CHINESE_FONT,
            font_size=Fonts.BODY,
            background_color=Colors.BG_GRAY
        )
        date_row.add_widget(self.date_input)
        content.add_widget(date_row)
        
        btn_row = BoxLayout(spacing=dp(15))
        cancel_btn = Button(
            text='取消',
            background_color=Colors.GRAY,
            font_name=CHINESE_FONT,
            font_size=Fonts.BUTTON,
            color=Colors.TEXT_WHITE
        )
        cancel_btn.bind(on_press=lambda x: self._popup.dismiss())
        
        save_btn = Button(
            text='保存',
            background_color=Colors.SUCCESS,
            font_name=CHINESE_FONT,
            font_size=Fonts.BUTTON,
            color=Colors.TEXT_WHITE
        )
        save_btn.bind(on_press=self.save_reminder)
        
        btn_row.add_widget(cancel_btn)
        btn_row.add_widget(save_btn)
        content.add_widget(btn_row)
        
        self._popup = Popup(
            title='',
            content=content,
            size_hint=(0.7, 0.5),
            auto_dismiss=False
        )
        self._popup.open()
    
    def save_reminder(self, instance):
        pet_name = self.pet_spinner.text
        title = self.title_input.text.strip()
        due_date = self.date_input.text.strip()
        
        if pet_name == '请选择宠物' or not pet_name:
            self.show_error('请选择宠物')
            return
        if not title:
            self.show_error('请输入提醒标题')
            return
        if not due_date:
            due_date = date.today().isoformat()
        
        pets = PetDatabase.get_all_pets()
        pet_id = None
        for pet in pets:
            if pet[1] == pet_name:
                pet_id = pet[0]
                break
        
        if pet_id:
            PetDatabase.add_reminder(pet_id, title, due_date)
            self._popup.dismiss()
            self.load_reminders()
        else:
            self.show_error('未找到该宠物')
    
    def delete_reminder(self, reminder_id):
        confirm_popup = Popup(
            title='确认删除',
            content=BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15)),
            size_hint=(0.5, 0.3)
        )
        
        confirm_popup.content.add_widget(Label(
            text='确定要删除这条提醒吗？',
            font_name=CHINESE_FONT,
            font_size=Fonts.BODY,
            color=Colors.TEXT_PRIMARY
        ))
        
        btn_row = BoxLayout(spacing=dp(15))
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
        delete_btn.bind(on_press=lambda x: self.confirm_delete(reminder_id, confirm_popup))
        
        btn_row.add_widget(cancel_btn)
        btn_row.add_widget(delete_btn)
        confirm_popup.content.add_widget(btn_row)
        
        confirm_popup.open()
    
    def confirm_delete(self, reminder_id, popup):
        PetDatabase.delete_reminder(reminder_id)
        popup.dismiss()
        self.load_reminders()
    
    def show_error(self, message):
        popup = Popup(
            title='提示',
            content=BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15)),
            size_hint=(0.5, 0.3)
        )
        
        popup.content.add_widget(Label(
            text=message,
            font_name=CHINESE_FONT,
            font_size=Fonts.BODY,
            color=Colors.DANGER
        ))
        
        ok_btn = Button(
            text='确定',
            background_color=Colors.PRIMARY,
            font_name=CHINESE_FONT,
            font_size=Fonts.BUTTON,
            color=Colors.TEXT_WHITE
        )
        ok_btn.bind(on_press=lambda x: popup.dismiss())
        popup.content.add_widget(ok_btn)
        
        popup.open()
    
    def go_back(self, instance):
        self.manager.current = 'main'