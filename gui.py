import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.scrolled import ScrolledText
from tkinter import messagebox
import os
import threading
import queue
from text_processor import MedicalTextProcessor
from ai_helper import AIHelper

class DrCorrectApp(ttk.Window):
    def __init__(self):
        super().__init__(themename="litera") 
        
        API_KEY = os.getenv("GEMINI_API_KEY")
        if not API_KEY:
            messagebox.showerror("API Key Error", "GEMINI_API_KEY environment variable not found.\nAI features will be disabled.")
            self.ai_helper = None
        else:
            self.ai_helper = AIHelper(API_KEY)

        self.processor = MedicalTextProcessor()
        self.title("DrCorrect.AI - Medical Terminology Assistant")
        self.geometry("1000x700")

        main_frame = ttk.Frame(self)
        main_frame.pack(expand=True, fill='both', padx=10, pady=10)
        
        self.text_widget = ScrolledText(main_frame, wrap=tk.WORD, font=("Helvetica", 11), undo=True, autohide=True)
        self.text_widget.pack(expand=True, fill='both', side='left', padx=(0, 5))
        self.text_widget.tag_configure("misspelled", foreground="red", underline=True)
        
        self.ai_sidebar = ttk.Frame(main_frame, width=300)
        self.ai_sidebar.pack(side='right', fill='y')
        self.ai_sidebar.pack_propagate(False)
        ttk.Label(self.ai_sidebar, text="AI Assistant", font=("Helvetica", 12, "bold")).pack(anchor='w', pady=(0, 5))
        self.ai_display = ttk.Label(self.ai_sidebar, text="Select text and right-click to analyze.", wraplength=280)
        self.ai_display.pack(anchor='w', fill='x')

        self.suggestion_listbox = tk.Listbox(self, font=("Helvetica", 10), height=5)
        self.right_click_menu = tk.Menu(self.text_widget.text, tearoff=0)
        self.right_click_menu.add_command(label="Analyze Selected Text", command=self.run_ai_analysis)
        
        self.ai_queue = queue.Queue()
        self.after(100, self.process_ai_queue)

        self._bind_events()
        self.load_default_corpus()

    def _bind_events(self):
        self.text_widget.text.bind("<KeyRelease>", self._on_key_release)
        self.text_widget.text.bind("<space>", self._on_space_press) # Restore space binding's full function
        self.text_widget.text.bind("<Button-3>", self.show_right_click_menu)
        self.text_widget.text.bind("<Down>", self._on_down_arrow)
        self.text_widget.text.bind("<Up>", self._on_up_arrow)
        self.text_widget.text.bind("<Return>", self._accept_suggestion)
        self.text_widget.text.bind("<Tab>", self._accept_suggestion)
        self.suggestion_listbox.bind("<Double-1>", self._accept_suggestion)

    def load_default_corpus(self):
        success, count = self.processor.load_corpus_from_txt('medical_vocabulary.txt')
        if not success: messagebox.showerror("Vocabulary Error", "Could not find 'medical_vocabulary.txt'.")
        else: self.title(f"DrCorrect.AI - {count} terms loaded")

    def get_current_word_info(self):
        cursor_index = self.text_widget.index(tk.INSERT)
        line_start = self.text_widget.index(f"{cursor_index} linestart")
        text_on_line = self.text_widget.get(line_start, cursor_index)
        words = text_on_line.strip().split()
        if not words: return "", cursor_index, cursor_index
        current_word = words[-1]
        word_len = len(current_word)
        start_index = self.text_widget.index(f"{cursor_index}-{word_len}c")
        return current_word, start_index, cursor_index

    def _on_key_release(self, event):
        if event.keysym.isalnum() and event.char.strip():
            self.show_suggestions()
        elif event.keysym in ['BackSpace', 'space', 'Return', 'Tab', 'Up', 'Down']:
            self.suggestion_listbox.place_forget()

    def show_suggestions(self):
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
    
    def _on_space_press(self, event):
        """On space press, perform intelligent auto-correction OR highlight."""
        start_index = self.text_widget.index("insert-1c wordstart")
        end_index = self.text_widget.index("insert-1c wordend")
        word = self.text_widget.get(start_index, end_index).strip(".,!?:;")
        
        if word and not self.processor.is_known(word):
            # Check for an unambiguous correction
            corrected_word = self.processor.get_unambiguous_correction(word.lower())
            if corrected_word:
                # If found, perform the correction automatically
                self.text_widget.delete(start_index, end_index)
                self.text_widget.insert(start_index, corrected_word)
            else:
                # If ambiguous or no correction found, just highlight
                self.text_widget.tag_add("misspelled", start_index, end_index)
        else:
            self.text_widget.tag_remove("misspelled", start_index, end_index)

    def _accept_suggestion(self, event=None):
        if not self.suggestion_listbox.winfo_viewable(): return
        selection_indices = self.suggestion_listbox.curselection()
        if not selection_indices:
            if event and event.keysym == 'Tab': return "break"
            return
        selected_suggestion = self.suggestion_listbox.get(selection_indices[0])
        _, start_index, end_index = self.get_current_word_info()
        self.text_widget.delete(start_index, end_index)
        self.text_widget.insert(start_index, selected_suggestion)
        self.suggestion_listbox.place_forget()
        return "break"

    def _on_down_arrow(self, event):
        if not self.suggestion_listbox.winfo_viewable(): return "break"
        selection_indices = self.suggestion_listbox.curselection()
        if not selection_indices:
            self.suggestion_listbox.selection_set(0)
        else:
            current_index = selection_indices[0]
            if current_index < self.suggestion_listbox.size() - 1:
                self.suggestion_listbox.selection_clear(current_index)
                self.suggestion_listbox.selection_set(current_index + 1)
        return "break"

    def _on_up_arrow(self, event):
        if not self.suggestion_listbox.winfo_viewable(): return "break"
        selection_indices = self.suggestion_listbox.curselection()
        if not selection_indices: return
        current_index = selection_indices[0]
        if current_index > 0:
            self.suggestion_listbox.selection_clear(current_index)
            self.suggestion_listbox.selection_set(current_index - 1)
        return "break"

    def show_right_click_menu(self, event):
        self.right_click_menu.tk_popup(event.x_root, event.y_root)

    def run_ai_analysis(self):
        if not self.ai_helper or not self.ai_helper.is_ready():
            messagebox.showwarning("AI Not Ready", "The AI Assistant is not available.")
            return
        try:
            selected_text = self.text_widget.get(tk.SEL_FIRST, tk.SEL_LAST).strip()
            if not selected_text:
                messagebox.showwarning("Warning", "Please select text to analyze.")
                return
            self.clear_sidebar()
            ttk.Label(self.ai_sidebar, text=f"Analyzing: '{selected_text}'...", wraplength=280).pack(anchor='w')
            ttk.Progressbar(self.ai_sidebar, mode='indeterminate', name='progressbar').pack(fill='x', pady=5)
            self.ai_sidebar.children['progressbar'].start()
            threading.Thread(target=self._get_analysis_thread, args=(selected_text,), daemon=True).start()
        except tk.TclError:
            messagebox.showwarning("Warning", "Please select text to analyze.")

    def _get_analysis_thread(self, selected_text):
        result = self.ai_helper.analyze_text(selected_text)
        self.ai_queue.put(result)

    def process_ai_queue(self):
        try:
            result = self.ai_queue.get_nowait()
            self.clear_sidebar()
            self.ai_display = ttk.Label(self.ai_sidebar, text=result, wraplength=280)
            self.ai_display.pack(anchor='w', fill='x')
        except queue.Empty:
            pass
        finally:
            self.after(100, self.process_ai_queue)
    
    def clear_sidebar(self):
        for widget in self.ai_sidebar.winfo_children():
            widget.destroy()
        ttk.Label(self.ai_sidebar, text="AI Assistant", font=("Helvetica", 12, "bold")).pack(anchor='w', pady=(0, 5))