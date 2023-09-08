import os
import tkinter as tk
from tkinter import filedialog
import socket
import threading


class SenderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sender App")

        self.filepath = ""
        self.destination_ip = ""

        self.create_widgets()

    def create_widgets(self):
        self.file_label = tk.Label(self.root, text="Fichier à envoyer :")
        self.file_label.pack()

        self.select_file_button = tk.Button(self.root, text="Sélectionner un fichier", command=self.select_file)
        self.select_file_button.pack()

        self.destination_label = tk.Label(self.root, text="Adresse IP du destinataire :")
        self.destination_label.pack()

        self.destination_entry = tk.Entry(self.root)
        self.destination_entry.pack()

        self.send_button = tk.Button(self.root, text="Envoyer", command=self.send_file)
        self.send_button.pack()

    def select_file(self):
        self.filepath = filedialog.askopenfilename()

    def send_file(self):
        self.destination_ip = self.destination_entry.get()
        if not self.filepath or not self.destination_ip:
            return

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.destination_ip, 12345))  # Utilisez le port que vous préférez

            filename = os.path.basename(self.filepath)
            s.send(filename.encode())

            with open(self.filepath, 'rb') as file:
                while True:
                    data = file.read(1024)
                    if not data:
                        break
                    s.send(data)

            s.close()
            print("Fichier envoyé avec succès.")
        except Exception as e:
            print(f"Erreur lors de l'envoi : {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = SenderApp(root)
    root.mainloop()
