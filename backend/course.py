import pandas as pd
df_org=pd.read_csv('Courser.csv')
df=df_org.copy()
df.drop(['University','Difficulty Level','Course Rating','Course URL','Course Description'], axis=1,inplace=True)
from sklearn.feature_extraction.text import TfidfVectorizer


tfv = TfidfVectorizer(min_df=3,  max_features=None,
            strip_accents='unicode', analyzer='word',token_pattern=r'\w{1,}',
            ngram_range=(1, 3),
            stop_words = 'english')

# Filling NaNs with empty string
df['cleaned'] = df['Skills'].fillna('')
tfv_matrix = tfv.fit_transform(df['cleaned'])
tm=tfv_matrix
import scipy.sparse
tfidfcheck=pd.DataFrame.sparse.from_spmatrix(tm)
from sklearn.metrics.pairwise import sigmoid_kernel

# Compute the sigmoid kernel
sig = sigmoid_kernel(tfv_matrix, tfv_matrix)
indices = pd.Series(df.index, index=df['Course Name']).drop_duplicates()
list(enumerate(sig[indices['Write A Feature Length Screenplay For Film Or Television']]))[0:25]
sorted(list(enumerate(sig[indices['Write A Feature Length Screenplay For Film Or Television']])), key=lambda x: x[1], reverse=True)[0:25]
def give_rec(title, sig=sig):
    # Get the index corresponding to given course
    idx = indices[title]

    # Get the pairwsie similarity scores with given course with every available course in the data set
    sig_scores = list(enumerate(sig[idx]))

    # Sort the recommended courses
    sig_scores = sorted(sig_scores, key=lambda x: x[1], reverse=True)

    # Scores of the 10 most similar courses
    sig_scores = sig_scores[1:11]

    # get courses indices for top 10 recommended courses
    course_indices = [i[0] for i in sig_scores]

    # Top 10 most similar courses
    return df_org.iloc[course_indices]

import difflib
namelist=df['Course Name'].tolist()
word='voices of social change'
simlist=difflib.get_close_matches(word, namelist)

# print(namelist)

try:
        findf=give_rec(simlist[0])
        findf=findf.reset_index(drop=True)
except:
        findf = pd.DataFrame()

if findf.empty:
        ms='Sorry! we did not find any matching courses, Try adding more keywords in your search.'
        ht=' '
else:
        ht='done'
        ms='Here are some recommendations :'



print(namelist)

