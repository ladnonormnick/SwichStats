%%writefile buildozer.spec
[app]
title = SwitchStats
package.name = switchstats
package.domain = com.threebest
version = 0.1
source.dir = .
source.main = main.py
orientation = portrait
fullscreen = 0

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
key.store.password = switchstats
key.alias.password = switchstats


#
# Buildozer section
#

[buildozer]
android.use_gradle_daemon = True
#log_level = 2
