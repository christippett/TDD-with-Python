from django.test import TestCase
from django.core.urlresolvers import resolve
from lists.views import home_page

# TestCase is an augmented version of the standard unittest.TestCase,
# with some Django-specific features thrown in

# class SmokeTest(TestCase):
# 	
# 	def test_bad_maths(self):
# 		self.assertEqual(1 + 1, 3)

class HomePageTest(TestCase):
	
	def test_root_url_resolves_to_home_page_view(self):
		found = resolve('/') # function Django uses internally to resolve URLs and find what view function they should be mapped to
		self.assertEqual(found.func, home_page) # Check that resolve, when called with '/', finds a function called home_page
		
		# NB: home_page is the view function stored in lists/views.py