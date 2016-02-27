# Twitter Troll Project

Final project for Data Science Postgrade in the University of Barcelona. The main goal is to create a model where we detect if a twitter user is a Troll or not, understanding by troll a person who sows discord on the Internet by starting arguments or upsetting people, by posting inflammatory, extraneous, or off-topic messages in an online community (such as a newsgroup, forum, chat room, or blog) with the deliberate intent of provoking readers into an emotional response or of otherwise disrupting normal on-topic discussion, often for their own amusement or interest.

We divide the trolls in the next categories:

- Qualitative:
    - *Drama Queen*
    - *Haters*
- Quantitative:
    - *Bots*
    - *Spammer*


## 1. Getting the data.

With a dictionary of twitter API Tokens in a `keys.py` file we create a Python thread for each Token key that requests all the data from a list of users.
The users are randomly picked using the Twitters Stream API, all over USA and filtering to the ones written in English.

`python3 populate_db.pt &` was run during 2 whole days.

## 2. Analyzing the Data.

In order to create an easier to analyze table we processed all the data obtained and stored in the MongoDB and we processed it and stored it in a SQL table. That way It's easier to go over.

Added variables:

#### Parameters
- number_of_tweets
- account_old
- language
    - sistema
    - tweets
- Mentions
    - Done by user
    - Done to user
    - Answers
- Followers
    - account_old
    - language
- total hashtags
- tweets with hashtag
- Tweets
    - time
    - geo
    - number of hashtags
    - number of likes
    - number of retweets
    - answers
​
​
#### Parametros en C2
- original content / retweet
- Links / tweet
- `int` mentions
- own language / followers
- own language / followees
- Tweets / day
- period of tweet
- number followers with less than 30 followers
- account_old
- trending_topic hashtags
- likes tweets in tweets with mentions
- answers per tweet
- strange hours ?
- Verified followers
- Followers / followees
​


## 3. Creating a model.

## 4. Creating a webApp.


## License

The MIT License (MIT)

Copyright (c) 2016 Alejandro Fernández Piqué, Albert Trias Creus, Eduard Ribas Fernández, Gabriel de Maeztu Pontevia

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
