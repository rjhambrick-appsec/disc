# Disc Inventory

A Python desktop application using Tkinter (included with the standard Windows Python installer). No additional packages are required.

## Run

Install Python 3.10 or later with Tkinter support, then run from this folder:

```powershell
python disc_inventory.py
```

Enter the disc details and click **Save disc**. Use **Currently in my bag** for the Boolean field. Comment is optional; all other text and number fields are required. Speed, glide, turn, fade, and weight accept integers (including negative turn values), and rating accepts a finite decimal number. Weight is entered in grams. No rating scale is imposed.

Each save appends a record to `disc_inventory.csv` beside the application, using all twelve columns. Existing records are retained. Boolean values are stored as `True` or `False`; commas, quotes, and multiline comments are handled by Python's CSV writer. After a successful save, the form clears for the next disc. **Clear** resets the form without saving.
