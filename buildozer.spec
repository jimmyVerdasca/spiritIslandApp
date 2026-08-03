[app]

title = Spirit Island Companion

package.name = spiritisland
package.domain = org.spiritisland

version = 0.1.0

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,db,sql

requirements = python3,kivy==2.2.1,kivymd

orientation = portrait
fullscreen = 0


# Android
android.archs = arm64-v8a
android.api = 33
android.minapi = 24
android.ndk = 25b
android.ndk_api = 24

android.accept_sdk_license = True

android.release_artifact = aab
android.debug_artifact = apk


# python-for-android
p4a.url = https://github.com/kivy/python-for-android
p4a.branch = master


[buildozer]
warn_on_root = 0
log_level = 2