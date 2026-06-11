[app]

# (str) Title of your application
title = 宠物管家

# (str) Package name
package.name = petmanager

# (str) Package domain (needed for android/ios packaging)
package.domain = com.petmanager

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,ttf,txt,db,spec,json

# (str) Application versioning (method 1)
version = 1.0.0

# (list) Application requirements
# 关键修改：移除 python3 的版本号，让 Buildozer 自动匹配
requirements = python3, hostpython3, kivy==2.1.0, sqlite3, pillow

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

#
# Android specific
#

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (int) Android NDK API to use.
android.ndk_api = 21

# (bool) Use --private data storage (True) or --dir public storage (False)
android.private_storage = True

# (str) Python version (android.python_version for android)
android.python_version = 3

# (bool) If True, then automatically accept SDK license
android.accept_sdk_license = True

# (str) The Android archs to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a, armeabi-v7a

# (bool) enables Android auto backup feature (Android API >=23)
android.allow_backup = True

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

#
# OSX Specific
#

osx.python_version = 3
osx.kivy_version = 2.1.0

#
# iOS specific
#

ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master
ios.ios_deploy_url = https://github.com/phonegap/ios-deploy
ios.ios_deploy_branch = 1.10.0

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
