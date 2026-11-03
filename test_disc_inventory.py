import csv
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from disc_inventory import Disc, TEXT_FIELDS, save_disc, validate_text


class TextValidationTests(unittest.TestCase):
    def test_blocks_special_characters_in_every_string_field(self):
        for field in TEXT_FIELDS:
            for value in [chr(n) for n in (39, 34, 96, 59, 60, 62, 38, 124, 36, 61, 43, 64, 92, 9, 0)]:
                with self.subTest(field=field, value=value):
                    with self.assertRaises(ValueError):
                        validate_text(field, value)
            with self.assertRaises(ValueError):
                validate_text(field, ' -123')

    def test_allowed_text_and_comment_line_breaks(self):
        for field in TEXT_FIELDS:
            validate_text(field, 'Élan 2, blue-white_pro.')
        validate_text('comment', 'First line.\nSecond line.')
        with self.assertRaises(ValueError):
            validate_text('name', 'Two\nlines')

    def test_invalid_record_does_not_change_csv(self):
        disc = Disc('Roadrunner', 'Innova', 9, 5, -4, 1, 'Star', 170,
                    'Blue', True, 4.5, 'Good disc, flies straight.\nEasy to throw')
        with TemporaryDirectory() as folder:
            path = Path(folder) / 'inventory.csv'
            save_disc(disc, path)
            original = path.read_bytes()
            with path.open(newline='', encoding='utf-8') as file:
                rows = list(csv.DictReader(file))
            self.assertEqual(rows[0]['turn'], '-4')
            self.assertEqual(rows[0]['comment'], disc.comment)
            for field in TEXT_FIELDS:
                previous = getattr(disc, field)
                setattr(disc, field, '=1+1')
                with self.assertRaises(ValueError):
                    save_disc(disc, path)
                self.assertEqual(path.read_bytes(), original)
                setattr(disc, field, previous)


if __name__ == '__main__':
    unittest.main()
