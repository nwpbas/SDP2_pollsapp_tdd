from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest

class NewVisitorTest(unittest.TestCase):  

    def setUp(self):  
        self.browser = webdriver.Firefox()

    def tearDown(self):  
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):  
        # Edith has heard about a cool new online to-do app. She goes
        # to check out its homepage
        self.browser.get('http://localhost:8000/polls')

        # She notices the page title and header mention Polls
        self.assertIn('Polls', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text  
        self.assertIn('Question Polls', header_text)

        # She notices a section for insert a Question
        inputbox = self.browser.find_element_by_id('id_new_question')  
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a question'
        )

        # She types a Question into a text box
        inputbox.send_keys('What is your favorite color')  

        # When she hits enter, the page updates, and now the page show
        # The question that she has inserted
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # She notice the Question seems like to be able to click
        # and response back to something

        # After insert she notice the page has an edit and delete button

        # And she notice that she can edit and delete a question by select of each question

        # She select first question and click the edit button

        # the page updates, and now the show page show a question that
        # she has selects

        # She notice that she can edit a name of question

        # She rename a question to "What is your favortie language programming"

        # # There is still a text box inviting her to add another item. She
        # # enters "Use peacock feathers to make a fly" (Edith is very
        # # methodical)
        # inputbox = self.browser.find_element_by_id('id_new_item')
        # inputbox.send_keys('Use peacock feathers to make a fly')
        # inputbox.send_keys(Keys.ENTER)
        # time.sleep(1)

        # # The page updates again, and now shows both items on her list
        # self.check_for_row_in_list_table('1: Buy peacock feathers')
        # self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')

		# # Edith wonders whether the site will remember her list. Then she sees
		# # that the site has generated a unique URL for her -- there is some
		# # explanatory text to that effect.
        # self.fail('Finish the test!')


if __name__ == '__main__':  
    unittest.main(warnings='ignore')