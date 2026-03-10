[app]
title = Green Energy City
package.name = greenenergycity
package.domain = org.greenenergycity

icon.filename = data/splash/icon.png
presplash.filename = data/splash/presplash.png
# Цвет фона presplash совпадает с фоном заставки (белый),
# а затем плавно переходит к тёмно-зелёному фону приложения.
android.presplash_color = #ffffff

source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

requirements = python3,kivy

orientation = portrait
fullscreen = 1

android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
