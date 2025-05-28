[app]
# (str) Title of your application
title = MyApp

# (str) Package name
package.name = SwichStats

# (str) Package domain (needed for android packaging)
package.domain = org.myorg

# (str) Version of your application
version = 0.1

# (str) Application source file
source.main = main.py

# (list) Application source files
source.include_exts = py,png,jpg,kv,atlas

# (str) Application requirements
requirements = python3,kivy

# (str) Supported orientation (one of: landscape, sensorLandscape, portrait, sensorPortrait, all)
orientation = portrait

# (bool) Whether the application should be fullscreen
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET

# (list) Supported platforms
# (str) Android and iOS; Apple's distribution requires a Mac OS
# platform = android,ios

# (str) Application icon
icon.filename = %(source.dir)s/icon.png

# (str) Additional added files
# (list) Application data files to be included in the package
# (python file) Excluded files can be also added to the `source.exclude_patterns` variable.
# source.exclude_patterns =