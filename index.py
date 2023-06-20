import tkinter as tk
from tkinter import ttk
from compressor import VideoCompressor
from pytube import YouTube
import os
from tkinter import filedialog

class AppMenu(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Video Compressor")
        self.geometry("900x900")
     
        self.menu = tk.Menu(self)
        self.config(menu=self.menu)

        self.file_menu = tk.Menu(self.menu, tearoff=0)
        self.file_menu.add_command(label="Exit", command=self.quit)
        self.menu.add_cascade(label="File", menu=self.file_menu)

        self.functionality_menu = tk.Menu(self.menu, tearoff=0)
        self.functionality_menu.add_command(label="Compresseur vidéo (FFmpeg)", command=self.open_video_compressor)
        self.functionality_menu.add_command(label="Télécharger vidéo youtube", command=self.download_video)
        self.menu.add_cascade(label="Fonctionnalité", menu=self.functionality_menu)

        self.configure(bg="#1c2331") 
        self.menu.configure(bg="#1c2331", fg="#ffffff") 


        # Frame download
        self.download_frame = tk.Frame(self, bd=2, relief=tk.GROOVE)
        self.download_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)

        self.download_label = tk.Label(self.download_frame, text="Vidéos téléchargées", font=("Helvetica", 16, "bold"), fg="#ffffff", bg="#007acc")
        self.download_label.pack(pady=10)
        self.download_listbox = tk.Listbox(self.download_frame, width=100, height=20)
        self.download_listbox.pack(pady=10)

        self.open_folder_icon = tk.PhotoImage(file="./assets/icons/folder-open.png")
        self.open_folder_button = tk.Button(self.download_frame, text="Ouvrir le dossier", command=self.open_download_folder, image=self.open_folder_icon, compound="left")
        self.open_folder_button.pack(pady=10)
        

        self.refresh_icon = tk.PhotoImage(file="./assets/icons/refresh.png")
        self.refresh_button = tk.Button(self.download_frame, text="Rafraîchir la liste", command=self.refresh_download_list, image=self.refresh_icon, compound="left")
        self.refresh_button.pack(pady=10)

        self.compress_icon = tk.PhotoImage(file="./assets/icons/compress.png")
        self.compress_button = tk.Button(self.download_frame, text="Ouvrir le compresseur", command=self.open_video_compressor, image=self.compress_icon, compound="left")
        self.compress_button.pack(pady=10)

        self.delete_icon = tk.PhotoImage(file="./assets/icons/delete.png")
        self.delete_button = tk.Button(self.download_frame, text="Supprimer", command=self.delete_video, image=self.delete_icon, compound="left")
        self.delete_button.pack(pady=10)

        self.download_button = tk.Button(self, text="Télécharger vidéo Youtube", command=self.download_video, bg="#007acc", fg="#ffffff", font=("Helvetica", 14, "bold"), pady=10)
        self.download_button.pack(side=tk.TOP, pady=10)

        self.refresh_download_list()
        self.download_label = ttk.Label(self, text="")
        self.download_label.pack()



    def delete_video(self):
        selection = self.download_listbox.curselection()
        if len(selection) == 0:
            tk.messagebox.showwarning("Supprimer", "Veuillez sélectionner une vidéo à supprimer.")
            return
        video = self.download_listbox.get(selection)
        video_path = os.path.join(os.getcwd(), "download", video.split(" (")[0])
        confirm = tk.messagebox.askyesno("Supprimer", f"Êtes-vous sûr de vouloir supprimer {video} ?")
        if confirm:
            try:
                os.remove(video_path)
                tk.messagebox.showinfo("Supprimer", "La vidéo a été supprimée.")
                self.refresh_download_list()  # Actualiser la liste des vidéos téléchargées
            except:
                tk.messagebox.showerror("Supprimer", "Une erreur est survenue lors de la suppression de la vidéo.")

    def open_download_folder(self):
        download_folder = os.path.join(os.getcwd(), "download")
        if os.path.exists(download_folder):
            os.startfile(download_folder)
        else:
            tk.messagebox.showwarning("Ouvrir le dossier", "Le dossier de téléchargement n'existe pas.")

    def refresh_download_list(self):
        self.download_listbox.delete(0, tk.END) 
        download_folder = os.path.join(os.getcwd(), "download")
        if os.path.exists(download_folder):
            for filename in os.listdir(download_folder):
                filepath = os.path.join(download_folder, filename)
                if os.path.isfile(filepath) and filename.endswith(".mp4"):
                    filesize = os.path.getsize(filepath)
                    filesize_str = self.format_filesize(filesize)
                    self.download_listbox.insert(tk.END, f"{filename} ({filesize_str})")

    def open_video_compressor(self):
        video_compressor = VideoCompressor()
        video_compressor.mainloop()

    def download_video(self):
        if not os.path.exists("download"):
            os.makedirs("download")
        url = tk.simpledialog.askstring("Download Video", "Entrer l'url d'une vidéo youtube:")
        if url is None:
            return

        try:
            yt = YouTube(url)
            video = yt.streams.get_highest_resolution()
            video.download("download")
            
            tk.messagebox.showinfo("Download Video", "La vidéo a bien été téléchargée!")
            self.refresh_download_list()  # Actualiser la liste des vidéos téléchargées
        except:
            tk.messagebox.showerror("Download Video", "Une erreur est survenue lors du téléchargement, veuillez vérifier l'URL.")

    def format_filesize(self, filesize):
        # Convertir la taille en octets en une chaîne de caractères plus lisible
        for unit in ["o", "Ko", "Mo", "Go", "To"]:
            if filesize < 1024:
                return f"{filesize:.1f} {unit}"
            filesize /= 1024

if __name__ == "__main__":
    app = AppMenu()
    app.mainloop()
