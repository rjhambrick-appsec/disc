# Disc Inventory

A Python desktop application using Tkinter (included with the standard Windows Python installer). No additional packages are required.

## Run

Install Python 3.10 or later with Tkinter support, then run from this folder:

```powershell
python disc_inventory.py
```

Enter the disc details and click **Save disc**. Use **Currently in my bag** for the Boolean field. Comment is optional; all other text and number fields are required. Speed, glide, turn, fade, and weight accept integers (including negative turn values), and rating accepts a finite decimal number. Weight is entered in grams. No rating scale is imposed.

All string fields (name, manufacturer, material, color, and comment) accept only Unicode letters and numbers, ordinary spaces, periods, commas, hyphens, and underscores. Comments also accept line breaks. Other characters, including quotes, semicolons, angle brackets, backslashes, and spreadsheet formula prefixes, are rejected with a field-specific error. Text cannot start with a hyphen, to prevent spreadsheet formula interpretation. Numeric fields still accept negative numbers where applicable. This intentionally restrictive policy also excludes punctuation in legitimate names, such as apostrophes. Character filtering does not replace parameterized queries or context-specific escaping if other storage or display systems are added later.

Each save appends a record to `disc_inventory.csv` beside the application, using all twelve columns. Existing records are retained. Boolean values are stored as `True` or `False`; commas and multiline comments are handled by Python's CSV writer. After a successful save, the form clears for the next disc. **Clear** resets the form without saving.
