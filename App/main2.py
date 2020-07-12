from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from pytube import YouTube
from PIL import Image, ImageTk
from tkinter import messagebox as tkMessageBox

# sample== https://www.youtube.com/watch?v=ZHQaA9Z6vlQ
FolderName = ""
fileSizeInBytes = 0
MaxFileSize = 0


def openDirectory():
    global FolderName
    FolderName = filedialog.askdirectory()
    if (len(FolderName) > 1):
        fileLocationLabelError.config(text=FolderName, fg="green")

    else:
        fileLocationLabelError.config(text="Please choose folder!", fg="red")


def DownloadFile():
    global MaxFileSize, fileSizeInBytes

    choice = youtubeChoices.get()
    video = youtubeEntry.get()
    try:
        if (len(video) > 1):
            youtubeEntryError.config(text="")
            print(video, "at", FolderName)
            yt = YouTube(video, on_progress_callback=progress)
            # on_complete_callback=complete
            print("Video Name is:\n\n", yt.title)

            if (choice == downloadChoices[0]):
                print("720p Video file downloading...")
                loadingLabel.config(text="Downloaded (720px)")

                selectedVideo = yt.streams.filter(progressive=True).first()

            elif (choice == downloadChoices[1]):
                print("144p video file downloading...")
                loadingLabel.config(text="Downloaded (144px)")
                selectedVideo = yt.streams.filter(progressive=True, file_extension='mp4').last()

            elif (choice == downloadChoices[2]):
                print("3gp file downloading...")
                loadingLabel.config(text="Downloaded (3gp)")
                selectedVideo = yt.streams.filter(file_extension='3gp').first()

            elif (choice == downloadChoices[3]):
                print("Audio file downloading...")
                loadingLabel.config(text="Downloaded (mp3)")
                selectedVideo = yt.streams.filter(only_audio=True).first()

            fileSizeInBytes = selectedVideo.filesize
            MaxFileSize = fileSizeInBytes / 1024000
            MB = str(MaxFileSize) + " MB"
            print("File Size = {:00.00f} MB".format(MaxFileSize))

            # now Download ------->
            selectedVideo.download(FolderName)
            # ==========>
            print("Downloaded on:  {}".format(FolderName))
            # loadingLabel.config(text=("Download Complete ",MB))
            complete()

        else:
            youtubeEntryError.config(text="Please paste youtube link", fg="red")
    except Exception as e:
        print(e)
        print("Error!!")
        tkMessageBox.showinfo("Download", "File Not Found")

# ============progress bar==================
def progress(stream=None, chunk=None, file_handle=None, remaining=None):
    percent = (100 * (fileSizeInBytes - remaining)) / fileSizeInBytes
    print("{:00.0f}% downloaded".format(percent))
    # loadingLabel.config(text="Downloading...")


def complete():
    downloadButton.config(text=("Download Complete"))


# ================tkinter window
root = Tk()
root.title("Video/Audio Downloader")
root.minsize(640, 1000)
root.maxsize(640, 1000)
root.configure(bg="white")
# ===============contents strech ac to windows strech====
root.grid_columnconfigure(0, weight=1)  # strech things Horiontally


# =============youtube link label=================
image6 =Image.open('you.png')
image5 = ImageTk.PhotoImage(image6)
youtubeLinkLabel = Label(root, image=image5)
youtubeLinkLabel.grid(row=0)
youtubeLinkLabel.place(x=0, y=0)

# ==========get youtube link in entry box
youtubeEntryVar = StringVar()
youtubeEntry = Entry(root, width=50, textvariable=youtubeEntryVar, bg="black",fg="white",border=10, font=("Pangolin", 10))
youtubeEntry.place(x=150, y=400, height=35)

# =========when link is wrong print this label
youtubeEntryError = Label(root, fg="red", bg="white", text="", font=("Pangolin", 15))
youtubeEntryError.place(x=150, y=370)

# # Asking where to save file label
# SaveLabel = Label(root, text="Where to download file: ", fg="blue", font=("Arial", 20, "bold"))
# SaveLabel.grid()


# Asking where to save file Button
image4 =Image.open('browse.jpg')
image3 = ImageTk.PhotoImage(image4)
SaveEntry = Button(root, image=image3, width=200, bg="white",border=0, text="Choose folder", font=("Pangolin", 15), command=openDirectory)
SaveEntry.place(x=0, y=500)

# Entry label if user don`t choose directory
fileLocationLabelError = Label(root, text="", bg="white", font=("Pangolin", 20))
fileLocationLabelError.grid()
fileLocationLabelError.place(x=0, y=570)


# ======= what to download choice==========
youtubeChooseLabel = Label(root, text="Select the Format", bg="white", fg="black", font=("Pangolin", 20))
youtubeChooseLabel.grid()
youtubeChooseLabel.place(x=400, y=530)


# Combobox with four choices:
downloadChoices = ["MP4_720p", "Mp4_144p", "Video_3gp", "Song_MP3"]
youtubeChoices = ttk.Combobox(root, values=downloadChoices)
youtubeChoices.grid()
youtubeChoices.place(x=450, y=570)


# ==================Download button===================
image2 =Image.open('download.png')
image1 = ImageTk.PhotoImage(image2)
downloadButton = Button(root,image=image1, text="Download", width=420, bg="white", fg="blue", border=0, command=DownloadFile, font=("Pangolin", 20))
downloadButton.place(x=150, y=600)


loadingLabel = ttk.Label(root, text="App developed by Ayush Jain", font=("Pangolin", 20))
loadingLabel.place(x=150, y=450)

root.mainloop()