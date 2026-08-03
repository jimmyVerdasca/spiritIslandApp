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
android.api = 35
android.minapi = 26
android.archs = arm64-v8a

p4a.branch = stable


[buildozer]
warn_on_root = 0
log_level = 2