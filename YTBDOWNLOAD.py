from pytube import YouTube, Playlist
from kivy.lang import Builder
from kivymd.app import MDApp
import os
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.filemanager import MDFileManager
from kivymd.toast import toast
from kivymd.icon_definitions import md_icons

class App(MDApp):

    pathdownload = ""
    def __init__(self, **kwargs):
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
        self.pathdownload = path
        self.exit_manager()

    def exit_manager(self, *args):
        self.manager_open = False
        self.file_manager.close()

        self.Download()
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
        video_Link = self.root.ids.urlYoutube.text

        if len(video_Link) > 0:
            if "playlist" not in video_Link:
                self.downloadVideo(video_Link, self.pathdownload, formato)
            else:
                self.downloadPlaylist(video_Link, self.pathdownload, formato)
        else:
            toast("ENDEREÇO INVÁLIDO! VERIFIQUE O LINK DO VIDEO!")


    def downloadPlaylist(self, video_Link, path, opcaoFormato):
        try:
            link = video_Link

            p = Playlist(link)

            toast("Baixando a playlist "+ p.title)

            for url in p.video_urls:
                yt = YouTube(url)
                if (opcaoFormato == 1):
                    audio = yt.streams.filter(only_audio=True, file_extension='mp4').desc()[0]
                    audio.download(path)
                if (opcaoFormato == 2):
                    video = yt.streams.filter(file_extension='mp4', only_video=True)[0]
                    video.download(path)

            toast("Finalizado. Salvo em " + path)
            toast("A PLAYLIST "+p.title+" FOI SALVA EM \n"
                                + path)
        except:
            toast("Não foi possivel realizar o download da playlist! Tente novamente!")


    def downloadVideo(self, video_Link, path, opcaoFormato):
        try:
            link = video_Link
            yt = YouTube(link)
            toast("Baixando o vídeo "+ yt.title)
            if(opcaoFormato == 1):
                audio = yt.streams.filter(only_audio=True, file_extension='mp4').desc()[0]
                audio.download(path)
            if (opcaoFormato == 2):
                video = yt.streams.filter(file_extension='mp4', only_video=True)[0]
                video.download(path)

            toast("O VÍDEO "+yt.title+" FOI SALVO EM \n"
                                + path)
        except:
            toast("Não foi possivel realizar o download do vídeo! Verifique se o vídeo é publica e tente novamente!")

App().run()
