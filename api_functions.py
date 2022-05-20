from matplotlib.cbook import print_cycles
from pdfminer.high_level import extract_text
import nltk
from psycopg2 import sql, connect
from requests import post

nltk.download('punkt')
nltk.download('stopwords')


def connection():
    try:
        conn = connect(
            dbname='pinops',
            user="postgres",
            host="127.0.0.1",
            password='root',
            port="5432"
        )

        print('Base de données connectée avec succès', conn)
    except Exception as err:
        print("Connexion base de données : ", err)
        conn = None
    return conn


def get_keys(table, conn):
    columns = []

    # declare cursor objects from the connection
    col_cursor = conn.cursor()
    # get from the data base (key cloud)

    # declare an empty list for the column names
    columns = []

    # declare cursor objects from the connection
    col_cursor = conn.cursor()

    # concatenate string for query to get column names
    # SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = 'some_table';
    candidature = '''SELECT keyname FROM public."Keyclouds"'''

    try:
        sql_object = sql.SQL(
            # pass SQL statement to sql.SQL() method
            candidature
        ).format(
            # pass the identifier to the Identifier() method
            sql.Identifier(table)
        )

        # execute the SQL string to get list with col names in a tuple
        col_cursor.execute(sql_object)

        # get the tuple element from the liast
        col_names = (col_cursor.fetchall())

        # print list of tuples with column names

        # iterate list of tuples and grab first element
        for tup in col_names:
            # append the col name string to the list
            columns += [tup[0]]

        # close the cursor object to prevent memory leaks
        col_cursor.close()

    except Exception as err:
        print("get_columns_names ERROR:", err)

    # return the list of column names
    return columns


# you may read the database from a csv file or some other database
SKILLS_DB = [
    'machine learning',
    'data science',
    'python',
    'word',
    'excel',
    'English',
    'mongodb',
    'hbase',
    'css',
    'html',
    'js',
    'ENGLISH'
]


def extract_text_from_pdf(pdf_path):
    return extract_text(pdf_path)


def jaccard_similarity(list1, list2):
    list1 = [x.lower() for x in list1]
    list2 = [x.lower() for x in list2]

    intersection = len(list(set(list1).intersection(list2)))
    union = (len(list1) + len(list2)) - intersection
    return (float(intersection) / union) * 100


def extract_skills(input_text, COLUMNS_DB):

    stop_words = set(nltk.corpus.stopwords.words('english'))
    word_tokens = nltk.tokenize.word_tokenize(input_text)

    # remove the stop words
    filtered_tokens = [w for w in word_tokens if w not in stop_words]

    # remove the punctuation
    filtered_tokens = [w for w in word_tokens if w.isalpha()]

    # generate bigrams and trigrams (such as artificial intelligence)
    bigrams_trigrams = list(
        map(' '.join, nltk.everygrams(filtered_tokens, 2, 3)))

    # we create a set to keep the results in.
    found_skills = set()

    # we search for each token in our skills database
    for token in filtered_tokens:
        if token.lower() in COLUMNS_DB:
            found_skills.add(token)

    # we search for each bigram and trigram in our skills database
    for ngram in bigrams_trigrams:
        if ngram.lower() in COLUMNS_DB:
            found_skills.add(ngram)

    return found_skills
