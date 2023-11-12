from cx_Freeze import setup, Executable
import distutils.util
from pathlib import Path
import sys

upgrade_code = '{b7bc9891-45c7-4f31-bf02-6aa9bcd2b8c3}'  # uuid.uuid4()
all_users = False
source_path = r'.'
py_file = 'main.py'
includes = []
base = 'Win32GUI'
install_dir = 'RenameFiles'
app_name = 'RenameFiles'
caption = 'RenameFiles'
version = '0.0.1'
description = 'RenameFiles Application'
author = 'yamakox'
copyright = '(C) 2023 ' + author
ico_file = r'.\49255_rename_icon.ico'
manifest_file = r'.\main.exe.manifest'

build_exe_options = dict(
    packages = [],
    excludes = [],
    includes = includes,
    path = sys.path + [source_path],
    include_files = [ico_file],
)

programfiles_dir = (
    'ProgramFiles64Folder'
    if distutils.util.get_platform() == 'win-amd64' else
    'ProgramFilesFolder'
)

# https://stackoverflow.com/questions/15734703/use-cx-freeze-to-create-an-msi-that-adds-a-shortcut-to-the-desktop
# https://github.com/marcelotduarte/cx_Freeze/issues/48#issuecomment-274308507
# https://softwarefactory.jp/ja/developer/windowsinstaller/MSI0003.html
# SendToのフォルダは %APPDATA%\Microsoft\Windows\SendTo
# または、「ファイル名を指定して実行」(Win+R)で shell:sendto
# なお、SendToのAll Usersは作れない模様。
bdist_msi_options = dict(
    upgrade_code=upgrade_code,
    all_users=all_users,
    add_to_path=False,
    initial_target_dir=r'[%s]\%s' % (programfiles_dir, install_dir),
    data = dict(
        Shortcut = [
            ('SendToFolderShortcut',    # Shortcut
             'SendToFolder',            # Directory_
             f'ファイル名を一括変更 ({caption})',   # Name
             'TARGETDIR',               # Component_
             '[TARGETDIR]%s.exe' % Path(py_file).stem,  # Target
             None,                      # Arguments
             None,                      # Description
             None,                      # Hotkey
             None,                      # Icon
             None,                      # IconIndex
             None,                      # ShowCmd
             'TARGETDIR'                # WkDir
             ),
        ]
    ),
)

options = dict(
    build_exe = build_exe_options,
    bdist_msi = bdist_msi_options,
)

executables = [
    Executable(Path(source_path) / Path(py_file),
               base=base if sys.platform=='win32' else None,
               icon=ico_file,
               manifest=manifest_file, 
               shortcut_name=caption,
               shortcut_dir='ProgramMenuFolder'
    )
]

setup(name=app_name,
      version = version,
      description = description,
      author = author,
      options = options,
      executables = executables
)
