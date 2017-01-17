# -*- mode: python -*-

block_cipher = None


a = Analysis(['interface.py'],
             pathex=['/Users/katiedaisey/Desktop/projects/scheduling/interface'],
             binaries=None,
             datas=None,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='TA Scheduling',
          debug=False,
          strip=False,
          upx=True,
          console=False , version='version.txt', icon='icon.ico')
app = BUNDLE(exe,
             name='TA Scheduling.app',
             icon='icon.ico',
             bundle_identifier='com.kmd.katiedaisey.TAScheduling',
             info_plist={
             'CFBundleIdentifier': 'com.kmd.katiedaisey.TAScheduling',
             'CFBundleShortVersionString': '1.0.0',
             'CFBundleExecutable': 'MacOS/TA Scheduling',
             'CFBundleName': 'TA Scheduling',
             'CFBundleInfoDictionaryVersion': '6.0',
             'CFBundleDisplayName': 'TA Scheduling',
             'CFBundleIconFile': 'icon.ico',
             'CFBundlePackageType': 'APPL',
             'LSBackgroundOnly': '1',
             'UILaunchImageFile': 'icon.ico',
             }
             )
