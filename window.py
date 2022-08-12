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
        self.image_preview.grid(row=0, columnspan=5)

        self.button_generate = tk.Button(self.frame, text="Generate", command=self.onGenerate)
        self.button_generate.grid(row=1, column=0, sticky=tk.W)

        self.progress_bar = Progressbar(self.frame, mode='indeterminate')
        self.progress_bar.grid(row=1, column=1, columnspan=3)
        self.progress_bar.grid_remove()

        self.button_save = tk.Button(self.frame, text="Save To PNG", command=self.onSave)
        self.button_save.grid(row=1, column=4, sticky=tk.E)

        self.root.mainloop()

    def onSave(self):
        if self.current_image_PIL:
            filename = asksaveasfilename(filetypes = [('PNG', '*.png')], defaultextension= [('PNG', '*.png')])
            if filename:
                self.current_image_PIL.save(filename)

    def updatePreview(self, new_image):
        self.progress_bar.stop()
        self.progress_bar.grid_remove()
        self.current_image_PIL = new_image
        self.current_image = ImageTk.PhotoImage(new_image)
        self.image_preview.itemconfig(self._canvas_image, image=self.current_image)

    def onGenerate(self):
        if not self.generate_thread._is_stopped:
            print("Generate")
            self.progress_bar.grid()
            self.progress_bar.start()
            self.generate_thread.restart()
            # self.generate_thread.run()