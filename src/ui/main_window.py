"""Main window UI for QuickConvertTool."""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional
from ..core.registry import ConverterRegistry
from ..core.converter import Converter


class MainWindow:
    """
    Main application window for QuickConvertTool.

    Provides a user-friendly interface for selecting conversion types and
    performing unit conversions.
    """

    def __init__(self, registry: ConverterRegistry):
        """
        Initialize the main window.

        Args:
            registry: The converter registry containing all available converters
        """
        self.registry = registry
        self.current_converter: Optional[Converter] = None

        # Create main window
        self.root = tk.Tk()
        self.root.title("QuickConvertTool")
        self.root.geometry("450x300")
        self.root.resizable(False, False)

        # Configure style
        style = ttk.Style()
        style.theme_use("clam")

        self._create_widgets()
        self._initialize_converter()

    def _create_widgets(self):
        """Create and layout all UI widgets."""
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Title
        title_label = ttk.Label(
            main_frame,
            text="QuickConvertTool",
            font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Converter type selection
        ttk.Label(main_frame, text="Conversion Type:").grid(
            row=1, column=0, sticky=tk.W, pady=5
        )
        self.converter_var = tk.StringVar()
        self.converter_combo = ttk.Combobox(
            main_frame,
            textvariable=self.converter_var,
            state="readonly",
            width=30
        )
        self.converter_combo["values"] = self.registry.get_converter_names()
        self.converter_combo.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)
        self.converter_combo.bind("<<ComboboxSelected>>", self._on_converter_changed)

        # From section
        ttk.Label(main_frame, text="From:").grid(
            row=2, column=0, sticky=tk.W, pady=5
        )
        from_frame = ttk.Frame(main_frame)
        from_frame.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)

        self.from_value_var = tk.StringVar()
        self.from_value_entry = ttk.Entry(
            from_frame,
            textvariable=self.from_value_var,
            width=15
        )
        self.from_value_entry.grid(row=0, column=0, padx=(0, 5))
        self.from_value_entry.bind("<KeyRelease>", self._on_value_changed)

        self.from_unit_var = tk.StringVar()
        self.from_unit_combo = ttk.Combobox(
            from_frame,
            textvariable=self.from_unit_var,
            state="readonly",
            width=12
        )
        self.from_unit_combo.grid(row=0, column=1)
        self.from_unit_combo.bind("<<ComboboxSelected>>", self._on_unit_changed)

        # To section
        ttk.Label(main_frame, text="To:").grid(
            row=3, column=0, sticky=tk.W, pady=5
        )
        to_frame = ttk.Frame(main_frame)
        to_frame.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5)

        self.to_value_var = tk.StringVar()
        self.to_value_label = ttk.Label(
            to_frame,
            textvariable=self.to_value_var,
            relief=tk.SUNKEN,
            width=15,
            anchor=tk.E,
            padding=(5, 2)
        )
        self.to_value_label.grid(row=0, column=0, padx=(0, 5))

        self.to_unit_var = tk.StringVar()
        self.to_unit_combo = ttk.Combobox(
            to_frame,
            textvariable=self.to_unit_var,
            state="readonly",
            width=12
        )
        self.to_unit_combo.grid(row=0, column=1)
        self.to_unit_combo.bind("<<ComboboxSelected>>", self._on_unit_changed)

        # Convert button
        self.convert_button = ttk.Button(
            main_frame,
            text="Convert",
            command=self._perform_conversion
        )
        self.convert_button.grid(row=4, column=0, columnspan=2, pady=20)

        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(
            main_frame,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        status_label.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E))

        # Configure column weights
        main_frame.columnconfigure(1, weight=1)

    def _initialize_converter(self):
        """Initialize the first converter if available."""
        converter_names = self.registry.get_converter_names()
        if converter_names:
            self.converter_var.set(converter_names[0])
            self._on_converter_changed()

    def _on_converter_changed(self, event=None):
        """Handle converter type selection change."""
        converter_name = self.converter_var.get()
        if not converter_name:
            return

        try:
            self.current_converter = self.registry.get_converter(converter_name)
            units = self.current_converter.units

            # Update unit combo boxes
            self.from_unit_combo["values"] = units
            self.to_unit_combo["values"] = units

            # Set default units
            if units:
                self.from_unit_var.set(units[0])
                self.to_unit_var.set(units[1] if len(units) > 1 else units[0])

            # Clear values
            self.from_value_var.set("")
            self.to_value_var.set("")

            self.status_var.set(f"Selected: {converter_name}")
        except KeyError as e:
            messagebox.showerror("Error", str(e))

    def _on_unit_changed(self, event=None):
        """Handle unit selection change."""
        self._perform_conversion()

    def _on_value_changed(self, event=None):
        """Handle input value change (for real-time conversion)."""
        self._perform_conversion()

    def _perform_conversion(self):
        """Perform the conversion and update the result."""
        if not self.current_converter:
            return

        try:
            # Get input value
            value_str = self.from_value_var.get().strip()
            if not value_str:
                self.to_value_var.set("")
                return

            value = float(value_str)

            # Get units
            from_unit = self.from_unit_var.get()
            to_unit = self.to_unit_var.get()

            if not from_unit or not to_unit:
                return

            # Perform conversion
            result = self.current_converter.convert(value, from_unit, to_unit)

            # Format result (6 significant figures)
            if abs(result) < 0.000001 and result != 0:
                formatted_result = f"{result:.6e}"
            else:
                formatted_result = f"{result:.6g}"

            self.to_value_var.set(formatted_result)
            self.status_var.set("Conversion successful")

        except ValueError as e:
            if str(e).startswith("Unsupported unit"):
                messagebox.showerror("Error", str(e))
            else:
                self.to_value_var.set("Invalid input")
                self.status_var.set("Please enter a valid number")
        except Exception as e:
            messagebox.showerror("Error", f"Conversion failed: {str(e)}")
            self.status_var.set("Conversion failed")

    def run(self):
        """Start the application main loop."""
        self.root.mainloop()
