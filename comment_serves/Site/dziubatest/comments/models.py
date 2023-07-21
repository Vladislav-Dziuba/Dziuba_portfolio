from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context


import nltk
import numpy as np
import pandas as pd
# from tensorflow.keras.layers import Dense, LSTM, Input, Dropout, Embedding
# from tensorflow.keras.models import Sequential, load_model
# from tensorflow.keras.optimizers import Adam
# from tensorflow.keras.preprocessing.text import Tokenizer, text_to_word_sequence
# from tensorflow.keras.preprocessing.sequence import pad_sequences



from nltk.corpus import stopwords
nltk.download('stopwords')
stopwords_set = set(stopwords.words('english'))


from nltk.stem import WordNetLemmatizer
nltk.download('omw-1.4')
nltk.download('wordnet')

wordnet_lemmatizer = WordNetLemmatizer()


score_star=[(1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5'),(6,'6'),(7,'7'),(8,'8'),(9,'9'),(10,'10')]


class Comment(models.Model):
    title = models.CharField(max_length=200,verbose_name='Заголовок')
    slug = models.SlugField(max_length=200, unique=True, db_index=True, verbose_name='URL')
    content = models.TextField(blank=True, verbose_name='Текст отзыва',validators=[
        RegexValidator(
            regex='^[a-zA-Z0-9 !?;:,.<>()@"#№$-_|&*-+/\']*$',
            message='Отзыв должен быть на английском языке',
            code='invalid_username'
        ),
    ])
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Бинарная оценка')
    score = models.CharField(max_length=20,blank=True,null=True,verbose_name='оценка по 10')
    pred = models.CharField(max_length=20,blank=True,null=True,verbose_name='Распознавание')
    # status_LSTM = models.CharField(max_length=20,blank=True,null=True,verbose_name='Распознавание LSTM')
    # score_LSTM = models.CharField(max_length=20,blank=True,null=True,verbose_name='оценка по 10')


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post',kwargs={'post_slug': self.slug})

    def save(self,*args,**kwargs):


        regression = joblib.load('ml_model/ml_model.joblib')
        vectorizer = joblib.load('ml_model/vectorizer_model.joblib')

        without_stop = [i for i in self.content.split(' ') if i not in stopwords_set]
        lemm = ' '.join([wordnet_lemmatizer.lemmatize(word) for word in without_stop])
        tf = vectorizer.transform(pd.Series(lemm).tolist())

        predpred = regression.predict(tf)
        if predpred[0]==0:
            self.pred = 'Отрицательный'
        else:
            self.pred = 'Положительный'

        pred_proba = regression.predict_proba(tf)
        if pred_proba[0][1] <0.2:
            self.score = '2/10'
        elif 0.2 < pred_proba[0][1] < 0.3:
            self.score = '3/10'
        elif 0.3 < pred_proba[0][1] < 0.4:
            self.score = '4/10'

        elif 0.5 < pred_proba[0][1] < 0.6:
            self.score = '7/10'
        elif 0.7 < pred_proba[0][1] < 0.9:
            self.score = '8/10'
        elif 0.96 < pred_proba[0][1] :
            self.score = '9/10'
        else:
            self.score = '5/10'


        ### пришлось вырезать этот кусок из за несогласованности tensorflow с сервисом beget
        # lstm = load_model('ml_model/best_model_lstm.h5')
        # token = joblib.load('ml_model/tokenizer.joblib')
        #
        #
        # data2 = token.texts_to_sequences([self.content.lower()])
        #
        # data_pad2 = pad_sequences(data2, maxlen=150)
        #
        # res = lstm.predict(data_pad2)


        # if np.argmax(res) == 0:
        #     self.status_LSTM = 'Положительный'
        #     if 0.6 < res[0][0] < 0.75:
        #         self.score_LSTM = '7/10'
        #     elif 0.75 < res[0][0] < 0.9:
        #         self.score_LSTM = '8/10'
        #     else:
        #         self.score_LSTM = '9/10'
        # else:
        #     self.status_LSTM = 'Отрицательный'

        return super().save(*args,**kwargs)


    class Meta:
        verbose_name = 'Отзывы о фильмах'
        verbose_name_plural = 'Отзывы о фильмах'
        ordering = ['-time_create', 'title']



class Category(models.Model):
    name = models.CharField(max_length=50, db_index=True,verbose_name='Категория')
    slug = models.SlugField(max_length=200, unique=True, db_index=True, verbose_name='URL')
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category',kwargs={'cat_id': self.pk})


    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['id']

