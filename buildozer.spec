[app]

# (str) Title of your application
title = QI1489

# (str) Package name
package.name = qi1489

# (str) Package domain (needed for android/ios packaging)
package.domain = org.smjxgame

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,kv,atlas,ttf,db

# (str) Application versioning
version = 1.0

# (list) Application requirements
requirements = python3,kivy==2.2.1,kivymd==1.1.1,requests,certifi,urllib3,chardet,charset-normalizer,idna,android

# (str) Supported orientation
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK / AAB will support.
android.minapi = 24

# (str) Android NDK version to use
android.ndk = 25b

# (str) Android SDK directory (if empty, it will be automatically downloaded.)
# android.sdk_path =

# (str) ANT directory
# android.ant_path =

# (bool) Enable AndroidX support. Enable when 'android.gradle_dependencies'
# contains 'androidx' packages.
android.enable_androidx = True

# (str) Application icon
# icon.filename = %(source.dir)s/assets/icon.png

# (str) Presplash color
android.presplash_color = #0A0E27

# (list) The Android archs to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a

# Use latest python-for-android (fixes -luuid missing on NDK)
p4a.branch = master

# (bool) enables Android auto backup feature (Android API >=23)
android.allow_backup = True

# (str) OUYA Console category. Should be one of GAME or APP
# If you leave this blank, OUYA will classify your app as APP
# ouya.category = GAME

# (str) Filename of OUYA Console icon.
# It must be a 732x412 png image.
# ouya.icon.filename = %(source.dir)s/assets/ouya_icon.png

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = disable to allow as root)
warn_on_root = 1
