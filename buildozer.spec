
[app]
title = SwichStats
package.name = SwichStats
package.domain = com.threebest
version = 1.0
source.dir = .
source.main = main.py
orientation = portrait
fullscreen = 0


icon.filename = img/logo.png
#
# Python section
#

requirements = python3,kivy,plyer
android.permissions = INTERNET, VIBRATE

#
# Android section
#

android.api = 33
android.minapi = 21
android.ndk_api = 21

# Android keystore creation parameters.
key.store.password = swichstats
key.alias.password = swichstats


#
# Buildozer section
#

[buildozer]
android.use_gradle_daemon = True
#log_level = 2
