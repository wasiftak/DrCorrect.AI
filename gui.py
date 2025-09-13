import tkinter as tk
from tkinter import scrolledtext, messagebox
from text_processor import MedicalTextProcessor

class DrCorrectApp(tk.Tk):
    """The main GUI class for the application."""
    def __init__(self):
        super().__init__()
        self.processor = MedicalTextProcessor()
        self.title("DrCorrect.AI - Clinical Notes Assistant")
        self.geometry("1000x700")

        main_frame = tk.Frame(self)
        main_frame.pack(expand=True, fill='both', padx=10, pady=10)

        editor_frame = tk.Frame(main_frame)
        editor_frame.pack(side='left', expand=True, fill='both', padx=(0, 5))
        
        editor_label = tk.Label(editor_frame, text="Clinical Notes", font=("Arial", 12, "bold"))
        editor_label.pack(anchor='w')
        
        self.text_widget = scrolledtext.ScrolledText(editor_frame, wrap=tk.WORD, font=("Arial", 12), undo=True)
        self.text_widget.pack(expand=True, fill='both')
        
        self.suggestion_listbox = tk.Listbox(self, font=("Arial", 10), height=5)

        self._bind_events()
        self.load_default_corpus()

    def _bind_events(self):
        """Binds all necessary events to their handler methods."""
        self.text_widget.bind("<space>", self._on_space_press)
        self.text_widget.bind("<KeyRelease>", self._on_key_release)
        self.text_widget.bind("<Tab>", self._accept_suggestion)
        self.suggestion_listbox.bind("<Double-1>", self._accept_suggestion)
        self.text_widget.bind("<FocusOut>", lambda e: self.suggestion_listbox.place_forget())

    def load_default_corpus(self):
        """Loads the vocabulary from the processed text file."""
        success, count = self.processor.load_corpus_from_txt('medical_vocabulary.txt')
        if not success:
            messagebox.showerror("Vocabulary Error", "Could not find or load 'medical_vocabulary.txt'. Please run the 'build_corpus.py' script first.")
        else:
            self.title(f"DrCorrect.AI - {count} terms loaded")

    def get_current_word_info(self):
        """A robust method to get the current word being typed."""
        cursor_index = self.text_widget.index(tk.INSERT)
        line_start = self.text_widget.index(f"{cursor_index} linestart")
        text_on_line = self.text_widget.get(line_start, cursor_index)
        
        words = text_on_line.strip().split()
        if not words:
            return "", cursor_index, cursor_index

        current_word = words[-1]
        
        word_len = len(current_word)
        start_index = self.text_widget.index(f"{cursor_index}-{word_len}c")
        
        return current_word, start_index, cursor_index

    def _on_key_release(self, event):
        """Handles auto-suggestion on key release."""
        if event.keysym.isalnum() and event.char.strip():
            self.show_suggestions()
        elif event.keysym in ['BackSpace', 'space', 'Return']:
            self.suggestion_listbox.place_forget()

    def show_suggestions(self):
        """Displays the suggestion listbox below the cursor."""
        current_word, _, _ = self.get_current_word_info()
        
        if len(current_word) < 3:
            self.suggestion_listbox.place_forget()
            return

        suggestions = self.processor.get_suggestions(current_word.lower())

        if suggestions:
            x, y, _, h = self.text_widget.bbox(tk.INSERT)
            self.suggestion_listbox.place(x=self.text_widget.winfo_x() + x, y=self.text_widget.winfo_y() + y + h)
            self.suggestion_listbox.delete(0, tk.END)
            for s in suggestions: self.suggestion_listbox.insert(tk.END, s)
            if suggestions: self.suggestion_listbox.selection_set(0)
        else:
            self.suggestion_listbox.place_forget()
            
    def _accept_suggestion(self, event=None):
        """Inserts the selected suggestion into the text widget."""
        if not self.suggestion_listbox.winfo_viewable():
            return "break"
        selection_indices = self.suggestion_listbox.curselection()
        if not selection_indices:
            return "break"
        
        selected_suggestion = self.suggestion_listbox.get(selection_indices[0])
        
        # We need the word info to correctly replace the text
        _, start_index, end_index = self.get_current_word_info()
        
        self.text_widget.delete(start_index, end_index)
        self.text_widget.insert(start_index, selected_suggestion)
        self.suggestion_listbox.place_forget()
        return "break"

    def _on_space_press(self, event):
        """Handles auto-correction using robust, built-in word boundaries."""
        start_index = self.text_widget.index("insert-1c wordstart")
        end_index = self.text_widget.index("insert-1c wordend")
        word_to_check = self.text_widget.get(start_index, end_index).strip()
        
        if word_to_check:
            corrected_word = self.processor.correct_word(word_to_check.lower())
            if corrected_word and corrected_word != word_to_check.lower():
                self.text_widget.delete(start_index, end_index)
                self.text_widget.insert(start_index, corrected_word)