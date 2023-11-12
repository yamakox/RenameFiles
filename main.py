import wx
import wx.lib.scrolledpanel as scrolled
import sys
from pathlib import Path

invalid_charactors = dict(
    win32 = set('\\/:*?"<>|')
)

class MainApp(wx.App):
    def OnInit(self):
        self.frame = MainFrame(None, title='RenameFiles')
        self.frame.Show()
        self.frame.add_filenames(sys.argv[1:])
        #self.frame.add_test()
        if len(self.frame.items):
            k = list(self.frame.items.keys())[0]
            self.frame.items[k].text_ctrl.SetFocus()
        return True

class MainFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(MainFrame, self).__init__(*args, **kw)
        self.items = {}

        self.SetSize(self.FromDIP(wx.Size(800, 450)))
        self.SetIcon(wx.Icon(r'.\49255_rename_icon.ico'))
        self.SetDropTarget(FileDropTarget(self))

        panel = wx.Panel(self)
        sizer = wx.FlexGridSizer(2, 1, wx.Size(2, 2))
        sizer.AddGrowableRow(0)
        sizer.AddGrowableCol(0)
        panel.SetSizer(sizer)

        self.filename_list_panel = FilenameListPanel(panel)
        sizer.Add(self.filename_list_panel, flag=wx.EXPAND)

        button_panel = wx.Panel(panel)
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_panel.SetSizer(button_sizer)
        self.rename_btn = wx.Button(button_panel, label='Rename Files')
        self.close_btn = wx.Button(button_panel, label='Close')
        self.rename_btn.Bind(wx.EVT_BUTTON, self.on_rename)
        self.close_btn.Bind(wx.EVT_BUTTON, self.on_cancel)
        button_sizer.AddStretchSpacer()
        button_sizer.Add(self.rename_btn, flag=wx.TOP|wx.RIGHT|wx.BOTTOM, border=4)
        button_sizer.Add(self.close_btn, flag=wx.TOP|wx.RIGHT|wx.BOTTOM, border=4)
        sizer.Add(button_panel, flag=wx.EXPAND|wx.RIGHT|wx.BOTTOM, border=6)

    def add_filenames(self, filenames):
        for i in filenames:
            filepath = Path(i)
            if filepath in self.items:
                continue
            item = FilenameItem(self.filename_list_panel, filepath=filepath)
            self.filename_list_panel.add(item)
            self.items[item.filepath] = item
        self.filename_list_panel.update_layout()

    def add_test(self):
        self.add_filenames(['AAA', 'BBB', 'CCCC'] * 10)

    def on_rename(self, event):
        self.__rename_files()

    def on_cancel(self, event):
        self.Destroy()

    def __rename_files(self):
        files = []
        try:
            for (key, item) in self.items.items():
                if item.rename():
                    files.append(item.name)
        except Exception as ex:
            item.text_ctrl.SetFocus()
            wx.MessageBox(str(ex), parent=self, style=wx.OK_DEFAULT|wx.ICON_ERROR)
        if files:
            wx.MessageBox('ファイル名を変更しました。\n\n' + '\n'.join(files), parent=self)

class FileDropTarget(wx.FileDropTarget):
    def __init__(self, frame: MainFrame, *args, **kw):
        super(FileDropTarget, self).__init__(*args, **kw)
        self.frame = frame

    def OnDropFiles(self, x, y, filenames):
        self.frame.add_filenames(filenames)
        return True

class FilenameListPanel(scrolled.ScrolledPanel):
    def __init__(self, *args, **kw):
        super(FilenameListPanel, self).__init__(*args, **kw)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)

    def add(self, item):
        self.sizer.Add(item.sizer, flag=wx.EXPAND|wx.LEFT|wx.TOP|wx.RIGHT, border=4)

    def update_layout(self):
        self.SetAutoLayout(True)
        self.SetupScrolling(scrollIntoView=True, scrollToTop=False)

class FilenameItem():
    def __init__(self, parent, filepath: Path):
        self.filepath = filepath
        self.filename = self.filepath.name

        self.sizer = wx.FlexGridSizer(1, 3, wx.Size(2, 0))
        self.sizer.AddGrowableCol(0)
        #self.SetSizer(self.sizer)5

        self.text_ctrl = wx.TextCtrl(parent, value=self.filename)
        # self.text_ctrl.SetHint(self.filename)
        self.reset_btn = wx.Button(parent, label='🔄️', style=wx.BU_EXACTFIT)
        self.delete_btn = wx.Button(parent, label='✖', style=wx.BU_EXACTFIT)
        self.reset_btn.DisableFocusFromKeyboard()
        self.delete_btn.DisableFocusFromKeyboard()
        self.reset_btn.Bind(wx.EVT_BUTTON, self.on_reset)
        self.delete_btn.Bind(wx.EVT_BUTTON, self.on_delete)
        self.sizer.Add(self.text_ctrl, flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=4)
        self.sizer.Add(self.reset_btn)
        self.sizer.Add(self.delete_btn)

    def on_reset(self, event):
        # self.text_ctrl.SetValue(self.filename)
        self.text_ctrl.ChangeValue(self.filename)

    def on_delete(self, event):
        app.frame.filename_list_panel.sizer.Remove(self.sizer)
        self.text_ctrl.Destroy()
        self.reset_btn.Destroy()
        self.delete_btn.Destroy()
        app.frame.filename_list_panel.update_layout()
        del app.frame.items[self.filepath]

    def rename(self):
        self.name = self.text_ctrl.GetValue().strip()
        if len(self.name) < 1:
            self.raise_error('ファイル名を入力してください。')
        elif (sys.platform in invalid_charactors and 
              len(invalid_charactors[sys.platform] & set(self.name))):
            self.raise_error('ファイル名に使用できない文字が含まれています。\n\nファイル名: ' + self.name)
        new_filepath = self.filepath.parent / self.name
        if self.filepath == new_filepath:
            return False
        if new_filepath.exists():
            self.raise_error('同名のファイルが既に存在します。\n\nファイル名: ' + self.name)
        self.filepath.rename(new_filepath)
        self.filepath = new_filepath
        self.text_ctrl.ChangeValue(self.name)
        return True

    def raise_error(self, text):
        raise Exception(text)

    def __str__(self) -> str:
        return f'FilenameItem("{self.filepath}", "{self.name}")'

if __name__ == '__main__':
    app = MainApp()
    app.MainLoop()
