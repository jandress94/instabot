import time
import argparse
from tqdm import tqdm as tqdm
from datetime import datetime
import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


PAGE_LOAD_WAIT_PROP = 1. / 30


class InstagramBot:
    def __init__(self, chromedriver_path):
        self.browser = webdriver.Chrome(chromedriver_path)

    def sign_in(self, username, password):
        self.browser.get('https://www.instagram.com/accounts/login/')
        time.sleep(2)

        username_input = self.browser.find_elements_by_css_selector('form input')[0]
        password_input = self.browser.find_elements_by_css_selector('form input')[1]

        username_input.send_keys(username)
        password_input.send_keys(password)
        password_input.send_keys(Keys.ENTER)

    def follow_account(self, account, page_load_wait_time=2):

        self.browser.get('https://www.instagram.com/%s' % account)

        buttons = self.browser.find_elements_by_css_selector('button')
        time.sleep(page_load_wait_time)

        if len(buttons) == 0:
            print('Account "%s" does not seem to exist.' % account)
            return False

        button_texts = [b.text for b in buttons]

        try:
            follow_button_index = button_texts.index("Follow")
            print('Following account "%s"' % account)
            # buttons[follow_button_index].click()
            return True

        except ValueError as ve:
            print('You seem to already follow the account "%s"' % account)
            return False


def bulk_follow(chromedriver_path, username, password, account_list_file, processed_users_filename, seconds_per_req, req_per_day):
    bot = InstagramBot(chromedriver_path)

    print("Signing In")
    bot.sign_in(username, password)

    input("At this point, we should be signed in to the account. Press ENTER when ready...")

    try:
        with open(processed_users_filename, 'r') as fp:
            processed_usernames = set(u.strip() for u in fp)
    except FileNotFoundError as fnfe:
        processed_usernames = set()

    with open(account_list_file, 'r') as fp:
        usernames = set(u.strip() for u in fp)
        usernames -= processed_usernames

    print("Found %d usernames to follow." % len(usernames))

    request_count = 0
    for u in tqdm(usernames):
        page_load_wait_time = seconds_per_req * PAGE_LOAD_WAIT_PROP
        is_request_sent = bot.follow_account(u, page_load_wait_time=page_load_wait_time)

        processed_usernames.add(u)
        with open(processed_users_filename, 'a') as pufp:
            pufp.write(u + "\n")

        if not is_request_sent:
            continue

        request_count += 1
        if request_count >= req_per_day:
            print("Max number of requests sent today.")
            seconds_to_wait = 24*60*60 - (request_count - 1) * seconds_per_req
            request_count = 0
        else:
            seconds_to_wait = seconds_per_req - page_load_wait_time

        print("The time is %s, waiting %d seconds before attempting next account." % (str(datetime.now()), int(seconds_to_wait)))
        time.sleep(seconds_to_wait)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Follow all the instagram accounts listed in a file",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--username", type=str, required=True,
                        help="The username or email of the account that will do the following.")
    parser.add_argument("--password", type=str, required=True,
                        help="The password of the account that will do the following. "
                             "Note: if the password contains an exclamation point, "
                             "it must be surrounded by single quotes.")
    parser.add_argument("--account_list_file", type=str, required=True,
                        help="The accounts that will be followed, one per line.")
    parser.add_argument("--processed_users_filename", type=str, required=False, default="processed_usernames.txt",
                        help="A file where the processed users will be written. "
                             "This makes processing faster if the job is restarted.")
    parser.add_argument("--req_per_hour", type=int, required=False, default=20,
                        help="The number of follow requests to send per hour.")
    parser.add_argument("--req_per_day", type=int, required=False, default=150,
                        help="The maximum number of follow requests to send in a single day.")
    parser.add_argument("--chromedriver_path", type=str, required=False, default=os.path.join(os.getcwd(), 'chromedriver'),
                        help="The path to the chromedriver executable.")

    args = parser.parse_args()

    seconds_per_req = 3600 / args.req_per_hour

    bulk_follow(args.chromedriver_path,
                args.username,
                args.password,
                args.account_list_file,
                args.processed_users_filename,
                seconds_per_req,
                args.req_per_day)
