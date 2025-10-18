"""Main GUI application."""

import sys
import logging
from pathlib import Path
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import queue

from convertext.converters.loader import load_converters
from convertext.config import Config
from convertext.core import ConversionEngine
from convertext.registry import get_registry

from convertext_gui.widgets import DropZone, FileList, DebugConsole
from convertext_gui.logging_config import setup_logging

logger = logging.getLogger(__name__)


class ConvertExtGUI(ttk.Window):
    """Main GUI window for ConverText."""

    def __init__(self):
        super().__init__(
            themename="darkly",  # Start with dark theme
            title="ConverText",
            size=(800, 1000),
            resizable=(True, True)
        )

        # Customize theme to black/yellow only
        style = ttk.Style()

        # Base styles
        style.configure('TFrame', background='#000000')
        style.configure('TLabel', background='#000000', foreground='#FFD700', font=("Monaco", 13))
        style.configure('TLabelframe', background='#000000', foreground='#FFD700', font=("Monaco", 13), bordercolor='#FFD700', lightcolor='#FFD700', darkcolor='#FFD700')
        style.configure('TLabelframe.Label', background='#000000', foreground='#FFD700', font=("Monaco", 13, "bold"))

        # Buttons - yellow on black, no border
        style.configure('TButton', background='#FFD700', foreground='#000000', font=("Monaco", 13), borderwidth=0, relief='flat')

        # Checkbuttons - yellow square indicators
        style.configure('TCheckbutton',
                       background='#000000',
                       foreground='#FFD700',
                       font=("Monaco", 13),
                       indicatorrelief='flat',
                       indicatordiameter=13,
                       indicatormargin=5,
                       indicatorbackground='#000000',
                       indicatorforeground='#FFD700')
        style.map('TCheckbutton',
                 background=[('active', '#000000'), ('selected', '#000000')],
                 foreground=[('active', '#FFD700'), ('selected', '#FFD700')],
                 indicatorbackground=[('selected', '#FFD700'), ('!selected', '#000000')],
                 indicatorforeground=[('selected', '#000000'), ('!selected', '#FFD700')])

        # Entry fields - yellow on black
        style.configure('TEntry',
                       background='#000000',
                       foreground='#FFD700',
                       fieldbackground='#000000',
                       font=("Monaco", 13),
                       insertcolor='#FFD700',
                       bordercolor='#FFD700')
        style.map('TEntry',
                 fieldbackground=[('focus', '#000000')],
                 foreground=[('focus', '#FFD700')])

        # Convert button - large with hover effect, no border
        style.configure('Convert.TButton',
                       font=("Monaco", 21, "bold"),
                       background="#FFD700",
                       foreground="#000000",
                       borderwidth=0,
                       relief='flat')
        style.map('Convert.TButton',
                 background=[('active', '#FFFFFF'), ('!active', '#FFD700')],
                 foreground=[('active', '#000000'), ('!active', '#000000')])

        # Configure window background
        self.configure(background='#000000')

        # Set window icon
        try:
            import sys
            if getattr(sys, 'frozen', False):
                # PyInstaller bundle - assets in Resources/convertext_gui/
                base_path = Path(sys._MEIPASS) / "convertext_gui"
            else:
                # Running from source
                base_path = Path(__file__).parent

            icon_path = base_path / "assets" / "icon.png"
            if icon_path.exists():
                icon = tk.PhotoImage(file=str(icon_path))
                self.iconphoto(True, icon)
        except Exception:
            pass

        # Setup logging
        self.debug_mode = False
        self.log_file = setup_logging(self.debug_mode)
        logger.info(f"Starting ConverText GUI v{self._get_version()}")
        logger.info(f"Debug mode: {self.debug_mode}")
        logger.info(f"Log file: {self.log_file}")

        # Initialize convertext
        load_converters()
        self.convertext_config = Config()
        self.engine = ConversionEngine(self.convertext_config)

        # State
        self.format_vars = {}
        self.output_dir = None
        self.debug_console = None
        self.progress_queue = queue.Queue()

        # Build UI
        self._create_widgets()
        self._bind_shortcuts()
        self._create_menu()
        self._center_window()

        # Start queue processor
        self._process_progress_queue()

    def _get_version(self):
        """Get application version."""
        try:
            from convertext_gui import __version__
            return __version__
        except ImportError:
            return "unknown"

    def _create_widgets(self):
        """Create all UI widgets."""
        # Drop zone
        self.drop_zone = DropZone(self, self._on_files_dropped)
        self.drop_zone.pack(fill=X, padx=21, pady=21)

        # File list
        self.file_list = FileList(self)
        self.file_list.pack(fill=BOTH, expand=True, padx=21, pady=13)

        # Format selection
        self._create_format_section()

        # Output settings
        self._create_output_section()

        # Convert button
        self._create_convert_button()

        # Progress section
        self._create_progress_section()

    def _create_format_section(self):
        """Create format selection checkboxes."""
        frame = ttk.Labelframe(
            self,
            text="Output Formats",
            padding=13
        )
        frame.pack(fill=X, padx=21, pady=13)

        # Get available formats from registry
        registry = get_registry()
        formats = registry.list_supported_formats()

        # Unique target formats
        all_targets = set()
        for targets in formats.values():
            all_targets.update(targets)

        # Create checkboxes (3 per row)
        row_frame = None
        for i, fmt in enumerate(sorted(all_targets)):
            if i % 3 == 0:
                row_frame = ttk.Frame(frame)
                row_frame.pack(fill=X, pady=2)

            var = tk.BooleanVar()
            self.format_vars[fmt] = var

            cb = ttk.Checkbutton(
                row_frame,
                text=fmt.upper(),
                variable=var
            )
            cb.pack(side=LEFT, padx=13)

    def _create_output_section(self):
        """Create output directory selector."""
        frame = ttk.Frame(self)
        frame.pack(fill=X, padx=21, pady=13)

        label = ttk.Label(frame, text="Output Directory:")
        label.pack(anchor=W)

        row = ttk.Frame(frame)
        row.pack(fill=X, pady=8)

        # Entry field showing actual path
        self.output_var = tk.StringVar(value=str(Path.home()))
        self.output_dir = Path.home()

        output_entry = ttk.Entry(
            row,
            textvariable=self.output_var,
            font=("Monaco", 13),
            foreground='#FFD700'
        )
        output_entry.pack(side=LEFT, fill=X, expand=True, padx=(0, 13))

        # Browse button
        browse_btn = ttk.Button(
            row,
            text="Browse...",
            command=self._browse_output,
            style='Convert.TButton'
        )
        browse_btn.pack(side=LEFT)

        # Overwrite checkbox
        self.overwrite_var = tk.BooleanVar(value=False)
        overwrite_cb = ttk.Checkbutton(
            frame,
            text="Overwrite existing files",
            variable=self.overwrite_var
        )
        overwrite_cb.pack(anchor=W, pady=8)

        # Debug options
        debug_row = ttk.Frame(frame)
        debug_row.pack(fill=X, pady=8)

        self.debug_var = tk.BooleanVar(value=self.debug_mode)
        debug_cb = ttk.Checkbutton(
            debug_row,
            text="Debug mode (verbose output)",
            variable=self.debug_var,
            command=self._toggle_debug
        )
        debug_cb.pack(side=LEFT)

        self.keep_intermediate_var = tk.BooleanVar(value=False)
        keep_cb = ttk.Checkbutton(
            debug_row,
            text="Keep intermediate files",
            variable=self.keep_intermediate_var
        )
        keep_cb.pack(side=LEFT, padx=(13, 0))

    def _create_convert_button(self):
        """Create main convert button."""
        self.convert_btn = ttk.Button(
            self,
            text="Convert",
            command=self.start_conversion,
            style='Convert.TButton',
            width=21
        )
        self.convert_btn.pack(pady=21)

    def _create_progress_section(self):
        """Create progress bar and status."""
        frame = ttk.Frame(self)
        frame.pack(fill=X, padx=21, pady=13)

        # Progress label (hidden initially)
        self.progress_label = ttk.Label(
            frame,
            text="",
            font=("Monaco", 10)
        )
        self.progress_label.pack(anchor=W)

        # Progress bar (yellow theme)
        style = ttk.Style()
        style.configure('Yellow.Horizontal.TProgressbar',
                       background='#FFD700',
                       troughcolor='#000000',
                       bordercolor='#FFD700',
                       lightcolor='#FFD700',
                       darkcolor='#FFD700')

        self.progress_bar = ttk.Progressbar(
            frame,
            mode="determinate",
            style='Yellow.Horizontal.TProgressbar',
            maximum=100
        )
        self.progress_bar.pack(fill=X, pady=5)

        # Status text with ETA
        self.status_label = ttk.Label(
            frame,
            text="",
            font=("Monaco", 9)
        )
        self.status_label.pack(anchor=W)

    def _on_files_dropped(self, files):
        """Handle files dropped or selected."""
        self.file_list.add_files(files)
        self._update_output_from_files()

    def _update_output_from_files(self):
        """Update output path based on first selected file."""
        if self.file_list.files:
            # Default to first file's directory
            first_file = self.file_list.files[0]
            self.output_dir = first_file.parent
            self.output_var.set(str(self.output_dir))
        else:
            self.output_var.set("")
            self.output_dir = None

    def _browse_output(self):
        """Browse for custom output directory."""
        from tkinter import filedialog
        directory = filedialog.askdirectory(
            title="Select Output Directory",
            initialdir=str(self.output_dir) if self.output_dir else str(Path.home())
        )
        if directory:
            self.output_dir = Path(directory)
            self.output_var.set(str(self.output_dir))

    def start_conversion(self):
        """Start conversion process."""
        # Validate
        if not self.file_list.files:
            self._show_error("No files selected", "Please add files to convert.")
            return

        selected_formats = [fmt for fmt, var in self.format_vars.items() if var.get()]
        if not selected_formats:
            self._show_error("No formats selected", "Please select at least one output format.")
            return

        # Disable UI
        self.convert_btn.configure(state="disabled", text="Converting...")
        self.progress_bar['value'] = 0

        # Start thread
        from convertext_gui.threads import ConversionThread
        logger.info(f"Starting conversion: {len(self.file_list.files)} files to {selected_formats}")
        thread = ConversionThread(
            engine=self.engine,
            files=self.file_list.files,
            formats=selected_formats,
            output_dir=self.output_dir,
            overwrite=self.overwrite_var.get(),
            keep_intermediate=self.keep_intermediate_var.get(),
            callback=self._on_conversion_progress
        )
        thread.start()

    def _on_conversion_progress(self, progress, status, result):
        """Update UI from conversion thread."""
        self.progress_queue.put((progress, status, result))

    def _process_progress_queue(self):
        """Process queued progress updates (runs in main thread)."""
        try:
            while True:
                progress, status, result = self.progress_queue.get_nowait()
                self._update_ui(progress, status, result)
        except queue.Empty:
            pass
        finally:
            self.after(100, self._process_progress_queue)

    def _update_ui(self, progress, status, result):
        """Update UI elements (called from main thread)."""
        try:
            self.progress_bar['value'] = progress
            self.status_label.configure(text=status)

            if result:
                if result.success:
                    self.progress_label.configure(
                        text=f"✓ {result.source_path.name} → {result.target_path.name}",
                        foreground="#FFD700"
                    )
                else:
                    self.progress_label.configure(
                        text=f"✗ {result.source_path.name}: {result.error}",
                        foreground="#FFFFFF"
                    )

            if progress >= 100:
                self.convert_btn.configure(state="normal", text="Convert")
                self._show_success()
        except Exception as e:
            logger.exception(f"UI update failed: {e}")
            try:
                self.convert_btn.configure(state="normal", text="Convert")
            except:
                pass

    def _show_success(self):
        """Show success dialog."""
        from tkinter import messagebox
        result = messagebox.askyesno(
            "Conversion Complete",
            f"Successfully converted {len(self.file_list.files)} file(s)!\n\nOpen output folder?",
            parent=self
        )
        if result:
            self._open_output_folder()

    def _open_output_folder(self):
        """Open output folder in system file manager."""
        import subprocess

        folder = self.output_dir if self.output_dir else self.file_list.files[0].parent

        if sys.platform == "win32":
            subprocess.Popen(f'explorer "{folder}"')
        elif sys.platform == "darwin":
            subprocess.Popen(["open", str(folder)])
        else:  # linux
            subprocess.Popen(["xdg-open", str(folder)])

    def _show_error(self, title, message):
        """Show error dialog."""
        from tkinter import messagebox
        messagebox.showerror(title, message, parent=self)

    def _toggle_debug(self):
        """Toggle debug mode."""
        self.debug_mode = self.debug_var.get()
        setup_logging(self.debug_mode)
        logger.info(f"Debug mode {'enabled' if self.debug_mode else 'disabled'}")

        if self.debug_mode and not self.debug_console:
            self._show_debug_console()
        elif not self.debug_mode and self.debug_console:
            self._hide_debug_console()

    def _show_debug_console(self):
        """Show debug console window."""
        if self.debug_console:
            return

        self.debug_console = DebugConsole(self)
        logger.info("Debug console opened")

    def _hide_debug_console(self):
        """Hide debug console window."""
        if self.debug_console:
            self.debug_console.destroy()
            self.debug_console = None
            logger.info("Debug console closed")

    def _bind_shortcuts(self):
        """Bind keyboard shortcuts."""
        self.bind('<Control-o>', lambda e: self.drop_zone._on_click(None))
        self.bind('<Control-Return>', lambda e: self.start_conversion())
        self.bind('<Escape>', lambda e: self.quit())
        self.bind('<Control-q>', lambda e: self.quit())
        self.bind('<Control-d>', lambda e: self._toggle_debug())
        logger.debug("Keyboard shortcuts bound")

    def _create_menu(self):
        """Create menu bar."""
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open Files...", command=lambda: self.drop_zone._on_click(None), accelerator="Ctrl+O")
        file_menu.add_separator()
        file_menu.add_command(label="Quit", command=self.quit, accelerator="Ctrl+Q")

        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_checkbutton(label="Debug Console", variable=self.debug_var, command=self._toggle_debug, accelerator="Ctrl+D")

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self._show_about)
        help_menu.add_command(label="View Logs", command=self._open_log_file)

    def _show_about(self):
        """Show about dialog."""
        from tkinter import messagebox
        version = self._get_version()
        messagebox.showinfo(
            "About ConverText",
            f"ConverText v{version}\n\n"
            "Universal document converter\n\n"
            f"Debug mode: {self.debug_mode}\n"
            f"Log file: {self.log_file}\n\n"
            "License: MIT",
            parent=self
        )

    def _open_log_file(self):
        """Open log file in default editor."""
        import subprocess
        if sys.platform == "win32":
            subprocess.Popen(['notepad', str(self.log_file)])
        elif sys.platform == "darwin":
            subprocess.Popen(['open', str(self.log_file)])
        else:
            subprocess.Popen(['xdg-open', str(self.log_file)])

    def _center_window(self):
        """Center window on screen."""
        self.update_idletasks()
        width = 800
        height = 1000
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
        self.minsize(700, 800)


def main():
    """Main entry point."""
    app = ConvertExtGUI()
    app.mainloop()


if __name__ == "__main__":
    main()
