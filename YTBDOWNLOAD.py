from pytube import YouTube, Playlist
from kivy.lang import Builder
from kivymd.app import MDApp
import os
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.filemanager import MDFileManager
from kivymd.toast import toast
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivymd.uix.dropdownitem import MDDropDownItem
import threading
import kivy.clock as Clock

class App(MDApp):
    pathdownload = ""
    def __init__(self, **kwargs):
        self.lblPath = []
        super().__init__(**kwargs)
        Window.bind(on_keyboard=self.events)
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager, select_path=self.select_path,
        )

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"
        return None

    def file_manager_open(self):
        self.file_manager.show_disks()  # output manager to the screen
        self.manager_open = True

    def select_path(self, path: str):

        label = MDLabel(id='lblPath', text=path, pos_hint={"center_x": .5, "center_y": .45}, halign="center")
        if(len(self.lblPath) > 0):
            self.root.remove_widget(self.lblPath[0])
            self.lblPath.pop(0)
        self.lblPath.append(label)
        self.root.add_widget(label)
        self.pathdownload = self.lblPath[0].text
        self.exit_manager()

    def exit_manager(self, *args):
        self.manager_open = False
        self.file_manager.close()

    def events(self, instance, keyboard, keycode, text, modifiers):
        '''Called when buttons are pressed on the mobile device.'''

        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()
        return True

    def Download(self):
        formato = 0
        if (self.root.ids.audio.state == "down"):
            formato = 1
        else:
            formato = 2

        if len(self.pathdownload) <= 0:
            self.showDialog("ERROR", "Escolha uma pasta onde salvar!")
            return

        video_Link = self.root.ids.urlYoutube.text

        if len(video_Link) > 0:
            try:
                if "playlist" not in video_Link:
                    yt = YouTube(video_Link)
                    thread = threading.Thread(target=self.downloadYt, args=(yt, formato))
                    thread.start()
                else:
                    p = Playlist(video_Link)
                    for url in p.video_urls:
                        yt = YouTube(url)
                        thread = threading.Thread(target=self.downloadYt, args=(yt, formato))
                        thread.start()

            except Exception as e:
                print(e)
                self.showDialog("ERROR", "Houve uma erro ao extrair o vídeo! Tente novamente!")

    def downloadYt(self, yt, opcaoFormato):
        self.root.ids.spinner.active = True
        self.root.ids.btnDownload.disabled = True
        self.root.ids.btnDownload.text = "Salvando..."
        try:
            if opcaoFormato == 1:
                audio = yt.streams.filter(file_extension='mp4', type='audio', progressive=False).desc().first()
                audio.download(self.pathdownload)
            if opcaoFormato == 2:
                video = yt.streams.filter(type='video', file_extension='mp4', progressive=True).desc().first()
                video.download(self.pathdownload)
            Clock.Clock.create_trigger(self.showDialog("Salvo", yt.title + " foi salvo!"))
        except Exception as e:
            print(e)
            self.showDialog('ERROR', 'Não foi possivel baixar ' + yt.title)
        finally:
            self.root.ids.btnDownload.disabled = False
            self.root.ids.btnDownload.text = "Salvar"
            self.root.ids.spinner.active = False
    def showDialog(self, title, text):
        dialog = MDDialog(
            title=title,
            text=text)
        dialog.open()


App().run()
