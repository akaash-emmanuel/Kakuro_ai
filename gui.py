import tkinter as tk
from tkinter import filedialog, messagebox
from extractSequences import extractSequences
from kakuroSolver import kakuroSolver



class KakuroGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Kakuro Puzzle Solver")

        # Set window size and background color
        self.root.geometry("600x700")
        self.root.config(bg="#e3f2fd")

        # Title label
        self.title_label = tk.Label(root, text="Kakuro Puzzle Solver", font=("Helvetica", 20, "bold"), bg="#e3f2fd",
                                    fg="#1976D2")
        self.title_label.pack(pady=20)

        # Main Frame (to organize all widgets)
        self.main_frame = tk.Frame(root, bg="#e3f2fd")
        self.main_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Puzzle Load Section
        self.load_frame = tk.Frame(self.main_frame, bg="#e3f2fd")
        self.load_frame.pack(pady=10, fill="x")

        # File selection button
        self.select_file_button = tk.Button(self.load_frame, text="Select Puzzle File", font=("Arial", 12),
                                            command=self.select_file,
                                            relief="raised", bg="#4CAF50", fg="white", padx=10, pady=5)
        self.select_file_button.grid(row=0, column=0, padx=10)

        # Solve button
        self.solve_button = tk.Button(self.load_frame, text="Solve Puzzle", font=("Arial", 12),
                                      command=self.solve_puzzle,
                                      relief="raised", bg="#2196F3", fg="white", padx=10, pady=5)
        self.solve_button.grid(row=0, column=1, padx=10)

        # Puzzle Grid Section
        self.grid_frame = tk.Frame(self.main_frame, bg="#e3f2fd")
        self.grid_frame.pack(fill="both", expand=True)

        # Solution Status Label
        self.solution_label = tk.Label(root, text="", font=("Arial", 14, "bold"), bg="#e3f2fd")
        self.solution_label.pack(pady=10)

        # Status Bar
        self.status_bar = tk.Label(root, text="Ready", font=("Arial", 10), bg="#2196F3", fg="white", anchor="w",
                                   padx=10)
        self.status_bar.pack(side="bottom", fill="x", pady=5)

        self.input_file = None
        self.puzzle = None

    def select_file(self):
        """Open file dialog to select a puzzle input file"""
        self.input_file = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if self.input_file:
            self.load_puzzle()

    def load_puzzle(self):
        """Load the puzzle into the grid for display"""
        try:
            self.status_bar.config(text="Loading puzzle...")
            self.puzzle = extractSequences(self.input_file)

            # Clear the existing grid
            for widget in self.grid_frame.winfo_children():
                widget.destroy()

            # Create a grid of Entry widgets to represent the puzzle
            self.entries = []
            for r in range(self.puzzle.rows):
                row_entries = []
                for c in range(self.puzzle.columns):
                    entry = tk.Entry(self.grid_frame, width=5, font=("Arial", 14), justify="center",
                                     relief="solid", bd=2, highlightthickness=1)
                    entry.grid(row=r, column=c, padx=5, pady=5, sticky="nsew")
                    row_entries.append(entry)
                self.entries.append(row_entries)

            # Make the grid resizeable
            for r in range(self.puzzle.rows):
                self.grid_frame.grid_rowconfigure(r, weight=1)
            for c in range(self.puzzle.columns):
                self.grid_frame.grid_columnconfigure(c, weight=1)

            self.status_bar.config(text="Puzzle loaded successfully!")
        except Exception as e:
            self.status_bar.config(text="Error loading puzzle.")
            messagebox.showerror("Error", f"Failed to load puzzle: {str(e)}")

    def solve_puzzle(self):
        """Solve the Kakuro puzzle and update the GUI with the solution"""
        try:
            if self.puzzle is None:
                raise ValueError("Please load a puzzle file first.")

            self.status_bar.config(text="Solving puzzle...")
            # Get the solution from kakuroSolver
            solver = kakuroSolver(self.puzzle.rows, self.puzzle.columns, self.puzzle.coordsToHorizontalSequenceDict,
                                  self.puzzle.coordsToVerticalSequenceDict)
            solver.getSolution()

            # Display the solution in the GUI
            self.display_solution(solver.kakuroBoard)

        except Exception as e:
            self.status_bar.config(text="Error solving puzzle.")
            messagebox.showerror("Error", f"Failed to solve the puzzle: {str(e)}")

    def display_solution(self, solution):
        """Display the solved puzzle on the grid"""
        for r in range(self.puzzle.rows):
            for c in range(self.puzzle.columns):
                value = solution[r][c]
                entry = self.entries[r][c]
                if value == -1:
                    entry.delete(0, tk.END)
                    entry.insert(0, "#")
                    entry.config(bg="#FFCDD2")  # Red for unsolved cells
                else:
                    entry.delete(0, tk.END)
                    entry.insert(0, str(value))
                    entry.config(bg="#C8E6C9")  # Light Green for solved cells

        self.solution_label.config(text="Puzzle Solved!", fg="green")
        self.status_bar.config(text="Puzzle solved successfully!")


if __name__ == "__main__":
    root = tk.Tk()
    app = KakuroGUI(root)
    root.mainloop()
