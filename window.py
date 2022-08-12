import tkinter as tk
from tkinter.ttk import Progressbar
from tkinter.filedialog import asksaveasfilename
from PIL import ImageTk, Image
from threading import Thread
from rthread import ReusableThread

class MainWindow(Thread):
    def __init__(self, generate):
        Thread.__init__(self, name="GUI")
        # self.start()
        self.generate = generate
        self.current_image_PIL = None
        self.generate_thread = None

        self.generate_thread = ReusableThread(target=self.generate, args=[self.updatePreview])
        self.generate_thread.daemon = True
        self.generate_thread.start()

    def onDelete(self):
        self.root.quit()

    def run(self):
        self.root = tk.Tk()
        self.root.title("BiomeGenerator")
        self.root.protocol("WM_DELETE_WINDOW", self.onDelete)

        self.frame = tk.Frame(self.root, width=800,height=640)
        self.frame.pack(expand=True, fill=tk.BOTH)

        self.image_preview = tk.Canvas(self.frame, bg='white', width=640, height=640)
        self._canvas_image = self.image_preview.create_image(0,0, anchor=tk.NW)
        self.image_preview.grid(row=0, columnspan=5, rowspan=3)

        self.image_red_preview = tk.Canvas(self.frame, bg='red', width=210, height=210)
        self._red_noise_image = self.image_red_preview.create_image(0,0, anchor=tk.NW)
        self.image_red_preview.grid(row=0, column=6)

        self.image_green_preview = tk.Canvas(self.frame, bg='green', width=210, height=210)
        self._green_noise_image = self.image_green_preview.create_image(0,0, anchor=tk.NW)
        self.image_green_preview.grid(row=1, column=6)

        self.image_blue_preview = tk.Canvas(self.frame, bg='blue', width=210, height=210)
        self._blue_noise_image = self.image_blue_preview.create_image(0,0, anchor=tk.NW)
        self.image_blue_preview.grid(row=2, column=6)

        self.button_generate = tk.Button(self.frame, text="Generate", command=self.onGenerate)
        self.button_generate.grid(row=3, column=0, sticky=tk.W)

        self.progress_bar = Progressbar(self.frame, mode='indeterminate')
        self.progress_bar.grid(row=3, column=1, columnspan=5)
        self.progress_bar.grid_remove()

        self.button_save = tk.Button(self.frame, text="Save To PNG", command=self.onSave)
        self.button_save.grid(row=3, column=6, sticky=tk.E)

        self.root.mainloop()

    def onSave(self):
        if self.current_image_PIL:
            filename = asksaveasfilename(filetypes = [('PNG', '*.png')], defaultextension= [('PNG', '*.png')])
            if filename:
                self.current_image_PIL.save(filename)

    def updatePreview(self, new_image: Image.Image):
        self.progress_bar.stop()
        self.progress_bar.grid_remove()
        self.current_image_PIL = new_image
        self.current_image = ImageTk.PhotoImage(new_image)
        self.current_red_image = ImageTk.PhotoImage(new_image.getchannel("R").resize((210,210), Image.ANTIALIAS))
        self.current_green_image = ImageTk.PhotoImage(new_image.getchannel("G").resize((210,210), Image.ANTIALIAS))
        self.current_blue_image = ImageTk.PhotoImage(new_image.getchannel("B").resize((210,210), Image.ANTIALIAS))
        self.image_preview.itemconfig(self._canvas_image, image=self.current_image)
        self.image_red_preview.itemconfig(self._red_noise_image, image=self.current_red_image)
        self.image_green_preview.itemconfig(self._green_noise_image, image=self.current_green_image)
        self.image_blue_preview.itemconfig(self._blue_noise_image, image=self.current_blue_image)

    def onGenerate(self):
        if not self.generate_thread._is_stopped:
            print("Generate")
            self.progress_bar.grid()
            self.progress_bar.start()
            self.generate_thread.restart()
            # self.generate_thread.run()