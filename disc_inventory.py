"""A simple desktop form for recording a disc golf inventory."""

import csv
from dataclasses import asdict, dataclass, fields
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, ttk


CSV_PATH = Path(__file__).resolve().with_name("disc_inventory.csv")


@dataclass
class Disc:
    name: str
    manufacturer: str
    speed: int
    glide: int
    turn: int
    fade: int
    material: str
    weight: int
    color: str
    in_bag: bool
    rating: float
    comment: str


FIELD_NAMES = [field.name for field in fields(Disc)]


def save_disc(disc: Disc, path: Path = CSV_PATH) -> None:
    """Append a record, adding the column headings to a new or empty file."""
    needs_header = not path.exists() or path.stat().st_size == 0
    if not needs_header:
        with path.open("r", newline="", encoding="utf-8") as file:
            if next(csv.reader(file), None) != FIELD_NAMES:
                raise ValueError("The existing CSV has unexpected columns.")
    with path.open("a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELD_NAMES)
        if needs_header:
            writer.writeheader()
        writer.writerow(asdict(disc))


class InventoryApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        root.title("Disc Inventory")
        root.minsize(470, 640)
        frame = ttk.Frame(root, padding=24)
        frame.grid(sticky="nsew")
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

        ttk.Label(frame, text="Add a disc", font=("Segoe UI", 20, "bold")).grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, 6)
        )
        ttk.Label(frame, text="Enter disc details. All fields except comment are required.").grid(
            row=1, column=0, columnspan=2, sticky="w", pady=(0, 18)
        )
        self.values: dict[str, tk.StringVar] = {}
        labels = [
            ("name", "Name"), ("manufacturer", "Manufacturer"),
            ("speed", "Speed (integer)"), ("glide", "Glide (integer)"),
            ("turn", "Turn (integer)"), ("fade", "Fade (integer)"),
            ("material", "Material"), ("weight", "Weight in grams (integer)"),
            ("color", "Color"), ("rating", "Rating (decimal)"),
        ]
        for row, (key, label) in enumerate(labels, start=2):
            ttk.Label(frame, text=label).grid(row=row, column=0, sticky="w", padx=(0, 16), pady=5)
            variable = tk.StringVar()
            self.values[key] = variable
            entry = ttk.Entry(frame, textvariable=variable, width=30)
            entry.grid(row=row, column=1, sticky="ew", pady=5)
            if key == "name":
                self.name_entry = entry

        self.in_bag = tk.BooleanVar(value=False)
        ttk.Checkbutton(frame, text="Currently in my bag", variable=self.in_bag).grid(
            row=12, column=1, sticky="w", pady=8
        )
        ttk.Label(frame, text="Comment (optional)").grid(row=13, column=0, sticky="nw", pady=5)
        self.comment = tk.Text(frame, height=4, width=30, wrap="word", font=("Segoe UI", 10))
        self.comment.grid(row=13, column=1, sticky="ew", pady=5)
        buttons = ttk.Frame(frame)
        buttons.grid(row=14, column=0, columnspan=2, sticky="e", pady=(16, 8))
        ttk.Button(buttons, text="Clear", command=self.clear).pack(side="left", padx=8)
        ttk.Button(buttons, text="Save disc", command=self.save).pack(side="left")
        self.status = tk.StringVar(value="Ready to add a disc.")
        ttk.Label(frame, textvariable=self.status, wraplength=420).grid(
            row=15, column=0, columnspan=2, sticky="w", pady=6
        )
        self.name_entry.focus_set()

    def clear(self) -> None:
        for variable in self.values.values():
            variable.set("")
        self.in_bag.set(False)
        self.comment.delete("1.0", tk.END)
        self.status.set("Ready to add a disc.")
        self.name_entry.focus_set()

    def save(self) -> None:
        data = {key: variable.get().strip() for key, variable in self.values.items()}
        for key, value in data.items():
            if not value:
                messagebox.showerror("Missing value", f"Please enter {key}.", parent=self.root)
                return
        try:
            for key in ("speed", "glide", "turn", "fade", "weight"):
                try:
                    data[key] = int(data[key])
                except ValueError:
                    raise ValueError(f"{key.capitalize()} must be a whole number.") from None
            try:
                data["rating"] = float(data["rating"])
            except ValueError:
                raise ValueError("Rating must be a number, such as 4.5.") from None
            import math
            if not math.isfinite(data["rating"]):
                raise ValueError("Rating must be a finite number.")
            disc = Disc(**data, in_bag=self.in_bag.get(), comment=self.comment.get("1.0", "end-1c").strip())
            save_disc(disc)
        except (ValueError, OSError, csv.Error) as error:
            messagebox.showerror("Unable to save disc", str(error), parent=self.root)
            return
        self.clear()
        self.status.set(f'Saved "{disc.name}" to disc_inventory.csv.')


def main() -> None:
    root = tk.Tk()
    InventoryApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
