import customtkinter
from tkinter import messagebox, ttk
from customtkinter import CTkButton
from PIL import ImageTk, Image
import os
from CTkListbox import *
import pyttsx3
import speech_recognition

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("green")


class TodoApplication(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Task Manager")
        self.geometry("500x450")
        self.resizable(False, False)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "icons")
        self.task_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "task_image_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "task_image_light.png")),
            size=(20, 20))
        self.complete_task_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "complete_image_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "complete_image_light.png")), size=(20, 20))

        self.setting_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "cog_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "cog_light.png")), size=(15, 15))

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=10)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="Task Manager",
                                                             compound="left",
                                                             font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.task_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                   border_spacing=10,
                                                   text="Task",
                                                   fg_color="transparent", text_color=("gray10", "gray90"),
                                                   hover_color=("gray70", "gray30"),
                                                   image=self.task_image, anchor="w",
                                                   command=self.task_button_event)
        self.task_button.grid(row=1, column=0, sticky="ew")

        self.complete_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                       border_spacing=10, text="Completed Task",
                                                       fg_color="transparent", text_color=("gray10", "gray90"),
                                                       hover_color=("gray70", "gray30"),
                                                       image=self.complete_task_image, anchor="w",
                                                       command=self.complete_button_event)
        self.complete_button.grid(row=3, column=0, sticky="ew")

        self.setting_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                      border_spacing=10, text="Setting",
                                                      fg_color="transparent", text_color=("gray10", "gray90"),
                                                      hover_color=("gray70", "gray30"),
                                                      image=self.setting_image, anchor="w",
                                                      command=self.setting_button_event)
        self.setting_button.grid(row=7, column=0, sticky="ew")

        # create all task frame---------------------------------------------------------------------------------
        self.task_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.task_frame.grid_columnconfigure(0, weight=1)

        self.task_frame_label = customtkinter.CTkLabel(self.task_frame, text="INCOMPLETE TASK",
                                                       font=customtkinter.CTkFont(size=12, weight="bold"))
        self.task_frame_label.grid(row=0, columnspan=2, padx=20, pady=10)

        self.task_entry = customtkinter.CTkEntry(self.task_frame, width=300, placeholder_text="Add new Task")
        self.task_entry.grid(row=1, column=0, padx=(20, 0), pady=(20, 20))

        self.add_task_button = customtkinter.CTkButton(self.task_frame, width=5, text="Add Task",
                                                       command=self.add_task)
        self.add_task_button.grid(row=1, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")

        self.listbox = CTkListbox(self.task_frame, width=350, height=150, command=self.mark_as_done)
        self.listbox.grid(row=4, columnspan=2, padx=(20, 20), pady=(20, 0), sticky="nsew")

        self.remove_button = customtkinter.CTkButton(self.task_frame, text="Mark as done", width=400,
                                                     command=self.mark_as_done)
        self.remove_button.grid(row=5, columnspan=2, padx=(20, 20), pady=(20, 0), sticky="nsew")

        self.complete_task_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.complete_task_frame.grid_columnconfigure(0, weight=1)

        self.complete_task_frame_label = customtkinter.CTkLabel(self.complete_task_frame, text="COMPLETED TASK",
                                                                font=customtkinter.CTkFont(size=12, weight="bold"))
        self.complete_task_frame_label.grid(row=0, column=0, padx=20, pady=10)

        self.complete_listbox = CTkListbox(master=self.complete_task_frame, width=350, height=350,
                                           command=self.mark_as_done)
        self.complete_listbox.grid(row=1, columnspan=2, padx=(20, 20), pady=(0, 10), sticky="nsew")

        self.setting_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.setting_frame.grid_columnconfigure(0, weight=1)

        self.setting_frame_label = customtkinter.CTkLabel(self.setting_frame, text="SETTINGS",
                                                          font=customtkinter.CTkFont(size=12, weight="bold"))
        self.setting_frame_label.grid(row=0, column=0, padx=20, pady=10)

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.setting_frame,
                                                                values=["System", "Dark", "Light"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")
        self.select_frame_by_name("task")

        self.current_filter = None

        self.load_todo()

    def speak_male(self, text):
        engine = pyttsx3.init()
        engine.setProperty('rate', 160)
        engine.setProperty('pitch', 100)
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[0].id)

        engine.say(text)
        engine.runAndWait()

    def add_task(self):
        todo = self.task_entry.get()
        if todo == "":
            self.speak_male("Warning, Task cannot be empty!")
            messagebox.showwarning("Warning", "Task cannot be empty!")
            return
        else:
            new_frame = customtkinter.CTkFrame(self.listbox, fg_color="transparent")
            new_frame.grid(sticky="w", pady=5)

            checkbox = customtkinter.CTkCheckBox(new_frame, text=todo, width=5, height=5)
            checkbox.pack(side=customtkinter.RIGHT, anchor=customtkinter.W)

            with open("entry_tasklist.txt", 'a') as taskfile:
                taskfile.write(f"{todo}\n")

            self.task_entry.delete(0, customtkinter.END)

    def mark_as_done(self):
        to_delete = []
        for child in self.listbox.children.values():
            if isinstance(child, customtkinter.CTkFrame):
                for grandchild in child.children.values():
                    if isinstance(grandchild, customtkinter.CTkCheckBox):
                        if grandchild._check_state == True and grandchild._text != "":
                            to_delete.append(child)
                            # print(grandchild._check_state)
                            # print(grandchild._text)

                            # with open("entry_tasklist.txt", "r") as f:
                            #     data = f.readlins()
                            #     print(data)
                            #
                            #     with open("entry_tasklist.txt", "w") as filedata:
                            #         for textline in data:
                            #             if lineindex != grandchild._text:
                            #                 filedata.write(textline)
                            #                 lineindex += 1
                            #
                            # print("Line", grandchild._text, 'is deleted successfully\n')
                            # file = open("entry_tasklist.txt", "r")
                            # for line in file:
                            #     print(line)
                            #
                            # filedata.close()

                            new_frame = customtkinter.CTkFrame(self.complete_listbox, fg_color="transparent")
                            new_frame.grid(sticky="w", pady=5)

                            task_complete_checkbox = customtkinter.CTkCheckBox(new_frame, text=grandchild._text,
                                                                               width=5, height=5)
                            task_complete_checkbox.pack(side=customtkinter.RIGHT, anchor=customtkinter.W)
                            task_complete_checkbox.select()
                            task_complete_checkbox.configure(state="disabled")

                            with open("completed_tasklist.txt", 'a') as taskfile:
                                taskfile.write(f"{grandchild._text}\n")

        for i in range(0, len(to_delete)):
            to_delete[i].destroy()

    def load_todo(self):

        file = open("entry_tasklist.txt", "r")
        record_num = 1
        while True:
            record = file.readline()
            if record == "":
                file.close()
                break

            record = record.strip()

            if record_num == 1:
                # print(record)
                new_frame = customtkinter.CTkFrame(self.listbox, fg_color="transparent")
                new_frame.grid(sticky="w", pady=5)

                checkbox = customtkinter.CTkCheckBox(new_frame, text=record, width=5, height=5)
                checkbox.pack(side=customtkinter.RIGHT, anchor=customtkinter.W)
        file.close()

        deleted_file = open("completed_tasklist.txt", "r")
        deleted_record_num = 1
        while True:
            deleted_record = deleted_file.readline()
            if deleted_record == "":
                deleted_file.close()
                break

            deleted_record = deleted_record.strip()

            if deleted_record_num == 1:
                # print(record)
                deleted_new_frame = customtkinter.CTkFrame(self.complete_listbox, fg_color="transparent")
                deleted_new_frame.grid(sticky="w", pady=5)

                task_complete_checkbox = customtkinter.CTkCheckBox(deleted_new_frame, text=deleted_record, width=5,
                                                                   height=5)
                task_complete_checkbox.pack(side=customtkinter.RIGHT, anchor=customtkinter.W)
                task_complete_checkbox.select()
                task_complete_checkbox.configure(state="disabled")

        deleted_file.close()

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def task_button_event(self):
        self.select_frame_by_name("task")

    def complete_button_event(self):
        self.select_frame_by_name("complete_task")

    def setting_button_event(self):
        self.select_frame_by_name("setting")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.task_button.configure(fg_color=("gray75", "gray25") if name == "task" else "transparent")
        self.complete_button.configure(fg_color=("gray75", "gray25") if name == "complete_task" else "transparent")
        self.setting_button.configure(fg_color=("gray75", "gray25") if name == "setting" else "transparent")

        # show selected frame
        if name == "task":
            self.task_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.task_frame.grid_forget()
        if name == "complete_task":
            self.complete_task_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.complete_task_frame.grid_forget()

        if name == "setting":
            self.setting_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.setting_frame.grid_forget()


if __name__ == "__main__":
    root = TodoApplication()
    root.mainloop()
