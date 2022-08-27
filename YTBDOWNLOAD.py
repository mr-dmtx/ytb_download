from pytube import YouTube, Playlist
import tkinter as tk
from tkinter import *
from tkinter import messagebox, filedialog

def Widgets():
    head_label = Label(root, text="YouTube Video Downloader",
                       padx=10,
                       pady=15,
                       font="SegoeUI 20",
                       bg="black",
                       fg="white")
    head_label.grid(row=1,
                    column=1,
                    pady=10,
                    padx=10,
                    columnspan=2)

    link_label = Label(root,
                       text="YouTube Link :",
                       bg="black",
                       fg="white",
                       pady=5,
                       padx=5)
    link_label.grid(row=2,
                    column=0,
                    pady=5,
                    padx=5)

    root.linkText = Entry(root,
                          width=35,
                          textvariable=video_Link,
                          font="Arial 14")
    root.linkText.grid(row=2,
                       column=1,
                       pady=5,
                       padx=5,
                       columnspan=2)

    destination_label = Label(root,
                              text="Pasta destino:",
                              bg="black",
                              fg="white",
                              pady=5,
                              padx=9)
    destination_label.grid(row=3,
                           column=0,
                           pady=5,
                           padx=5)

    root.destinationText = Entry(root,
                                 width=27,
                                 textvariable=download_Path,
                                 font="Arial 14")
    root.destinationText.grid(row=3,
                              column=1,
                              pady=5,
                              padx=5)

    browse_B = Button(root,
                      text="Procurar",
                      command=Browse,
                      width=10,
                      bg="gray",
                      relief=GROOVE)
    browse_B.grid(row=3,
                  column=2,
                  pady=1,
                  padx=1)

    Download_B = Button(root,
                        text="BAIXAR VIDEO",
                        command=Download,
                        width=20,
                        bg="gray",
                        pady=10,
                        padx=15,
                        relief=GROOVE,
                        font="Georgia, 13")
    Download_B.grid(row=6,
                    column=1,
                    pady=20,
                    padx=20)


# Defining Browse() to select a
# destination folder to save the video

def Browse():
    # Presenting user with a pop-up for
    # directory selection. initialdir
    # argument is optional Retrieving the
    # user-input destination directory and
    # storing it in downloadDirectory
    download_Directory = filedialog.askdirectory(
        initialdir="YOUR DIRECTORY PATH", title="Save Video")

    # Displaying the directory in the directory
    # textbox
    download_Path.set(download_Directory)


# Defining Download() to download the video

def Download():
    if len(video_Link.get()) > 0:
        if "playlist" not in video_Link.get():
            downloadVideoAudio()
        else:
            downloadPlaylistAudio()
    else:
        messagebox.showerror("ERRO", "ENDEREÇO INVÁLIDO! VERIFIQUE O LINK DO VIDEO!")


def downloadPlaylistAudio():
    try:
        print("Link da playlist:")
        link = video_Link.get()

        p = Playlist(link)

        print("Baixando a playlist "+ p.title)

        for url in p.video_urls:
            yt = YouTube(url)
            audio = yt.streams.filter(only_audio=True)[0]
            audio.download(download_Path.get())
            print(yt.title)
        print("Finalizado. Salvo em " + download_Path.get())
        messagebox.showinfo("SUCESSO",
                            "A PLAYLIST "+p.title+" FOI SALVA EM \n"
                            + download_Path.get())
    except:
        messagebox.showerror("ERROR","Não foi possivel realizar o download da playlist! Tente novamente!")


def downloadVideoAudio():
    try:
        print("Link do vídeo:")
        link = video_Link.get()

        yt = YouTube(link)
        print("Baixando o vídeo", yt.title)

        audio = yt.streams.filter(only_audio=True)[0]
        audio.download(download_Path.get())

        print("Finalizado. Salvo em " + download_Path.get())
        messagebox.showinfo("SUCESSO",
                            "O AUDIO DO VÍDEO"+yt.title+" FOI SALVO EM \n"
                            + download_Path.get())
    except:
        messagebox.showerror("ERROR",
                            "Não foi possivel realizar o download do vídeo! Verifique se a playlist é publica e tente novamente!")

# Creating object of tk class
root = tk.Tk()

# Setting the title, background color
# and size of the tkinter window and
# disabling the resizing property
root.geometry("520x300")
root.resizable(False, False)
root.title("YouTube Video Downloader")
root.config(background="Black")

# Creating the tkinter Variables
video_Link = StringVar()
download_Path = StringVar()

# Calling the Widgets() function
Widgets()

# Defining infinite loop to run
# application
root.mainloop()