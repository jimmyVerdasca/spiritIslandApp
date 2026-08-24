[app]

title = Spirit Island Companion Online

package.name = spiritislandonline
package.domain = org.spiritisland.http

version = 0.1.0

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,db,sql,mp3
source.include_patterns = frontend/**,shared/**,config/**,data/**,main.py

requirements = python3==3.10.11,hostpython3==3.10.11,kivy==2.2.1,kivymd==1.2.0,requests==2.32.3

orientation = portrait
fullscreen = 0


# Android

android.archs = arm64-v8a
android.api = 35
android.minapi = 24
android.ndk = 25b
android.ndk_api = 24

android.permissions = INTERNET

android.accept_sdk_license = True

android.release_artifact = aab
android.debug_artifact = apk


# python-for-android

p4a.url = https://github.com/kivy/python-for-android
p4a.branch = master


[buildozer]

warn_on_root = 0
log_level = 2