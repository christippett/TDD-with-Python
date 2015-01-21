from django.test import TestCase

# TestCase is an augmented version of the standard unittest.TestCase,
# with some Django-specific features thrown in

# Create your tests here.
class SmokeTest(TestCase):
	
	def test_bad_maths(self):
		self.assertEqual(1 + 1, 3)