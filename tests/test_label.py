import unittest
import pendulum
import os
from src.label import load_template, generate_label
from src.product import Product
from datetime import datetime


class TestLabel(unittest.TestCase):
    def test_template_skips_comments(self):
        template = load_template("tests/files/test_comment_template.zpl")

        self.assertEqual(template.substitute(), "^XA^CI0")

    def test_generate_label(self):
        due_date = datetime(2020, 1, 1)
        product = Product(
            product="Bread",
            grocycode="12345",
            font_family="Arial",
            due_date=due_date.strftime("%Y-%m-%d"),
        )

        template = load_template("tests/files/test_substitution_template.zpl")

        label = generate_label(template, product, 10)
        self.assertIn("Bread", label)
        self.assertIn("12345", label)
        self.assertIn(due_date.strftime("%d / %m / %y"), label)

        tz = pendulum.timezone(os.getenv("TZ", "UTC"))
        today = datetime.now(tz).strftime("%d/%m/%y")
        self.assertIn(today, label)

    def test_generate_label_splits_name(self):
        product = Product(
            product="Very Long Bread",
            grocycode="12345",
            font_family="Arial",
            due_date="2020-01-01",
        )

        template = load_template("tests/files/test_substitution_template.zpl")

        label = generate_label(template, product, 10)
        self.assertIn("Very", label)
        self.assertIn("Long Bread", str(label))
        self.assertNotIn("Very Long Bread", label)
