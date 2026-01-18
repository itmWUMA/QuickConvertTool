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

    def __init__(self, registry: ConverterRegistry):
        """
        Initialize the main window.

        Args:
            registry: The converter registry containing all available converters
        """
        self.registry = registry
        self.current_converter: Optional[Converter] = None

        # Track the starting row for content (From/To/Convert)
        self._content_start_row = 2

        # Storage for parameter input variables
        self.param_vars: Dict[str, tk.StringVar] = {}

        # Create main window
        self.root = tk.Tk()
        self.root.title("QuickConvertTool")
        self.root.geometry("450x380")
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

        # Parameter area (initially hidden, will be dynamically shown for parameterized converters)
        self.parameter_frame = ttk.Frame(main_frame)

        # From section
        self.from_label = ttk.Label(main_frame, text="From:")
        self.from_frame = ttk.Frame(main_frame)

        self.from_value_var = tk.StringVar()
        self.from_value_entry = ttk.Entry(
            self.from_frame,
            textvariable=self.from_value_var,
            width=15
        )
        self.from_value_entry.grid(row=0, column=0, padx=(0, 5))
        self.from_value_entry.bind("<KeyRelease>", self._on_value_changed)

        self.from_unit_var = tk.StringVar()
        self.from_unit_combo = ttk.Combobox(
            self.from_frame,
            textvariable=self.from_unit_var,
            state="readonly",
            width=12
        )
        self.from_unit_combo.grid(row=0, column=1)
        self.from_unit_combo.bind("<<ComboboxSelected>>", self._on_unit_changed)

        # To section
        self.to_label = ttk.Label(main_frame, text="To:")
        self.to_frame = ttk.Frame(main_frame)

        self.to_value_var = tk.StringVar()
        self.to_value_label = ttk.Label(
            self.to_frame,
            textvariable=self.to_value_var,
            relief=tk.SUNKEN,
            width=15,
            anchor=tk.E,
            padding=(5, 2)
        )
        self.to_value_label.grid(row=0, column=0, padx=(0, 5))

        self.to_unit_var = tk.StringVar()
        self.to_unit_combo = ttk.Combobox(
            self.to_frame,
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

        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(
            main_frame,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W
        )

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

            # Show or hide parameter area based on converter type
            if hasattr(self.current_converter, 'parameters') and self.current_converter.parameters:
                self._show_parameter_area(self.current_converter.parameters)
            else:
                self._hide_parameter_area()

            # Update content row positions
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
        # Clear existing parameter widgets
        for widget in self.parameter_frame.winfo_children():
            widget.destroy()

        # Create parameter input fields
        self.param_vars = {}
        row = 0

        for param_name, config in params_config.items():
            ttk.Label(
                self.parameter_frame,
                text=config["label"]
            ).grid(row=row, column=0, sticky=tk.W, pady=5)

            var = tk.StringVar(value=config.get("default", ""))
            entry = ttk.Entry(
                self.parameter_frame,
                textvariable=var,
                width=30
            )
            entry.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5)
            entry.bind("<KeyRelease>", self._on_value_changed)

            self.param_vars[param_name] = var
            row += 1

        # Update content start row to account for parameters
        self._content_start_row = 2 + row

        # Show parameter area
        self.parameter_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E))

    def _hide_parameter_area(self):
        """Hide the parameter area and reset content start row."""
        self.parameter_frame.grid_remove()
        self._content_start_row = 2
        self.param_vars = {}

    def _update_content_rows(self):
        """Update grid row positions for From/To/Convert/Status sections."""
        # From section
        self.from_label.grid(row=self._content_start_row, column=0, sticky=tk.W, pady=5)
        self.from_frame.grid(row=self._content_start_row, column=1, sticky=(tk.W, tk.E), pady=5)

        # To section
        self.to_label.grid(row=self._content_start_row + 1, column=0, sticky=tk.W, pady=5)
        self.to_frame.grid(row=self._content_start_row + 1, column=1, sticky=(tk.W, tk.E), pady=5)

        # Convert button
        self.convert_button.grid(row=self._content_start_row + 2, column=0, columnspan=2, pady=20)

        # Status bar
        self.status_label.grid(row=self._content_start_row + 3, column=0, columnspan=2, sticky=(tk.W, tk.E))

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

            # Collect parameters if converter requires them
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

            # Perform conversion
            result = self.current_converter.convert(value, from_unit, to_unit, **kwargs)

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
                self.status_var.set(str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Conversion failed: {str(e)}")
            self.status_var.set("Conversion failed")

    def run(self):
        """Start the application main loop."""
        self.root.mainloop()
