from tkinter import *
from tkinter import Tk, Label, Button, Entry, IntVar, END, W, E, filedialog, messagebox
from tkinter.messagebox import showerror

from PIL import ImageTk, Image

from KMeansClustering import KMeansClustering


class Main:

    def __init__(self, master):
        # master is the root
        self.master = master
        self.master.title("K Means Clustering")
        self.master.minsize(width=800, height=600)
        self.master.maxsize(width=800, height=600)

        # path file
        self.path_text = StringVar()
        self.path_label = Label(master, text="file path:")
        self.path_entry = Entry(master, textvariable=self.path_text)
        self.file_path_btn = self.path_btn = Button(master, text="Browse",
                                                    command=lambda: self.open_file_dialog(self.path_text))
        # check if the user didnt gave a bad path!

        # number of cluster k
        self.number_k_cluster = IntVar()
        self.k_cluster_label = Label(master, text="Number of clusters k")
        self.k_cluster_entry = Entry(master, textvariable=self.number_k_cluster)

        # number of runs
        self.runs_number_cluster = IntVar()
        self.runs_number_label = Label(master, text="Number of runs")
        self.runs_number_entry = Entry(master, textvariable=self.runs_number_cluster)

        self.per_process_btn = Button(master, text="Pre-process", command=lambda: self.start_pre_process())
        self.cluster_btn = Button(master, text="Cluster", command=lambda: self.start_clustering())

        # Grid
        self.path_label.grid(row=0, column=0, sticky=W)
        self.path_entry.grid(row=0, column=1, columnspan=2)
        self.path_btn.grid(row=0, column=3)

        self.k_cluster_label.grid(row=1, column=0)
        self.k_cluster_entry.grid(row=1, column=1)

        self.runs_number_label.grid(row=2, column=0)
        self.runs_number_entry.grid(row=2, column=1)

        self.per_process_btn.grid(row=3, column=1, columnspan=2)
        self.cluster_btn.grid(row=4, column=1, columnspan=2)

        # self.canvas = Canvas(master, width=600, height=400, background='white')
        # self.canvas.grid(row=5, column=1)

        self.file_path = ''
        self.k_means_clustering = ''
        self.k_cluster = 0
        self.run_number = 0

    def open_file_dialog(self, path_entry_text):
        self.file_path = filedialog.askopenfilename(title="K Means Clustering", filetypes=[("Excel files", "*.xlsx")])
        path_entry_text.set(self.file_path)
        self.k_means_clustering = KMeansClustering(self.file_path)

    def start_pre_process(self):
        try:
            if self.file_path == '':
                raise ValueError
            elif self.k_means_clustering.check_file() == 'bad input':
                raise TypeError

            # pre process here!
            # when done!
            if self.k_means_clustering.pre_processing() == 'done':
                messagebox.showinfo(title="K Means Clustering", message="Preprocessing completed successfully!")

        except TypeError:
            showerror("K Means Clustering",
                      message=str("Bad input, please make sure your file contains the correct data"))
        except ValueError:
            showerror("K Means Clustering",
                      message=str("Please load an excel file to continue"))
            pass
        except:
            # error - not int
            showerror("K Means Clustering", message=str("Please enter and integer at Number of clusters k or Number "
                                                        "of runs"))

    def start_clustering(self):
        try:
            self.k_cluster = self.number_k_cluster.get()
            self.run_number = self.runs_number_cluster.get()

            if self.k_cluster < 2 or self.run_number < 1 or self.run_number > 100:
                # maybe add max of k
                raise ValueError
            self.photo1_path, self.photo2_path = self.k_means_clustering.kmeans(self.k_cluster, self.run_number)
            messagebox.showinfo(title="K Means Clustering", message="Clustering completed successfully!")
            image1 = Image.open(self.photo1_path)
            image2 = Image.open(self.photo2_path)
            self.photo1 = ImageTk.PhotoImage(image1)
            self.photo2 = ImageTk.PhotoImage(image2)
            self.photo1_label = Label(root, image=self.photo1)
            self.photo2_label = Label(root, image=self.photo2)
            # self.canvas.create_image(image=self.photo1, anchor=NW)
            self.photo1_label.grid(row=5, column=0, sticky=E)
            self.photo2_label.grid(row=5, column=1, sticky=W)
        except ValueError:
            showerror("K Means Clustering", message=str("Please enter valid numbers in Number of clusters k or Number"
                                                        "of runs"))
        except:
            # error - not int
            showerror("K Means Clustering", message=str("Clustering not completed successfully!"))


root = Tk()
my_gui = Main(root)
root.geometry("800x600")
root.mainloop()
