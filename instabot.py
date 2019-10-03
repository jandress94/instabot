import time
import argparse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class InstagramBot:
    def __init__(self):
        self.browser = webdriver.Chrome('/Users/jim/Downloads/chromedriver')

    def sign_in(self, username, password):
        self.browser.get('https://www.instagram.com/accounts/login/')
        time.sleep(2)

        username_input = self.browser.find_elements_by_css_selector('form input')[0]
        password_input = self.browser.find_elements_by_css_selector('form input')[1]

        username_input.send_keys(username)
        password_input.send_keys(password)
        password_input.send_keys(Keys.ENTER)

    def follow_account(self, account, load_to_click_time=2):

        self.browser.get('https://www.instagram.com/%s' % account)

        buttons = self.browser.find_elements_by_css_selector('button')

        if len(buttons) == 0:
            print('Account "%s" does not seem to exist.' % account)
            return

        button_texts = [b.text for b in buttons]

        try:
            follow_button_index = button_texts.index("Follow")
            print('Following account "%s"' % account)
            time.sleep(load_to_click_time)
            buttons[follow_button_index].click()

        except ValueError as ve:
            print('You seem to already follow the account "%s"' % account)


def bulk_follow(username, password, account_list_file):
    bot = InstagramBot()
    bot.sign_in(username, password)

    with open(account_list_file, 'r') as fp:
        for account in fp:
            time.sleep(4)
            bot.follow_account(account.strip())

    input('done, press SPACE to exit')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Follow all the instagram accounts listed in a file")
    parser.add_argument("--username", type=str, required=True,
                        help="The username or email of the account that will do the following.")
    parser.add_argument("--password", type=str, required=True,
                        help="The password of the account that will do the following. "
                             "Note: if the password contains an exclamation point, "
                             "it must be surrounded by single quotes.")
    parser.add_argument("--account_list_file", type=str, required=True,
                        help="The accounts that will be followed, one per line.")

    args = parser.parse_args()

    bulk_follow(args.username, args.password, args.account_list_file)
