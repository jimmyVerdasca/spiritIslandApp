[app]

title = Spirit Island Companion

package.name = spiritisland
package.domain = org.spiritisland

version = 0.1.0

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,db,sql

requirements = python3,kivy,kivymd

orientation = portrait
fullscreen = 0


# Android
android.accept_sdk_license = True
android.minapi = 26
android.api = 36
android.ndk = 29
android.archs = arm64-v8a,x86_64

p4a.branch = develop



[buildozer]
warn_on_root = 0
log_level = 2