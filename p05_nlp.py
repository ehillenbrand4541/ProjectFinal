import pandas as pd

# Vectorize
from sklearn.feature_extraction.text import TfidfVectorizer

# Reduce Dimensions
from sklearn.decomposition import TruncatedSVD
from sklearn.decomposition import LatentDirichletAllocation as LDA
from sklearn.decomposition import NMF
from sklearn.preprocessing import normalize


def vectorize_tfidf(text_pd_series, min_df=2, max_df=1.0, print_matrix=True):
    '''
    Returns a sparse doc/word matrix with Tf-Idf Vectorizer from dataframe of standardized text.
    Input text must be a Pandas series of strings.
    Also returns the feature names, which is necessary to run display_topics.
    Example function call: sm_v, feature_names = vectorize_tfidf(df_s)
    '''
    # define series to go into vectorizer
    x = text_pd_series
    # define vectorizer
    cv_tfidf = TfidfVectorizer(min_df=min_df, max_df=max_df)
    # vectorize: convert to sparse matrix
    sparse_matrix = cv_tfidf.fit_transform(x)
    feature_names = cv_tfidf.get_feature_names()
    # print the matrix
    if print_matrix:
        print(pd.DataFrame(sparse_matrix.toarray(), columns=feature_names))
    # return the sparse matrix and feature names
    return sparse_matrix, feature_names

def reduce_dim_lsa(sm, num_topics):
    '''
    Takes: sparse matrix "sm" (the output of vectorize_tfidf).
    Also takes the number of topics "num_topics" (int).
    LDA operation to reduce dimensions of sparse matrix
    Returns dimensionality-reduced doc/topic matrix "rd".
    Also returns lsa.components_ which is necessary to run display_topics.
    Example function call: rd_v, lsa_components = reduce_dim_lsa(sm_v, 40)
    '''
    # define Truncated SVD
    lsa = TruncatedSVD(n_components=num_topics)
    # do LSA on sparse matrix "sm"
    rd = normalize(lsa.fit_transform(sm))
    # return matrix of reduced dimensions
    return rd, lsa.components_

def reduce_dim_lda(sm, num_topics):
    '''
    Takes: sparse matrix "sm" (the output of vectorize_tfidf).
    Also takes the number of topics "num_topics" (int).
    LSA operation to reduce dimensions of sparse matrix
    Returns dimensionality reduced matrix "rd".
    Also returns lsa.components_ which is necessary to run display_topics.
    Example function call: rd_v, model_components = reduce_dim_lda(sm_v, 40)
    '''
    # define Truncated SVD
    lda = LDA(num_topics)
    # do LDA on sparse matrix "sm"
    rd = normalize(lda.fit_transform(sm))
    # return matrix of reduced dimensions
    return rd, lda.components_

def reduce_dim_nmf(sm, num_topics):
    '''
    Takes: sparse matrix "sm" (the output of vectorize_tfidf).
    Also takes the number of topics "num_topics" (int).
    LSA operation to reduce dimensions of sparse matrix
    Returns dimensionality reduced matrix "rd".
    Also returns nmf.components_ which is necessary to run display_topics.
    Example function call: rd_v, model_components = reduce_dim_nmf(sm_v, 40)
    '''
    # define Truncated SVD
    nmf = NMF(num_topics)
    # do NMF on sparse matrix "sm"
    rd = normalize(nmf.fit_transform(sm))
    # return matrix of reduced dimensions
    return rd, nmf.components_

def display_topics(model_components, feature_names, num_top_words, topic_names=None):
    '''
    Takes model components and feature names.
    Prints topics and a given number of their top words: "num_top_words" (int).
    Option to include topic names as a list.
    feature_names = output from vectorize_tfidf
    model_components = output from reduce_dim
    Example function call: display_topics(lsa_components, feature_names, 10)
    '''
    for ix, topic in enumerate(model_components):
        if not topic_names or not topic_names[ix]:
            print("\nTopic ", ix)
        else:
            print("\nTopic: '",topic_names[ix],"'")
        print(", ".join([feature_names[i] for i in topic.argsort()[:-num_top_words - 1:-1]]))
