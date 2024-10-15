import customtkinter as ctk
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class RubikApp:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        self.root = ctk.CTk()
        self.root.geometry("1200x600+200+100")
        self.root.title("Rubik's Cube Timer - Matrix Style")
        self.root.update()

        # Kolory
        self.green = "#00FF00"
        self.black = "#0A0A0A"
        self.font = ("Helvetica", 18)  # Zwiększona czcionka

        # Zmienna na czasy i liczba prób
        self.times = []
        self.max_trials = 0
        self.current_trial = 0

        # Główna ramka na wykres
        self.frame = ctk.CTkFrame(master=self.root, height=self.root.winfo_height() * 0.75, width=self.root.winfo_width() * 0.66, fg_color=self.black)
        self.frame.place(relx=0.33, rely=0.025)

        # Pole na wpisanie liczby prób
        self.trial_label = ctk.CTkLabel(master=self.root, text="Number of Trials:", text_color=self.green, font=self.font)
        self.trial_label.place(relx=0.025, rely=0.05)
        self.trial_input = ctk.CTkEntry(master=self.root, placeholder_text="Enter number of trials", justify='center', width=300, height=50, fg_color=self.black, text_color=self.green, font=self.font)
        self.trial_input.place(relx=0.025, rely=0.12)

        # Przycisk do rozpoczęcia prób (przeniesiony pod pole liczby prób)
        self.start_button = ctk.CTkButton(master=self.root, text="Start Trials", width=300, height=50, command=self.start_trials, fg_color=self.green, text_color=self.black, font=self.font)
        self.start_button.place(relx=0.025, rely=0.22)

        # Wyświetlanie scramblera
        self.scrambler_label = ctk.CTkLabel(master=self.root, text="Scrambler:", text_color=self.green, font=self.font)
        self.scrambler_label.place(relx=0.025, rely=0.32)
        self.scrambler_display = ctk.CTkEntry(master=self.root, justify='center', width=300, height=50, fg_color=self.black, text_color=self.green, state="readonly", font=self.font)
        self.scrambler_display.place(relx=0.025, rely=0.37)

        # Pole na wpisanie czasu
        self.time_label = ctk.CTkLabel(master=self.root, text="Enter your time (seconds):", text_color=self.green, font=self.font)
        self.time_label.place(relx=0.025, rely=0.48)
        self.time_input = ctk.CTkEntry(master=self.root, placeholder_text="Enter time", justify='center', width=150, height=50, fg_color=self.black, text_color=self.green, font=self.font)
        self.time_input.place(relx=0.025, rely=0.53)

        # Przycisk do zatwierdzania czasu
        self.submit_button = ctk.CTkButton(master=self.root, text="Submit Time", width=150, height=50, command=self.submit_time, state="disabled", fg_color=self.green, text_color=self.black, font=self.font)
        self.submit_button.place(relx=0.18, rely=0.53)

        # Pola na wyświetlanie statystyk (średni czas, najlepszy czas, najgorszy czas)
        self.best_time_label = ctk.CTkLabel(master=self.root, text="Best Time: N/A", text_color=self.green, font=self.font)
        self.best_time_label.place(relx=0.025, rely=0.7)
        self.avg_time_label = ctk.CTkLabel(master=self.root, text="Average Time: N/A", text_color=self.green, font=self.font)
        self.avg_time_label.place(relx=0.025, rely=0.75)
        self.worst_time_label = ctk.CTkLabel(master=self.root, text="Worst Time: N/A", text_color=self.green, font=self.font)
        self.worst_time_label.place(relx=0.025, rely=0.8)

        self.root.mainloop()

    def generate_scrambler(self):
        moves = ['U', 'D', 'L', 'R', 'F', 'B']
        modifiers = ['', "'", '2']
        scramble = [random.choice(moves) + random.choice(modifiers) for _ in range(10)]
        return ' '.join(scramble)

    def start_trials(self):
        try:
            self.max_trials = int(self.trial_input.get())
            self.current_trial = 0
            self.times = []
            self.scrambler_display.configure(state="normal")
            self.scrambler_display.delete(0, 'end')
            self.scrambler_display.insert(0, self.generate_scrambler())
            self.scrambler_display.configure(state="readonly")
            self.submit_button.configure(state="normal")
            self.start_button.configure(state="disabled")
        except ValueError:
            print("Please enter a valid number of trials.")

    def submit_time(self):
        try:
            time = float(self.time_input.get())
            self.times.append(time)
            self.time_input.delete(0, 'end')
            self.current_trial += 1
            if self.current_trial < self.max_trials:
                # Generowanie nowego scramblera
                self.scrambler_display.configure(state="normal")
                self.scrambler_display.delete(0, 'end')
                self.scrambler_display.insert(0, self.generate_scrambler())
                self.scrambler_display.configure(state="readonly")
            else:
                self.submit_button.configure(state="disabled")
                self.start_button.configure(state="normal")
            self.update_results()
            self.update_graph()
        except ValueError:
            print("Please enter a valid time.")

    def update_results(self):
        # Aktualizacja statystyk
        best_time = min(self.times)
        worst_time = max(self.times)
        avg_time = sum(self.times) / len(self.times)

        self.best_time_label.configure(text=f"Best Time: {best_time:.0f}s")
        self.avg_time_label.configure(text=f"Average Time: {avg_time:.0f}s")
        self.worst_time_label.configure(text=f"Worst Time: {worst_time:.0f}s")

    def update_graph(self):
        # Rysowanie wykresu
        fig, ax = plt.subplots()
        fig.set_size_inches(11, 5.3)
        trials = np.arange(1, len(self.times) + 1)
        ax.plot(trials, self.times, marker='o', color=self.green)
        ax.set_title('Rubik\'s Cube Times', color=self.green, fontsize=18)
        ax.set_xlabel('Trial Number', color=self.green, fontsize=16)
        ax.set_ylabel('Time (seconds)', color=self.green, fontsize=16)

        # Siatka z cienkimi liniami
        ax.grid(True, color=self.green, linewidth=0.3)  # Zmieniona grubość linii siatki na bardzo cienką

        # Ustawienia dla osi
        ax.tick_params(colors=self.green)
        ax.set_xticks(trials)  # Pokazuj liczby całkowite na osi X
        ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))  # Usunięcie wartości z przecinkiem na osi Y
        ax.spines['bottom'].set_color(self.green)
        ax.spines['top'].set_color(self.green)
        ax.spines['left'].set_color(self.green)
        ax.spines['right'].set_color(self.green)

        # Ustawienia kolorów tła
        ax.set_facecolor(self.black)  # Tło samego wykresu (obszar rysowania)
        fig.patch.set_facecolor(self.black)  # Tło całej figury (tło za wykresem)

        # Wyświetlenie wykresu na tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas.draw()
        canvas.get_tk_widget().place(relx=0.33, rely=0.025)


if __name__ == "__main__":
    RubikApp()
