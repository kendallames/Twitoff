from sklearn.linear_model import LogisticRegression
from .models import User
import numpy as np
from .twitter import vectorize_tweet




def predict_user(user0, user1, hypo_tweet_text):
    
    user0 = User.query.filter(User.username == user0_name)
    user1 = User.query.filter(User.username == user1_name)

    user0_vects = np.array([tweet.vect for tweet in user0.tweets])
    user1_vects = np.array([tweet.vect for tweet in user1.tweets])

    # X Matrix for training the logistic regression
    vects = np.vstack([user0_vects, user1_vects])

    # 1D Numpy Arrays 
    zeroes = np.zeroes(len(user0.tweets))
    ones = np.ones(len(user1.tweets))

    # Y Vector (target) for training the logistic regression
    labels = np.concatenate([zeroes, ones])

    # instantiate our logistic regression
    log_reg = LogisticRegression()

    # train our logistic regression
    log_reg.fit(vects, labels)

    # vectorize (get the word embeddings for)
    # our hypothetical tweet text
    hypo_tweet_vect = vectorize_tweet(hypo_tweet_text)

    # get a prediction for which
    prediction = log_reg.predict(hypo_tweet_vect.reshape(1, -1))

