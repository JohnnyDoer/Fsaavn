import os
import time
import pickle

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

SCROLL_PAUSE_TIME = 5
LOAD_PAUSE_TIME = 5

class Saavn:
    # Start automated firefox.
    def __init__(self):
        self.driver = webdriver.Firefox()
        print("Firefox started.")


    # Close browser on completion.
    def closeBrowser(self):
        self.driver.close()
        print("Browser closed.")


    # Login to Saavn.
    def login(self):
        print("Logging in.")
        driver = self.driver
        driver.get("https://www.jiosaavn.com/login")
        input("Press enter after logging in... ")
        pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb")) # Save all your cookies.


    # Get all the songs in your list.
    def get_songs(self):
        print("Getting songs.")
        driver = self.driver
        driver.get("https://www.jiosaavn.com/")

        cookies = pickle.load(open("cookies.pkl", "rb"))
        for cookie in cookies:
            driver.add_cookie(cookie)

        driver.get("https://www.jiosaavn.com/my-music/songs")

        time.sleep(5)

        # Scroll all the way to the end.
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            time.sleep(SCROLL_PAUSE_TIME)

            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        song_ref = driver.find_elements_by_xpath('//a[@class="u-color-js-gray"]')
        print("Total songs found:", len(song_ref))

        # Get all the links of the songs.
        songs = [a.get_attribute("href") for a in song_ref]

        # Save all the links.
        pickle.dump(songs, open("songs.pkl", "wb"))
        

    # Add all the songs to a playlist.
    def songs_to_playlist(self):
        print("Adding songs to playlist.")
        driver = self.driver
        driver.get("https://www.jiosaavn.com/")

        cookies = pickle.load(open("cookies.pkl", "rb"))
        for cookie in cookies:
            driver.add_cookie(cookie)

        songs = pickle.load(open("songs.pkl", "rb"))

        for song in songs:
            while True:
                try:
                    driver.get(str(song))
                    time.sleep(LOAD_PAUSE_TIME)
                    driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[1]/div/main/div[2]/figure/figcaption/div/p[3]/span/i").click()
                    driver.find_element_by_xpath("/html/body/div[1]/div[2]/aside[3]/div/div[2]/div/div/nav/ul/li[4]/span").click()
                    driver.find_element_by_xpath("/html/body/div[1]/div[2]/aside[3]/div/div[2]/div/div/nav/ul/li[4]/div/nav[2]/ul/li[2]/a").click()
                    time.sleep(LOAD_PAUSE_TIME)
                    break
                except:
                    continue



def main():
    user = Saavn()

    if not os.path.exists("cookies.pkl"):
        user.login()

    if not os.path.exists("songs.pkl"):
        user.get_songs()

    user.songs_to_playlist()

    user.closeBrowser()


main()