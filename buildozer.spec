[app]

title = 宠物管家
package.name = petmanager
package.domain = com.petmanager
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,txt,db,spec,json
version = 1.0.0

# 关键修改：移除版本号，让系统自动选择
requirements = python3, kivy==2.1.0, sqlite3

orientation = portrait
fullscreen = 0
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21
android.private_storage = True
android.python_version = 3
android.accept_sdk_license = True
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

log_level = 2

osx.python_version = 3
osx.kivy_version = 2.1.0

ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master
ios.ios_deploy_url = https://github.com/phonegap/ios-deploy
ios.ios_deploy_branch = 1.10.0

[buildozer]
log_level = 2
warn_on_root = 1
