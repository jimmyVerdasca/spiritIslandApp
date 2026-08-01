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

android.api = 33
android.minapi = 24

android.archs = arm64-v8a,x86_64

android.build_tools_version = 33.0.2

android.ndk = 25b

# Force Android Python recipe
android.python_version = 3.10


[buildozer]

warn_on_root = 0

# Keep stable p4a branch
p4a.branch = master