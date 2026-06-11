"""
寄养管理界面
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

class FosterScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup_ui()
    
    def setup_ui(self):
        self.main_layout = BoxLayout(orientation='vertical', padding=dp(0), spacing=dp(0))
        
        # 顶部标题栏 - 使用 Colors.PRIMARY 背景色
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
            text='寄养管理',
            font_size=Fonts.TITLE,
            color=Colors.TEXT_WHITE,
            font_name=CHINESE_FONT,
            bold=True
        )
        top_bar.add_widget(back_btn)
        top_bar.add_widget(title)
        top_bar.add_widget(Label(size_hint_x=0.18))
        self.main_layout.add_widget(top_bar)
        
        # 内容区域 - 使用 Colors.BG_LIGHT 背景色
        self.content_layout = BoxLayout(orientation='vertical', size_hint_y=0.9, padding=dp(Sizes.PADDING_MEDIUM), spacing=dp(Sizes.PADDING_MEDIUM))
        with self.content_layout.canvas.before:
            Color(*Colors.BG_LIGHT)
            RoundedRectangle(size=self.content_layout.size, pos=self.content_layout.pos, radius=[0])
        self.content_layout.bind(size=lambda i, v: setattr(self.content_layout.canvas.before.children[-1], 'size', v))
        self.content_layout.bind(pos=lambda i, v: setattr(self.content_layout.canvas.before.children[-1], 'pos', v))
        self.main_layout.add_widget(self.content_layout)
        
        self.add_widget(self.main_layout)
    
    def on_enter(self):
        self.show_foster_list()
    
    def show_foster_list(self):
        self.content_layout.clear_widgets()
        
        scroll = ScrollView()
        main_content = BoxLayout(orientation='vertical', spacing=dp(Sizes.PADDING_MEDIUM), size_hint_y=None, padding=dp(Sizes.PADDING_SMALL))
        main_content.bind(minimum_height=main_content.setter('height'))
        
        # 添加寄养卡片 - 使用 Colors.BG_WHITE 背景色
        add_card = BoxLayout(orientation='vertical', padding=dp(Sizes.PADDING_LARGE), spacing=dp(Sizes.PADDING_SMALL), size_hint_y=None, height=dp(420))
        with add_card.canvas.before:
            Color(*Colors.BG_WHITE)
            RoundedRectangle(size=add_card.size, pos=add_card.pos, radius=[dp(Sizes.RADIUS_MEDIUM)])
        add_card.bind(size=lambda i, v: setattr(add_card.canvas.before.children[-1], 'size', v))
        add_card.bind(pos=lambda i, v: setattr(add_card.canvas.before.children[-1], 'pos', v))
        
        add_card.add_widget(Label(
            text='添加寄养记录',
            font_size=Fonts.SUBTITLE,
            bold=True,
            font_name=CHINESE_FONT,
            color=Colors.TEXT_PRIMARY,
            size_hint_y=None,
            height=dp(40)
        ))
        
        pet_row = BoxLayout(spacing=dp(Sizes.PADDING_SMALL), size_hint_y=None, height=dp(Sizes.INPUT_HEIGHT))
        pet_label = Label(
            text='选择宠物',
            font_size=Fonts.BODY,
            size_hint_x=0.25,
            halign='right',
            font_name=CHINESE_FONT,
            color=Colors.TEXT_SECONDARY
        )
        pet_label.bind(size=pet_label.setter('text_size'))
        
        pets = PetDatabase.get_all_pets()
        pet_names = [pet[1] for pet in pets]
        
        self.pet_spinner = Spinner(
            text='选择宠物' if pet_names else '暂无宠物',
            values=pet_names if pet_names else [],
            size_hint_x=0.75,
            font_name=CHINESE_FONT,
            font_size=Fonts.BODY,
            option_cls=ChineseSpinnerOption,
            background_color=Colors.BG_GRAY
        )
        pet_row.add_widget(pet_label)
        pet_row.add_widget(self.pet_spinner)
        add_card.add_widget(pet_row)
        
        start_date_row = BoxLayout(spacing=dp(Sizes.PADDING_SMALL), size_hint_y=None, height=dp(Sizes.INPUT_HEIGHT))
        start_date_label = Label(
            text='寄养开始',
            font_size=Fonts.BODY,
            size_hint_x=0.25,
            halign='right',
            font_name=CHINESE_FONT,
            color=Colors.TEXT_SECONDARY
        )
        start_date_label.bind(size=start_date_label.setter('text_size'))
        self.start_date_input = TextInput(
            hint_text='YYYY-MM-DD',
            size_hint_x=0.75,
            font_name=CHINESE_FONT,
            font_size=Fonts.BODY,
            multiline=False,
            background_color=Colors.BG_GRAY,
            foreground_color=Colors.TEXT_PRIMARY,
            hint_text_color=Colors.TEXT_HINT
        )
        start_date_row.add_widget(start_date_label)
        start_date_row.add_widget(self.start_date_input)
        add_card.add_widget(start_date_row)
        
        end_date_row = BoxLayout(spacing=dp(Sizes.PADDING_SMALL), size_hint_y=None, height=dp(Sizes.INPUT_HEIGHT))
        end_date_label = Label(
            text='寄养结束',
            font_size=Fonts.BODY,
            size_hint_x=0.25,
            halign='right',
            font_name=CHINESE_FONT,
            color=Colors.TEXT_SECONDARY
        )
        end_date_label.bind(size=end_date_label.setter('text_size'))
        self.end_date_input = TextInput(
            hint_text='YYYY-MM-DD（可选）',
            size_hint_x=0.75,
            font_name=CHINESE_FONT,
            font_size=Fonts.BODY,
            multiline=False,
            background_color=Colors.BG_GRAY,
            foreground_color=Colors.TEXT_PRIMARY,
            hint_text_color=Colors.TEXT_HINT
        )
        end_date_row.add_widget(end_date_label)
        end_date_row.add_widget(self.end_date_input)
        add_card.add_widget(end_date_row)
        
        contact_name_row = BoxLayout(spacing=dp(Sizes.PADDING_SMALL), size_hint_y=None, height=dp(Sizes.INPUT_HEIGHT))
        contact_name_label = Label(
            text='联系人',
            font_size=Fonts.BODY,
            size_hint_x=0.25,
            halign='right',
            font_name=CHINESE_FONT,
            color=Colors.TEXT_SECONDARY
        )
        contact_name_label.bind(size=contact_name_label.setter('text_size'))
        self.contact_name_input = TextInput(
            hint_text='请输入联系人姓名',
            size_hint_x=0.75,
            font_name=CHINESE_FONT,
            font_size=Fonts.BODY,
            multiline=False,
            background_color=Colors.BG_GRAY,
            foreground_color=Colors.TEXT_PRIMARY,
            hint_text_color=Colors.TEXT_HINT
        )
        contact_name_row.add_widget(contact_name_label)
        contact_name_row.add_widget(self.contact_name_input)
        add_card.add_widget(contact_name_row)
        
        contact_phone_row = BoxLayout(spacing=dp(Sizes.PADDING_SMALL), size_hint_y=None, height=dp(Sizes.INPUT_HEIGHT))
        contact_phone_label = Label(
            text='联系电话',
            font_size=Fonts.BODY,
            size_hint_x=0.25,
            halign='right',
            font_name=CHINESE_FONT,
            color=Colors.TEXT_SECONDARY
        )
        contact_phone_label.bind(size=contact_phone_label.setter('text_size'))
        self.contact_phone_input = TextInput(
            hint_text='请输入联系电话',
            size_hint_x=0.75,
            font_name=CHINESE_FONT,
            font_size=Fonts.BODY,
            multiline=False,
            background_color=Colors.BG_GRAY,
            foreground_color=Colors.TEXT_PRIMARY,
            hint_text_color=Colors.TEXT_HINT
        )
        contact_phone_row.add_widget(contact_phone_label)
        contact_phone_row.add_widget(self.contact_phone_input)
        add_card.add_widget(contact_phone_row)
        
        contact_addr_row = BoxLayout(spacing=dp(Sizes.PADDING_SMALL), size_hint_y=None, height=dp(Sizes.INPUT_HEIGHT))
        contact_addr_label = Label(
            text='联系地址',
            font_size=Fonts.BODY,
            size_hint_x=0.25,
            halign='right',
            font_name=CHINESE_FONT,
            color=Colors.TEXT_SECONDARY
        )
        contact_addr_label.bind(size=contact_addr_label.setter('text_size'))
        self.contact_addr_input = TextInput(
            hint_text='请输入联系地址（可选）',
            size_hint_x=0.75,
            font_name=CHINESE_FONT,
            font_size=Fonts.BODY,
            multiline=False,
            background_color=Colors.BG_GRAY,
            foreground_color=Colors.TEXT_PRIMARY,
            hint_text_color=Colors.TEXT_HINT
        )
        contact_addr_row.add_widget(contact_addr_label)
        contact_addr_row.add_widget(self.contact_addr_input)
        add_card.add_widget(contact_addr_row)
        
        # 添加按钮 - 使用 Colors.SUCCESS
        add_btn = Button(
            text='添加寄养',
            size_hint_y=None,
            height=dp(Sizes.BUTTON_HEIGHT),
            background_color=Colors.SUCCESS,
            font_name=CHINESE_FONT,
            font_size=Fonts.BUTTON,
            color=Colors.TEXT_WHITE
        )
        add_btn.bind(on_press=self.add_foster)
        add_card.add_widget(add_btn)
        
        main_content.add_widget(add_card)
        
        # 寄养记录标题
        main_content.add_widget(Label(
            text='寄养记录',
            font_size=Fonts.SUBTITLE,
            bold=True,
            font_name=CHINESE_FONT,
            color=Colors.TEXT_PRIMARY,
            size_hint_y=None,
            height=dp(40)
        ))
        
        records = PetDatabase.get_all_foster_records()
        
        if not records:
            main_content.add_widget(Label(
                text='暂无寄养记录',
                font_size=Fonts.BODY_SMALL,
                color=Colors.TEXT_HINT,
                font_name=CHINESE_FONT,
                size_hint_y=None,
                height=dp(50)
            ))
        else:
            records_grid = GridLayout(cols=1, spacing=dp(Sizes.PADDING_SMALL), size_hint_y=None, row_default_height=dp(120))
            records_grid.bind(minimum_height=records_grid.setter('height'))
            
            for record in records:
                record_id, pet_name, start_date, end_date, contact_name, contact_phone, contact_addr, notes, status = record
                
                # 记录卡片 - 使用 Colors.BG_WHITE 背景色
                card = BoxLayout(orientation='vertical', padding=dp(Sizes.PADDING_MEDIUM), spacing=dp(Sizes.PADDING_SMALL), size_hint_y=None, height=dp(120))
                with card.canvas.before:
                    Color(*Colors.BG_WHITE)
                    RoundedRectangle(size=card.size, pos=card.pos, radius=[dp(Sizes.RADIUS_SMALL)])
                card.bind(size=lambda i, v: setattr(card.canvas.before.children[-1], 'size', v))
                card.bind(pos=lambda i, v: setattr(card.canvas.before.children[-1], 'pos', v))
                
                top_row = BoxLayout(orientation='horizontal', spacing=dp(Sizes.PADDING_SMALL))
                top_row.add_widget(Label(
                    text=pet_name,
                    font_size=Fonts.BODY,
                    bold=True,
                    font_name=CHINESE_FONT,
                    color=Colors.TEXT_PRIMARY
                ))
                # 状态标签 - 使用 Colors.SUCCESS（进行中）和 Colors.GRAY（已结束）
                status_label = Label(
                    text='进行中' if status == 'active' else '已结束',
                    font_size=Fonts.CAPTION,
                    font_name=CHINESE_FONT,
                    color=Colors.SUCCESS if status == 'active' else Colors.GRAY
                )
                top_row.add_widget(status_label)
                card.add_widget(top_row)
                
                card.add_widget(Label(
                    text=f'寄养时间：{start_date} ~ {end_date if end_date else "待定"}',
                    font_size=Fonts.BODY_SMALL,
                    color=Colors.TEXT_SECONDARY,
                    font_name=CHINESE_FONT
                ))
                card.add_widget(Label(
                    text=f'联系人：{contact_name} {contact_phone}',
                    font_size=Fonts.BODY_SMALL,
                    color=Colors.TEXT_SECONDARY,
                    font_name=CHINESE_FONT
                ))
                if contact_addr:
                    card.add_widget(Label(
                        text=f'地址：{contact_addr}',
                        font_size=Fonts.CAPTION,
                        color=Colors.TEXT_HINT,
                        font_name=CHINESE_FONT
                    ))
                
                # 删除按钮 - 使用 Colors.DANGER
                delete_btn = Button(
                    text='删除',
                    size_hint_x=0.15,
                    background_color=Colors.DANGER,
                    font_name=CHINESE_FONT,
                    font_size=Fonts.BODY_SMALL,
                    color=Colors.TEXT_WHITE
                )
                delete_btn.bind(on_press=lambda x, rid=record_id: self.delete_foster(rid))
                
                card.add_widget(delete_btn)
                
                records_grid.add_widget(card)
            
            main_content.add_widget(records_grid)
        
        scroll.add_widget(main_content)
        self.content_layout.add_widget(scroll)
    
    def add_foster(self, instance):
        pet_name = self.pet_spinner.text
        start_date = self.start_date_input.text.strip()
        end_date = self.end_date_input.text.strip()
        contact_name = self.contact_name_input.text.strip()
        contact_phone = self.contact_phone_input.text.strip()
        contact_addr = self.contact_addr_input.text.strip()
        
        if pet_name == '选择宠物' or not pet_name:
            self.show_error('请选择宠物')
            return
        if not start_date:
            self.show_error('请输入寄养开始日期')
            return
        if not contact_name:
            self.show_error('请输入联系人姓名')
            return
        
        pets = PetDatabase.get_all_pets()
        pet_id = None
        for pet in pets:
            if pet[1] == pet_name:
                pet_id = pet[0]
                break
        
        if pet_id:
            PetDatabase.add_foster_record(pet_id, start_date, end_date, contact_name, contact_phone, contact_addr)
            
            self.pet_spinner.text = '选择宠物'
            self.start_date_input.text = ''
            self.end_date_input.text = ''
            self.contact_name_input.text = ''
            self.contact_phone_input.text = ''
            self.contact_addr_input.text = ''
            
            self.show_foster_list()
        else:
            self.show_error('未找到该宠物')
    
    def delete_foster(self, record_id):
        confirm_popup = Popup(
            title='确认删除',
            content=BoxLayout(orientation='vertical', spacing=dp(Sizes.PADDING_SMALL), padding=dp(Sizes.PADDING_MEDIUM)),
            size_hint=(0.5, 0.3),
            title_font=CHINESE_FONT,
            title_color=Colors.TEXT_PRIMARY
        )
        
        confirm_popup.content.add_widget(Label(
            text='确定要删除这条寄养记录吗？',
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
        
        # 删除按钮 - 使用 Colors.DANGER
        delete_btn = Button(
            text='删除',
            background_color=Colors.DANGER,
            font_name=CHINESE_FONT,
            font_size=Fonts.BUTTON,
            color=Colors.TEXT_WHITE
        )
        delete_btn.bind(on_press=lambda x: self.confirm_delete(record_id, confirm_popup))
        
        btn_layout.add_widget(cancel_btn)
        btn_layout.add_widget(delete_btn)
        confirm_popup.content.add_widget(btn_layout)
        
        confirm_popup.open()
    
    def confirm_delete(self, record_id, popup):
        PetDatabase.delete_foster_record(record_id)
        popup.dismiss()
        self.show_foster_list()
    
    def show_error(self, message):
        popup = Popup(
            title='错误',
            content=Label(text=message, font_name=CHINESE_FONT, font_size=Fonts.BODY, color=Colors.TEXT_PRIMARY),
            size_hint=(0.6, 0.3),
            title_font=CHINESE_FONT,
            title_color=Colors.DANGER
        )
        popup.open()
    
    def go_back(self, instance):
        self.manager.current = 'main'