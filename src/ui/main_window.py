"""Main window UI for QuickConvertTool."""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Dict
from ..core.registry import ConverterRegistry
from ..core.converter import Converter


class MainWindow:
    """
    Main application window for QuickConvertTool.

    Provides a user-friendly interface for selecting conversion types and
    performing unit conversions. Supports dynamic parameter input for
    parameterized converters.
    """

    _MIN_WIDTH = 500
    _MIN_HEIGHT = 400
    _DEFAULT_WIDTH = 550
    _DEFAULT_HEIGHT = 450

    def __init__(self, registry: ConverterRegistry):
        """
        Initialize the main window.

        Args:
            registry: The converter registry containing all available converters
        """
        self.registry = registry
        self.current_converter: Optional[Converter] = None
        self._content_start_row = 2
        self.param_vars: Dict[str, tk.StringVar] = {}

        self.root = tk.Tk()
        self.root.title("QuickConvertTool")
        self.root.geometry(f"{self._DEFAULT_WIDTH}x{self._DEFAULT_HEIGHT}")
        self.root.minsize(self._MIN_WIDTH, self._MIN_HEIGHT)
        self.root.resizable(True, True)

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self._configure_styles()
        self._create_widgets()
        self._initialize_converter()

    def _configure_styles(self):
        """Configure ttk styles for a modern look."""
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Title.TLabel",
            font=("Segoe UI", 20, "bold"),
            foreground="#2c3e50"
        )

        style.configure(
            "Section.TLabel",
            font=("Segoe UI", 11),
            foreground="#34495e"
        )

        style.configure(
            "TLabel",
            font=("Segoe UI", 10)
        )

        style.configure(
            "TEntry",
            font=("Segoe UI", 11),
            padding=(8, 6)
        )

        style.configure(
            "TCombobox",
            font=("Segoe UI", 10),
            padding=(6, 4)
        )

        style.configure(
            "Primary.TButton",
            font=("Segoe UI", 11, "bold"),
            padding=(20, 10)
        )

        style.configure(
            "Result.TLabel",
            font=("Segoe UI", 12, "bold"),
            foreground="#27ae60",
            background="#ecf0f1",
            padding=(10, 8)
        )

        style.configure(
            "Status.TLabel",
            font=("Segoe UI", 9),
            foreground="#7f8c8d",
            padding=(5, 3)
        )

        style.configure(
            "Card.TFrame",
            background="#ffffff"
        )

    def _create_widgets(self):
        """Create and layout all UI widgets."""
        main_frame = ttk.Frame(self.root, padding="25 20 25 15")
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.columnconfigure(0, weight=0)
        main_frame.columnconfigure(1, weight=1)

        title_label = ttk.Label(
            main_frame,
            text="QuickConvertTool",
            style="Title.TLabel"
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 25))

        ttk.Label(
            main_frame,
            text="Conversion Type",
            style="Section.TLabel"
        ).grid(row=1, column=0, sticky="w", pady=(0, 8))

        self.converter_var = tk.StringVar()
        self.converter_combo = ttk.Combobox(
            main_frame,
            textvariable=self.converter_var,
            state="readonly",
            font=("Segoe UI", 10)
        )
        self.converter_combo["values"] = self.registry.get_converter_names()
        self.converter_combo.grid(row=1, column=1, sticky="ew", pady=(0, 8), padx=(10, 0))
        self.converter_combo.bind("<<ComboboxSelected>>", self._on_converter_changed)

        separator1 = ttk.Separator(main_frame, orient="horizontal")
        separator1.grid(row=2, column=0, columnspan=2, sticky="ew", pady=15)

        self.parameter_frame = ttk.Frame(main_frame)

        self.from_label = ttk.Label(main_frame, text="From", style="Section.TLabel")
        self.from_frame = ttk.Frame(main_frame)
        self.from_frame.columnconfigure(0, weight=1)
        self.from_frame.columnconfigure(1, weight=0)

        self.from_value_var = tk.StringVar()
        self.from_value_entry = ttk.Entry(
            self.from_frame,
            textvariable=self.from_value_var,
            font=("Segoe UI", 12)
        )
        self.from_value_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        self.from_value_entry.bind("<KeyRelease>", self._on_value_changed)

        self.from_unit_var = tk.StringVar()
        self.from_unit_combo = ttk.Combobox(
            self.from_frame,
            textvariable=self.from_unit_var,
            state="readonly",
            width=12,
            font=("Segoe UI", 10)
        )
        self.from_unit_combo.grid(row=0, column=1, sticky="e")
        self.from_unit_combo.bind("<<ComboboxSelected>>", self._on_unit_changed)

        self.to_label = ttk.Label(main_frame, text="To", style="Section.TLabel")
        self.to_frame = ttk.Frame(main_frame)
        self.to_frame.columnconfigure(0, weight=1)
        self.to_frame.columnconfigure(1, weight=0)

        self.to_value_var = tk.StringVar()
        self.to_value_label = ttk.Label(
            self.to_frame,
            textvariable=self.to_value_var,
            style="Result.TLabel",
            anchor="e"
        )
        self.to_value_label.grid(row=0, column=0, sticky="ew", padx=(0, 10))

        self.to_unit_var = tk.StringVar()
        self.to_unit_combo = ttk.Combobox(
            self.to_frame,
            textvariable=self.to_unit_var,
            state="readonly",
            width=12,
            font=("Segoe UI", 10)
        )
        self.to_unit_combo.grid(row=0, column=1, sticky="e")
        self.to_unit_combo.bind("<<ComboboxSelected>>", self._on_unit_changed)

        self.convert_button = ttk.Button(
            main_frame,
            text="Convert",
            command=self._perform_conversion,
            style="Primary.TButton"
        )

        self.status_var = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(
            main_frame,
            textvariable=self.status_var,
            style="Status.TLabel",
            anchor="w"
        )

        self._content_start_row = 3

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

            self.from_unit_combo["values"] = units
            self.to_unit_combo["values"] = units

            if units:
                self.from_unit_var.set(units[0])
                self.to_unit_var.set(units[1] if len(units) > 1 else units[0])

            self.from_value_var.set("")
            self.to_value_var.set("")

            if hasattr(self.current_converter, 'parameters') and self.current_converter.parameters:
                self._show_parameter_area(self.current_converter.parameters)
            else:
                self._hide_parameter_area()

            self._update_content_rows()
            self.status_var.set(f"Selected: {converter_name}")
        except KeyError as e:
            messagebox.showerror("Error", str(e))

    def _show_parameter_area(self, params_config: dict):
        """
        Dynamically create and show parameter input fields.

        Args:
            params_config: Dictionary of parameter configurations
        """
        for widget in self.parameter_frame.winfo_children():
            widget.destroy()

        self.parameter_frame.columnconfigure(1, weight=1)
        self.param_vars = {}
        row = 0

        for param_name, config in params_config.items():
            ttk.Label(
                self.parameter_frame,
                text=config["label"],
                style="Section.TLabel"
            ).grid(row=row, column=0, sticky="w", pady=8)

            var = tk.StringVar(value=config.get("default", ""))
            entry = ttk.Entry(
                self.parameter_frame,
                textvariable=var,
                font=("Segoe UI", 11)
            )
            entry.grid(row=row, column=1, sticky="ew", pady=8, padx=(10, 0))
            entry.bind("<KeyRelease>", self._on_value_changed)

            self.param_vars[param_name] = var
            row += 1

        self._content_start_row = 3 + row
        self.parameter_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 10))

    def _hide_parameter_area(self):
        """Hide the parameter area and reset content start row."""
        self.parameter_frame.grid_remove()
        self._content_start_row = 3
        self.param_vars = {}

    def _update_content_rows(self):
        """Update grid row positions for From/To/Convert/Status sections."""
        main_frame = self.from_label.master

        self.from_label.grid(row=self._content_start_row, column=0, sticky="w", pady=(10, 8))
        self.from_frame.grid(row=self._content_start_row, column=1, sticky="ew", pady=(10, 8), padx=(10, 0))

        self.to_label.grid(row=self._content_start_row + 1, column=0, sticky="w", pady=8)
        self.to_frame.grid(row=self._content_start_row + 1, column=1, sticky="ew", pady=8, padx=(10, 0))

        self.convert_button.grid(row=self._content_start_row + 2, column=0, columnspan=2, pady=25)

        self.status_label.grid(row=self._content_start_row + 3, column=0, columnspan=2, sticky="ew", pady=(5, 0))

        for i in range(self._content_start_row + 4):
            main_frame.rowconfigure(i, weight=0)

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
            value_str = self.from_value_var.get().strip()
            if not value_str:
                self.to_value_var.set("")
                return

            value = float(value_str)

            from_unit = self.from_unit_var.get()
            to_unit = self.to_unit_var.get()

            if not from_unit or not to_unit:
                return

            kwargs = {}
            if hasattr(self.current_converter, 'parameters') and self.current_converter.parameters:
                for param_name, var in self.param_vars.items():
                    param_str = var.get().strip()
                    if param_str:
                        try:
                            kwargs[param_name] = float(param_str)
                        except ValueError:
                            raise ValueError(
                                f"Invalid value for parameter '{param_name}': must be a number"
                            )

            result = self.current_converter.convert(value, from_unit, to_unit, **kwargs)

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
                self.status_var.set(str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Conversion failed: {str(e)}")
            self.status_var.set("Conversion failed")

    def run(self):
        """Start the application main loop."""
        self.root.mainloop()
