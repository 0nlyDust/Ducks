import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import pygame
import random
import sys
import os

MAX_PATOS = 10
IDLE_LIMIT = 200

def resource_path(relative_path):
    """Obtiene la ruta correcta para PyInstaller o desarrollo normal"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class DuckClicker:
    def __init__(self, root):
        self.root = root
        self.root.title("🌸 Estanque de Patitos Adorable 🌸")
        self.score = 0
        self.ducks = []
        self.hearts = []

        # --- Cargar GIF de fondo ---
        self.bg_gif = Image.open(resource_path("imagenes/fondo_animated.gif"))
        self.screen_width, self.screen_height = self.bg_gif.size
        self.root.geometry(f"{self.screen_width}x{self.screen_height}")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(root, width=self.screen_width, height=self.screen_height)
        self.canvas.pack()

        self.bg_frames = [ImageTk.PhotoImage(frame.convert("RGBA")) for frame in ImageSequence.Iterator(self.bg_gif)]
        self.bg_item = self.canvas.create_image(0, 0, anchor="nw", image=self.bg_frames[0])
        self.bg_index = 0
        self.animate_bg()

        # --- Sprites de patos ---
        self.sprites = {
            "left": [tk.PhotoImage(file=resource_path(f"imagenes/patos/izq{i}.png")) for i in range(1,5)],
            "right": [tk.PhotoImage(file=resource_path(f"imagenes/patos/der{i}.png")) for i in range(1,5)],
            "sleep_left": [tk.PhotoImage(file=resource_path(f"imagenes/patos/dormir_izq{i}.png")) for i in range(1,12)],
            "sleep_right": [tk.PhotoImage(file=resource_path(f"imagenes/patos/dormir_der{i}.png")) for i in range(1,12)],
            "fly_start_left": [tk.PhotoImage(file=resource_path(f"imagenes/patos/init_volar_izq{i}.png")) for i in range(1,7)],
            "fly_start_right": [tk.PhotoImage(file=resource_path(f"imagenes/patos/init_volar_der{i}.png")) for i in range(1,7)],
            "fly_left": [tk.PhotoImage(file=resource_path(f"imagenes/patos/volar_izq{i}.png")) for i in range(1,7)],
            "fly_right": [tk.PhotoImage(file=resource_path(f"imagenes/patos/volar_der{i}.png")) for i in range(1,7)]
        }

        # --- Inicializar mixer de pygame ---
        pygame.mixer.init()
        pygame.mixer.music.load(resource_path("sonidos/fondo.mp3"))
        pygame.mixer.music.play(-1)

        # --- Efectos de sonido ---
        self.sonido_pato = pygame.mixer.Sound(resource_path("sonidos/pato.wav"))
        self.sonido_dormir = pygame.mixer.Sound(resource_path("sonidos/duerme.wav"))
        self.sonido_volar = pygame.mixer.Sound(resource_path("sonidos/volar.wav"))
        self.sonido_comprar = pygame.mixer.Sound(resource_path("sonidos/comprar.wav"))

        # --- Accesorios ---
        self.accesorios = {
            "Gorra": {"precio":3, "img":resource_path("imagenes/gorra.png")},
            "Lazo": {"precio":5, "img":resource_path("imagenes/lazo.png")},
            "Cowboy": {"precio":6, "img":resource_path("imagenes/cowboy.png")},
            "Sombrero": {"precio":8, "img":resource_path("imagenes/sombrero.png")},
            "Corona": {"precio":10, "img":resource_path("imagenes/corona.png")}
        }
        self.accesorio_imgs = {n: tk.PhotoImage(file=d["img"]) for n,d in self.accesorios.items()}
        self.corazon_img = tk.PhotoImage(file=resource_path("imagenes/corazon.png"))

        # --- UI ---
        self.score_label = tk.Label(root, text="❤️ 0", font=("Arial",16,"bold"),
                                    fg="#ff6f91", bg="#fff0f5")
        self.score_label.place(x=10, y=10)

        self.tienda_visible = False
        self.tienda_btn = tk.Button(root, text="🛒 Tienda", font=("Arial",12,"bold"),
                                    bg="#ffb6c1", fg="white", command=self.toggle_tienda)
        self.tienda_btn.place(x=10, y=50)

        self.canvas.bind("<Button-1>", self.add_or_wake_duck)
        self.animate()

    def animate_bg(self):
        self.canvas.itemconfig(self.bg_item, image=self.bg_frames[self.bg_index])
        self.bg_index = (self.bg_index + 1) % len(self.bg_frames)
        self.root.after(100, self.animate_bg)

    def toggle_tienda(self):
        if not self.tienda_visible:
            self.tienda_win = tk.Toplevel(self.root)
            self.tienda_win.title("🛒 Tienda de Patitos")
            self.tienda_win.geometry("300x400")
            self.tienda_win.resizable(False, False)
            self.tienda_win.configure(bg="#ffe4e1")

            tk.Label(self.tienda_win, text="🛒 Tienda de Patitos", font=("Comic Sans MS",16,"bold"),
                    bg="#ffe4e1", fg="#ff6f91").pack(pady=8, fill="x")

            for nombre, datos in self.accesorios.items():
                frame = tk.Frame(self.tienda_win, bg="#ffe4e1", pady=4)
                frame.pack(fill="x", padx=5, pady=2)

                original = Image.open(datos["img"])
                resized = original.resize((30,25), Image.Resampling.LANCZOS)
                img = ImageTk.PhotoImage(resized)

                img_label = tk.Label(frame, image=img, bg="#ffe4e1")
                img_label.image = img
                img_label.pack(side="left")

                info = tk.Label(frame, text=f"{nombre}\n{datos['precio']} ❤️", font=("Arial",10), bg="#ffe4e1")
                info.pack(side="left", padx=5)

                btn = tk.Button(frame, text="Comprar", bg="#ffb6c1", fg="white",
                                font=("Arial",10,"bold"),
                                command=lambda n=nombre: self.comprar_y_equipar(n))
                btn.pack(side="right", padx=5)

            self.tienda_win.protocol("WM_DELETE_WINDOW", self.close_tienda)
            self.tienda_visible = True
        else:
            self.close_tienda()

    def close_tienda(self):
        if self.tienda_visible:
            self.tienda_win.destroy()
            self.tienda_visible = False

    def add_or_wake_duck(self, event):
        clicked_items = self.canvas.find_overlapping(event.x-1,event.y-1,event.x+1,event.y+1)
        for item in clicked_items:
            for duck in self.ducks:
                if duck["id"] == item and duck["sleeping"]:
                    duck["sleeping"] = False
                    duck["idle_time"] = 0
                    self.sonido_dormir.play()
                    return
            if "heart" in self.canvas.gettags(item):
                self.collect_heart_on_click(item)
                return
        if len(self.ducks) < MAX_PATOS:
            self.add_duck(event)

    def add_duck(self, event):
        self.sonido_pato.play()
        duck_id = self.canvas.create_image(event.x,event.y,image=self.sprites["right"][0], tags="duck")
        self.ducks.append({
            "id": duck_id,
            "dir_x":1,
            "dir_y":1,
            "frame_index":0,
            "frame_counter":0,
            "sleeping":False,
            "idle_time":0,
            "life_time":500,
            "flying":False,
            "fly_start":0,
            "accesorio":None,
            "speed_x":2
        })

    # --- Animación ---
    def animate(self):
        for duck in self.ducks[:]:
            x, y = self.canvas.coords(duck["id"])

            if not duck["flying"] and random.random() < 0.001:
                duck["flying"] = True
                duck["dir_x"] = random.choice([-1, 1])
                duck["speed_x"] = 4

            if duck["life_time"] <=0 and not duck["flying"]:
                duck["flying"] = True
                duck["dir_x"] = random.choice([-1, 1])
                duck["speed_x"] = 4

            if duck["flying"]:
                if duck["fly_start"] < 6:
                    frames = self.sprites["fly_start_right"] if duck["dir_x"]>0 else self.sprites["fly_start_left"]
                    duck["fly_start"] += 1
                else:
                    frames = self.sprites["fly_right"] if duck["dir_x"]>0 else self.sprites["fly_left"]

                duck["frame_index"] = (duck["frame_index"]+1) % len(frames)
                self.canvas.itemconfig(duck["id"], image=frames[duck["frame_index"]])

                if "acc_id" in duck:
                    self.canvas.delete(duck["acc_id"])
                    duck.pop("acc_id")
                    duck["accesorio"] = None

                self.canvas.move(duck["id"], duck["dir_x"]*duck["speed_x"], 0)

                x, y = self.canvas.coords(duck["id"])
                if x < -50 or x > self.screen_width + 50:
                    self.canvas.delete(duck["id"])
                    self.ducks.remove(duck)

            else:
                self.canvas.move(duck["id"], duck["dir_x"]*0.05, duck["dir_y"]*0.05)
                duck["life_time"] -=1
                duck["idle_time"] +=1
                if duck["idle_time"] > IDLE_LIMIT:
                    duck["sleeping"] = True

                if duck["idle_time"] > IDLE_LIMIT and not duck["sleeping"]:
                    if random.random() < 0.10:
                        duck["sleeping"] = True

                if x<50 or x>self.screen_width-50:
                    duck["dir_x"]*=-1

                # crear corazones solo si no duerme
                if not duck["sleeping"] and random.random() < 0.005:
                    self.create_heart(duck)

                if duck["sleeping"]:
                    frames = self.sprites["sleep_right"][4:9] if duck["dir_x"]>0 else self.sprites["sleep_left"][4:9]
                else:
                    frames = self.sprites["right"] if duck["dir_x"]>0 else self.sprites["left"]

                duck["frame_counter"] += 1
                if duck["frame_counter"] % 2 == 0:
                    duck["frame_index"] = (duck["frame_index"]+1) % len(frames)
                    self.canvas.itemconfig(duck["id"], image=frames[duck["frame_index"]])

                if duck["accesorio"]:
                    if "acc_id" in duck:
                        self.canvas.delete(duck["acc_id"])
                    duck["acc_id"] = self.canvas.create_image(x, y-15, image=duck["accesorio"], tags="accesorio")

        for heart in self.hearts[:]:
            dx = 2*random.random()-1
            dy = -0.7
            self.canvas.move(heart["id"], dx, dy)
            heart["life"] -=1
            if heart["life"]<=0:
                self.canvas.delete(heart["id"])
                self.hearts.remove(heart)

        self.root.after(200, self.animate)

    # --- Corazones ---
    def create_heart(self, duck):
        x, y = self.canvas.coords(duck["id"])
        heart_id = self.canvas.create_image(x, y-25, image=self.corazon_img, tags="heart")
        self.canvas.tag_bind(heart_id,"<Button-1>", lambda e,hid=heart_id: self.collect_heart_on_click(hid))
        self.hearts.append({"id":heart_id,"duck":duck,"life":150})

    def collect_heart_on_click(self, heart_id):
        for heart in self.hearts:
            if heart["id"]==heart_id:
                self.canvas.delete(heart_id)
                self.hearts.remove(heart)
                self.score+=1
                self.score_label.config(text=f"❤️ {self.score}")
                break

    # --- Comprar accesorios ---
    def comprar_y_equipar(self, nombre):
        precio = self.accesorios[nombre]["precio"]
        if self.score >= precio:
            self.score -= precio
            self.score_label.config(text=f"❤️ {self.score}")
            self.sonido_comprar.play()
            normal_ducks = [d for d in self.ducks if not d["flying"]]
            if normal_ducks:
                pato = random.choice(normal_ducks)
                pato["accesorio"] = self.accesorio_imgs[nombre]


if __name__=="__main__":
    root = tk.Tk()
    app = DuckClicker(root)
    root.mainloop()
