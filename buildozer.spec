[app]

# (str) Title of your application
title = 宠物管家

# (str) Package name
package.name = petmanager

# (str) Package domain (needed for android/ios packaging)
package.domain = com.petmanager

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,kv,atlas,ttf,txt,db,spec,json

# (str) Application versioning
version = 1.0.0

# (list) Application requirements
# 关键修改：使用 Python 3.11
requirements = python3==3.11, kivy==2.1.0, sqlite3, pillow

# (str) Supported orientation
orientation = portrait

# Android specific
fullscreen = 0
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21
android.private_storage = True
android.python_version = 3.11  # 关键修改
android.accept_sdk_license = True
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

# Log level
log_level = 2

# OSX Specific
osx.python_version = 3
osx.kivy_version = 2.1.0

# iOS specific
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master
ios.ios_deploy_url = https://github.com/phonegap/ios-deploy
ios.ios_deploy_branch = 1.10.0

[buildozer]
log_level = 2
warn_on_root = 1
