from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

# Import view function
from lists.views import home_page # home_page is the view function stored in lists/views.py

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
		
	def test_home_page_returns_correct_html(self):
		request = HttpRequest() # An HttpRequest object, this is what Django sees when a user's browser asks for a page
		response = home_page(request) # We pass this request to our home_page view, which gives a reponse in form of an HttpResponse object
		expected_html = render_to_string('home.html')
		self.assertEqual(response.content.decode(), expected_html)
		
		self.assertTrue(response.content.startswith(b'<html>'))
		self.assertIn(b'<title>To-Do lists</title>', response.content)
		self.assertTrue(response.content.endswith(b'</html>'))
		
		# NB: response.content is the HTML contents of the HttpResponse object
		
		# NB: response.content is in raw bytes, not a Python string, so
		# we have to use the b'' syntax to compare them (converts string to bytes)
		
	def test_home_page_can_save_a_POST_request(self):
		request = HttpRequest()
		request.method = 'POST'
		request.POST['item_text'] = 'A new list item'
		
		response = home_page(request)
		
		self.assertIn('A new list item', response.content.decode())
		expected_html = render_to_string(
			'home.html',
			{'new_item_text': 'A new list item'}
		)
		self.assertEqual(response.content.decode(), expected_html)