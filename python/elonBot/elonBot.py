import re
import tweepy
import time
import random
from datetime import date
from PIL import Image, ImageDraw


class ElonBot:
    print('this is my first twitter bot')

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)



    MORSE_CODE = {'A': '.-', 'B': '-...', 'C': '-.-.',
            'D': '-..', 'E': '.', 'F': '..-.',
            'G': '--.', 'H': '....', 'I': '..',
            'J': '.---', 'K': '-.-', 'L': '.-..',
            'M': '--', 'N': '-.', 'O': '---',
            'P': '.--.', 'Q': '--.-', 'R': '.-.',
            'S': '...', 'T': '-', 'U': '..-',
            'V': '...-', 'W': '.--', 'X': '-..-',
            'Y': '-.--', 'Z': '--..',

            '0': '-----', '1': '.----', '2': '..---',
            '3': '...--', '4': '....-', '5': '.....',
            '6': '-....', '7': '--...', '8': '---..',
            '9': '----.'
            }

    list_of_tweets = []
    while True:
        def get_elons_tweet(api):
            """Get Elon's last tweet by user ID"""
            tweets = tweepy.Cursor(api.user_timeline, id="44196397", since=date.today(), tweet_mode='extended').items(1)

            # remove all invalid characters
            elons_last_tweet = [re.sub('[^A-Za-z0-9]+', ' ', tweet.full_text) for tweet in tweets]

            # re-try until it returns a value - tweepy API fails to return the tweet sometimes
            while not elons_last_tweet:
                tweets = tweepy.Cursor(api.user_timeline, id="44196397", since=date.today(),
                                       tweet_mode='extended').items(1)
                elons_last_tweet = [re.sub('[^A-Za-z0-9]+', ' ', tweet.full_text) for tweet in tweets]
            return elons_last_tweet[0]
        print(get_elons_tweet(api))

        final_tweet = ''
        elons_last_tweet = get_elons_tweet(api)

        count = 1
        for element in elons_last_tweet:
            try:
                print(MORSE_CODE[element.upper()])
                final_tweet += MORSE_CODE[element.upper()] + ' '
                if count % 30 == 0:
                    final_tweet += '\n'
                count += 1
            except:
                pass

        final_word = 'Elon Musk said in Morse code: \n' + final_tweet
        print(final_word)

        print(len(final_word))

        list_of_colors = ['orange', 'yellow', 'white', 'red']
        if final_tweet not in list_of_tweets:
            W, H = (800, 300)
            msg = final_word

            im = Image.new("RGBA", (W, H), random.choice(list_of_colors))
            draw = ImageDraw.Draw(im)
            w, h = draw.textsize(msg)
            draw.text(((W - w) / 2, (H - h) / 2), msg, fill="black")
            im.save("hello.png", "PNG")
            api.update_with_media('hello.png')
            list_of_tweets.append(final_tweet)
        time.sleep(24.0 * 60.0 * 60.0)