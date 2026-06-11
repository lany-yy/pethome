"""
宠物管家 - 猫狗宠物管理系统
作者：宠物管家团队
版本：1.0.0
"""

import os
import sys

from kivy.core.text import LabelBase

CHINESE_FONT = 'Chinese'

def setup_fonts():
    font_paths = [
        'assets/fonts/NotoSansCJK-Regular.ttc',
        'assets/fonts/SourceHanSansSC-Regular.otf',
        'C:/Windows/Fonts/msyh.ttc',
        'C:/Windows/Fonts/simsun.ttc',
        'C:/Windows/Fonts/simhei.ttf',
    ]
    
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                LabelBase.register(name=CHINESE_FONT, fn_regular=font_path)
                print(f"成功加载字体: {font_path}")
                return
            except Exception as e:
                print(f"加载字体失败 {font_path}: {e}")
                continue
    
    try:
        LabelBase.register(name=CHINESE_FONT, fn_regular='Roboto')
        print("使用默认Roboto字体")
    except:
        pass

setup_fonts()

from kivy.config import Config
Config.set('input', 'mouse', 'mouse,disable_multitouch')
Config.set('kivy', 'exit_on_escape', '0')
Config.set('kivy', 'keyboard_mode', 'system')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.resources import resource_add_path

from screens.main_screen import MainScreen
from screens.pet_list_screen import PetListScreen
from screens.add_pet_screen import AddPetScreen
from screens.pet_detail_screen import PetDetailScreen
from screens.vaccine_screen import VaccineScreen
from screens.weight_screen import WeightScreen
from screens.reminder_screen import ReminderScreen
from screens.stats_screen import StatsScreen
from screens.pet_types_screen import PetTypesScreen
from screens.foster_screen import FosterScreen

from database.pet_db import init_database

class PetManagerApp(App):
    """宠物管家主应用类"""
    
    def build(self):
        init_database()
        
        sm = ScreenManager(transition=SlideTransition(duration=0.3))
        
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(PetListScreen(name='pet_list'))
        sm.add_widget(AddPetScreen(name='add_pet'))
        sm.add_widget(PetDetailScreen(name='pet_detail'))
        sm.add_widget(VaccineScreen(name='vaccine'))
        sm.add_widget(WeightScreen(name='weight'))
        sm.add_widget(ReminderScreen(name='reminder'))
        sm.add_widget(StatsScreen(name='stats'))
        sm.add_widget(PetTypesScreen(name='pet_types'))
        sm.add_widget(FosterScreen(name='foster'))
        
        return sm
    
    def on_start(self):
        print("宠物管家已启动")
    
    def on_stop(self):
        print("宠物管家已关闭")

if __name__ == '__main__':
    PetManagerApp().run()