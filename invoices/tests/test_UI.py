from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver


class TestLandingPage(StaticLiveServerTestCase):

    def setUp(self):
        self.base_url = self.live_server_url

        self.driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver') # Add chrome driver to sys PATH first

    def test_landing_page_load(self):
        self.driver.get(self.base_url)
        self.assertEqual(self.driver.title, "Invoices Landing Page")
        # self.assertIn("localhost", self.driver.current_url)


    # def test_landing_page_links(self):
        # self.driver.get(self.base_url)
        # self.assertEqual(self.driver.title, "Invoices Landing Page")
        # self.assertIn("http://127.0.0.1:8000/", self.driver.current_url)




    def tearDown(self):
        self.driver.quit()



