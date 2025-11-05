import tkinter as tk
import time
import random

import sys, os

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and PyInstaller"""
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

class Pet:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()

        def load_gif_frames(path, zoom_x=2, zoom_y=2):
            frames = []
            i = 0
            while True:
                try:
                    frame = tk.PhotoImage(file=path, format=f'gif -index {i}').zoom(zoom_x, zoom_y)
                    frames.append(frame)
                    i += 1
                except tk.TclError:
                    break
            return frames

        # Chione (walk/sit/tuna)
        self.chione_walk_right = load_gif_frames(resource_path('astre_chio/chione_walking_right.gif'))
        self.chione_walk_left = load_gif_frames(resource_path('astre_chio/chione_walking_left.gif'))
        self.chione_sit_right = load_gif_frames(resource_path('astre_chio/chione_sit_right.gif'))
        self.chione_sit_left = load_gif_frames(resource_path('astre_chio/chione_sit_left.gif'))
        self.chione_tuna_right = load_gif_frames(resource_path('astre_chio/chione_tuna_right.gif'))
        self.chione_tuna_left = load_gif_frames(resource_path('astre_chio/chione_tuna_left.gif'))
        self.chione_dancing = load_gif_frames(resource_path('astre_chio/chione_dancing.gif'))

        # Astre (run/sleep/nyancat)
        self.astre_run_right = load_gif_frames(resource_path('astre_chio/astre_walking_right.gif'))
        self.astre_run_left = load_gif_frames(resource_path('astre_chio/astre_walking_left.gif'))
        self.astre_sit_right = load_gif_frames(resource_path('astre_chio/astre_sit_right.gif'))
        self.astre_sit_left = load_gif_frames(resource_path('astre_chio/astre_sit_left.gif'))
        self.astre_sleep_right = load_gif_frames(resource_path('astre_chio/astre_sleeping_right.gif'))
        self.astre_sleep_left = load_gif_frames(resource_path('astre_chio/astre_sleeping_left.gif'))
        self.astre_nyancat_right = load_gif_frames(resource_path('astre_chio/astre_nyancat_right.gif'))
        self.astre_nyancat_left = load_gif_frames(resource_path('astre_chio/astre_nyancat_left.gif'))

        # --- Create windows ---
        self.chione = self.create_pet_window(self.chione_walk_right[0])
        self.astre = self.create_pet_window(self.astre_run_left[0])

        # --- Position setup ---
        screen_w = self.chione.winfo_screenwidth()
        screen_h = self.chione.winfo_screenheight()
        taskbar_height = 35
        pet_h = 100

        # Chione setup
        self.chione_x = 0
        self.chione_y = screen_h - pet_h - taskbar_height
        self.chione_dir = 1
        self.chione_state = "walk"

        # Astre setup
        self.astre_x = screen_w - 100
        self.astre_y = screen_h - pet_h - taskbar_height
        self.astre_dir = -1
        self.astre_state = "run"

        # --- Animation control ---
        self.chione_frame = 0
        self.astre_frame = 0
        self.chione_timestamp = time.time()
        self.astre_timestamp = time.time()

        # --- Start updates ---
        self.update()
        self.root.bind_all("<Escape>", self.exit_program)
        self.root.mainloop()
    
    def exit_program(self, event=None):
        try:
            self.chione.destroy()
            self.astre.destroy()
        except Exception:
            pass
        self.root.destroy()
        sys.exit()

    def create_pet_window(self, img):
        win = tk.Toplevel()
        win.overrideredirect(True)
        win.attributes('-topmost', True)
        win.wm_attributes('-transparentcolor', 'black')
        label = tk.Label(win, bd=0, bg='black', image=img)
        label.pack()
        win.label = label
        return win

    def update(self):
        current_time = time.time()
        screen_w = self.chione.winfo_screenwidth()

        # ===== CHIONE BEHAVIOR =====
        if self.chione_state == "walk":
            speed = random.uniform(0.12, 0.3)
            self.chione_x += self.chione_dir * speed

            if self.chione_x <= 0:
                self.chione_dir = 1
            elif self.chione_x >= screen_w - 100:
                self.chione_dir = -1

            if current_time > self.chione_timestamp + 0.25:
                self.chione_timestamp = current_time
                self.chione_frame = (self.chione_frame + 1) % len(self.chione_walk_right)
                img = (self.chione_walk_right if self.chione_dir == 1 else self.chione_walk_left)[self.chione_frame]
                self.chione.label.configure(image=img)
                self.chione.label.image = img

            if random.randint(1, 3000) == 1:
                self.chione_state = "sit"
                self.chione_frame = 0
                self.chione_timestamp = current_time
            
            if random.randint(1, 5000) == 1:
                self.chione_state = "tuna"
                self.chione_frame = 0
                self.chione_timestamp = current_time

            if random.randint(1, 6000) == 1:
                self.chione_state = "dance"
                self.chione_frame = 0
                self.chione_dance_start_time = current_time
                self.chione_timestamp = current_time

        elif self.chione_state == "sit":
            if current_time > self.chione_timestamp + 0.5:
                self.chione_timestamp = current_time
                if self.chione_dir == 1:
                    self.chione_frame = (self.chione_frame + 1) % len(self.chione_sit_right)
                    img = self.chione_sit_right[self.chione_frame]
                else:
                    self.chione_frame = (self.chione_frame + 1) % len(self.chione_sit_left)
                    img = self.chione_sit_left[self.chione_frame]
                self.chione.label.configure(image=img)
                self.chione.label.image = img

                if (
                    (self.chione_dir == 1 and self.chione_frame == len(self.chione_sit_right) - 1)
                    or (self.chione_dir == -1 and self.chione_frame == len(self.chione_sit_left) - 1)
                ) and random.randint(1, 2) == 1:
                    self.chione_state = "walk"
                    self.chione_frame = 0
                    self.chione_timestamp = current_time

        elif self.chione_state == "tuna":
            tuna_frame_delay = 0.5 

            if current_time > self.chione_timestamp + tuna_frame_delay:
                self.chione_timestamp = current_time
                if self.chione_dir == 1:
                    self.chione_frame = (self.chione_frame + 1) % len(self.chione_tuna_right)
                    img = self.chione_tuna_right[self.chione_frame]
                else:
                    self.chione_frame = (self.chione_frame + 1) % len(self.chione_tuna_left)
                    img = self.chione_tuna_left[self.chione_frame]
                self.chione.label.configure(image=img)
                self.chione.label.image = img

                if (
                    (self.chione_dir == 1 and self.chione_frame == len(self.chione_tuna_right) - 1)
                    or (self.chione_dir == -1 and self.chione_frame == len(self.chione_tuna_left) - 1)
                ):
                    self.chione_state = "walk"
                    self.chione_frame = 0
                    self.chione_timestamp = current_time
        
        elif self.chione_state == "dance":
            dance_frame_delay = 0.5
            dance_duration = 6.0  

            if len(self.chione_dancing) > 0 and current_time > self.chione_timestamp + dance_frame_delay:
                self.chione_timestamp = current_time
                self.chione_frame = (self.chione_frame + 1) % len(self.chione_dancing)
                img = self.chione_dancing[self.chione_frame]
                self.chione.label.configure(image=img)
                self.chione.label.image = img

            if hasattr(self, 'chione_dance_start_time') and current_time > self.chione_dance_start_time + dance_duration:
                self.chione_state = "walk"
                self.chione_frame = 0
                self.chione_timestamp = current_time
                try:
                    del self.chione_dance_start_time
                except Exception:
                    pass

        self.chione.geometry(f'100x100+{int(self.chione_x)}+{int(self.chione_y)}')

        # ===== ASTRE BEHAVIOR =====
        speed = random.uniform(0.4, 0.9)
        run_frame_delay = random.uniform(0.08, 0.15)
        sleep_frame_delay = 0.5 

        if self.astre_state == "run":
            self.astre_x += self.astre_dir * speed
            if self.astre_x <= 0:
                self.astre_dir = 1
            elif self.astre_x >= screen_w - 100:
                self.astre_dir = -1

            if current_time > self.astre_timestamp + run_frame_delay:
                self.astre_timestamp = current_time
                self.astre_frame = (self.astre_frame + 1) % len(self.astre_run_right)
                img = (self.astre_run_right if self.astre_dir == 1 else self.astre_run_left)[self.astre_frame]
                self.astre.label.configure(image=img)
                self.astre.label.image = img

            if random.randint(1, 2500) == 1:
                self.astre_state = "sleep"
                self.astre_frame = 0
                self.astre_timestamp = current_time
            
            if random.randint(1, 3000) == 1:
                self.astre_state = "sit"
                self.astre_frame = 0
                self.astre_timestamp = current_time
            
            if random.randint(1, 4000) == 1:
                self.astre_state = "nyancat"
                self.astre_frame = 0
                self.astre_timestamp = current_time

        elif self.astre_state == "sleep":
            if current_time > self.astre_timestamp + sleep_frame_delay:
                self.astre_timestamp = current_time
                if self.astre_dir == 1:
                    self.astre_frame = (self.astre_frame + 1) % len(self.astre_sleep_right)
                    img = self.astre_sleep_right[self.astre_frame]
                else:
                    self.astre_frame = (self.astre_frame + 1) % len(self.astre_sleep_left)
                    img = self.astre_sleep_left[self.astre_frame]
                self.astre.label.configure(image=img)
                self.astre.label.image = img

                if self.astre_frame == len(self.astre_sleep_right) - 1 and random.randint(1, 3) == 1:
                    self.astre_state = "run"
                    self.astre_frame = 0
                    self.astre_timestamp = current_time
        
        elif self.astre_state == "sit":
            if current_time > self.astre_timestamp + 0.5:
                self.astre_timestamp = current_time
                if self.astre_dir == 1:
                    self.astre_frame = (self.astre_frame + 1) % len(self.astre_sit_right)
                    img = self.astre_sit_right[self.astre_frame]
                else:
                    self.astre_frame = (self.astre_frame + 1) % len(self.astre_sit_left)
                    img = self.astre_sit_left[self.astre_frame]
                self.astre.label.configure(image=img)
                self.astre.label.image = img

                if (
                    (self.astre_dir == 1 and self.astre_frame == len(self.astre_sit_right) - 1)
                    or (self.astre_dir == -1 and self.astre_frame == len(self.astre_sit_left) - 1)
                ) and random.randint(1, 2) == 1:
                    self.astre_state = "run"
                    self.astre_frame = 0
                    self.astre_timestamp = current_time
        
        elif self.astre_state == "nyancat":
            nyancat_frame_delay = 0.5  

            if current_time > self.astre_timestamp + nyancat_frame_delay:
                self.astre_timestamp = current_time
                if self.astre_dir == 1:
                    self.astre_frame = (self.astre_frame + 1) % len(self.astre_nyancat_right)
                    img = self.astre_nyancat_right[self.astre_frame]
                else:
                    self.astre_frame = (self.astre_frame + 1) % len(self.astre_nyancat_left)
                    img = self.astre_nyancat_left[self.astre_frame]
                self.astre.label.configure(image=img)
                self.astre.label.image = img

                if (
                    (self.astre_dir == 1 and self.astre_frame == len(self.astre_nyancat_right) - 1)
                    or (self.astre_dir == -1 and self.astre_frame == len(self.astre_nyancat_left) - 1)
                ):
                    self.astre_state = "run"
                    self.astre_frame = 0
                    self.astre_timestamp = current_time

        self.astre.geometry(f'100x100+{int(self.astre_x)}+{int(self.astre_y)}')
        self.root.after(10, self.update)

Pet()