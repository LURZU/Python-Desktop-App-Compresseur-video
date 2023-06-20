import os
import subprocess
import tkinter as tk
from tkinter import filedialog

class VideoCompressor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Video Compressor")
        self.geometry("400x300")

        output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
        os.makedirs(output_dir, exist_ok=True)

        self.result_text = tk.Text(self, height=5, width=50)
        self.result_text.pack(pady=10)

        self.configure(bg="#264653") 

        self.select_file_button = tk.Button(self, text="Sélectionner un fichier", command=self.handle_file_selection)
        self.select_file_button.pack(pady=10)
        self.select_file_button.config(image=self.get_folder_icon())
        self.select_file_button.config(compound=tk.LEFT)

        self.video_listbox = tk.Listbox(self)
        self.video_listbox.pack(pady=10)
        videos = self.get_videos_list()
        for video in videos:
            self.video_listbox.insert(tk.END, video)

    def handle_file_selection(self):
        file_path = filedialog.askopenfilename(filetypes=[("Fichiers MP4", "*.mp4")])
        self.compress_video(file_path)

    def get_videos_list(self):
        download_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "download")
        videos = []
        for file in os.listdir(download_dir):
            if file.endswith(".mp4"):
                videos.append(file)
        return videos
    
    def handle_video_selection(self):
        selection = self.video_listbox.curselection()
        if len(selection) == 0:
            self.result_text.insert(tk.END, "Veuillez sélectionner une vidéo à compresser\n")
            return
        video = self.video_listbox.get(selection)
        video_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "download", video)
        self.compress_video(video_path)

        self.select_video_button = tk.Button(self, text="Sélectionner une vidéo", command=self.handle_video_selection)
        self.select_video_button.pack(pady=10)

    def get_folder_icon(self):
        icon_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "./assets/icons/folder.png")
        # charger l'image en tant que PhotoImage
        icon_image = tk.PhotoImage(file=icon_file)
        return icon_image

    def compress_video(self, file_path):
        try:
            if not file_path.endswith(".mp4"):
                self.result_text.insert(tk.END, "Veuillez sélectionner un fichier MP4 valide\n")
                return

            filename, file_extension = os.path.splitext(os.path.basename(file_path))
            output_filename = f"{filename}_compressed.mp4"
            output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output", output_filename)

            # utiliser le mode PIPE pour capturer la sortie de ffmpeg en temps réel
            p = subprocess.Popen(["ffmpeg", "-i", file_path, "-vcodec", "libx265", "-crf", "28", "-preset", "medium", output_path],
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

            # permet d'afficher la sortie des logs FFMPEG
            while True:
                output = p.stdout.readline()
                if output == '' and p.poll() is not None:
                    break
                if output:
                    self.result_text.insert(tk.END, output)
                    self.result_text.see(tk.END)
                    self.update_idletasks()

            self.result_text.insert(tk.END, f"Fichier compressé enregistré sous: {output_path}\n")
        except:
            self.result_text.insert(tk.END, "Erreur lors de la compression de la vidéo\n")


if __name__ == "__main__":
    app = VideoCompressor()
    app.mainloop()
