from django.test import TestCase
from app.calc import add
from app.calc import subtract

class CalcTests(TestCase):
	def test_add_numbers(self):
		"""Test that 2 numbers are added together"""
		self.assertEqual(add(1,2), 3)
	def test_subtract_numbers(self):
		"""Test that 2 numbers are subtracted"""
		self.assertEqual(subtract(3, 1), 2)