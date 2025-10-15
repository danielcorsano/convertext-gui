"""Custom GUI widgets."""

import tkinter as tk
import ttkbootstrap as ttk
import logging
from pathlib import Path
from tkinterdnd2 import DND_FILES, TkinterDnD
from ttkbootstrap.constants import *

logger = logging.getLogger(__name__)


class DropZone(ttk.Frame):
    """Drag-and-drop file zone."""

    def __init__(self, parent, on_drop_callback):
        super().__init__(parent, bootstyle=INFO, height=200)
        self.on_drop_callback = on_drop_callback
        self.dnd_enabled = False

        # Try to enable drag-and-drop
        try:
            self.drop_target_register(DND_FILES)
            self.dnd_bind('<<Drop>>', self._on_drop)
            self.dnd_enabled = True
            text = "📁 Drag & Drop Files Here\n\nor click to browse..."
            logger.info("Drag-and-drop enabled")
        except Exception as e:
            logger.warning(f"Drag-and-drop not available: {e}")
            text = "📁 Click to Browse Files..."

        # Label
        self.label = ttk.Label(
            self,
            text=text,
            font=("Helvetica", 14),
            bootstyle="inverse-info",
            anchor="center"
        )
        self.label.pack(expand=True, fill=BOTH, padx=20, pady=20)

        # Click to browse
        self.label.bind('<Button-1>', self._on_click)

        # Hover effect
        self.label.bind('<Enter>', self._on_hover_enter)
        self.label.bind('<Leave>', self._on_hover_leave)

    def _on_drop(self, event):
        """Handle file drop."""
        files = self.tk.splitlist(event.data)
        self.on_drop_callback(files)

    def _on_click(self, event):
        """Handle click to browse."""
        from tkinter import filedialog
        files = filedialog.askopenfilenames(
            title="Select Files to Convert",
            filetypes=[
                ("All Supported", "*.pdf;*.docx;*.doc;*.txt;*.md;*.html;*.epub;*.rtf;*.odt"),
                ("PDF", "*.pdf"),
                ("Word", "*.docx;*.doc"),
                ("Text", "*.txt"),
                ("Markdown", "*.md"),
                ("HTML", "*.html;*.htm"),
                ("EPUB", "*.epub"),
                ("RTF", "*.rtf"),
                ("ODT", "*.odt"),
                ("All Files", "*.*")
            ]
        )
        if files:
            self.on_drop_callback(files)

    def _on_hover_enter(self, event):
        """Hover effect."""
        self.label.configure(bootstyle="inverse-primary")

    def _on_hover_leave(self, event):
        """Hover effect."""
        self.label.configure(bootstyle="inverse-info")


class FileList(ttk.Frame):
    """Display and manage selected files."""

    def __init__(self, parent):
        super().__init__(parent)
        self.files = []

        # Header
        header = ttk.Label(
            self,
            text="Selected Files:",
            font=("Helvetica", 12, "bold")
        )
        header.pack(anchor=W, pady=(10, 5))

        # Scrollable frame
        self.canvas = tk.Canvas(self, height=150, bg="#2b3e50")
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.file_widgets = []

    def add_files(self, file_paths):
        """Add files to list."""
        for path in file_paths:
            p = Path(path)
            if p not in self.files:
                self.files.append(p)
                self._add_file_widget(p)

    def _add_file_widget(self, file_path):
        """Add file widget to scrollable list."""
        frame = ttk.Frame(self.scrollable_frame)
        frame.pack(fill=X, pady=2)

        # File icon and name
        label = ttk.Label(
            frame,
            text=f"📄 {file_path.name}",
            font=("Helvetica", 10)
        )
        label.pack(side=LEFT, padx=5)

        # Remove button
        remove_btn = ttk.Button(
            frame,
            text="✕",
            bootstyle="danger-link",
            width=3,
            command=lambda: self._remove_file(file_path, frame)
        )
        remove_btn.pack(side=RIGHT, padx=5)

        self.file_widgets.append((file_path, frame))

    def _remove_file(self, file_path, frame):
        """Remove file from list."""
        self.files.remove(file_path)
        frame.destroy()
        self.file_widgets = [(p, f) for p, f in self.file_widgets if p != file_path]

    def clear(self):
        """Clear all files."""
        for _, frame in self.file_widgets:
            frame.destroy()
        self.files.clear()
        self.file_widgets.clear()


class DebugConsole(tk.Toplevel):
    """Debug console window for viewing logs."""

    def __init__(self, parent):
        super().__init__(parent)
        self.title("Debug Console")
        self.geometry("800x400")

        # Text widget with scrollbar
        text_frame = ttk.Frame(self)
        text_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        self.text = tk.Text(
            text_frame,
            wrap=tk.WORD,
            font=("Courier", 10),
            bg="#1e1e1e",
            fg="#d4d4d4",
            state=tk.DISABLED
        )
        scrollbar = ttk.Scrollbar(text_frame, command=self.text.yview)
        self.text.configure(yscrollcommand=scrollbar.set)

        self.text.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Buttons
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill=X, padx=10, pady=(0, 10))

        clear_btn = ttk.Button(btn_frame, text="Clear", command=self.clear, bootstyle=SECONDARY)
        clear_btn.pack(side=LEFT, padx=5)

        # Add logging handler
        self.handler = TextHandler(self.text)
        self.handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.handler.setFormatter(formatter)
        logging.getLogger().addHandler(self.handler)

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def clear(self):
        """Clear console text."""
        self.text.configure(state=tk.NORMAL)
        self.text.delete(1.0, tk.END)
        self.text.configure(state=tk.DISABLED)

    def on_close(self):
        """Handle window close."""
        logging.getLogger().removeHandler(self.handler)
        self.destroy()


class TextHandler(logging.Handler):
    """Logging handler that writes to a Text widget."""

    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget

    def emit(self, record):
        """Emit a log record to the text widget."""
        msg = self.format(record) + '\n'

        def append():
            self.text_widget.configure(state=tk.NORMAL)
            self.text_widget.insert(tk.END, msg)
            self.text_widget.see(tk.END)
            self.text_widget.configure(state=tk.DISABLED)

        # Thread-safe update
        self.text_widget.after(0, append)
