import math
import json
from parsivar import Normalizer
from parsivar import Tokenizer
from parsivar import FindStems

json_file = open('IR_data_news_12k.json')
data = json.load(json_file)
# number of news
n_news = len(data.keys())

# stop words
persian_stop_word_list = [
                            '‏دیگران', 'همچنان', 'مدت', 'چیز', 'سایر', 'جا', 'طی', 'کل', 'کنونی', 'بیرون', 'مثلا', 'کامل', 'کاملا', 'آنکه', 'موارد', 'واقعی'
                            , 'امور', 'اکنون', 'بطور', 'بخشی', 'تحت' , 'چگونه', 'عدم', 'نوعی', 'حاضر', 'وضع', 'مقابل', 'کنار', 'خویش', 'نگاه', 'درون'
                            ,'زمانی', 'بنابراین', 'تو', 'خیلی', 'بزرگ', 'خودش', 'جز', 'اینجا', 'مختلف', 'توسط', 'نوع', 'همچنین', 'آنجا', 'قبل', 'جناح'
                            ,'اینها', 'طور', 'شاید', 'ایشان', 'جهت', 'طریق', 'مانند', 'پیدا', 'ممکن', 'کسانی', 'جای', 'کسی', 'غیر', 'بی', 'قابل', 'درباره'
                            ,'جدید', 'وقتی', 'اخیر', 'چرا', 'بیش', 'روی', 'طرف', 'جریان', 'زیر', 'آنچه', 'البته', 'فقط', 'چیزی', 'چون', 'برابر', 'هنوز'
                            ,'بخش', 'زمینه', 'بین', 'بدون', 'استفاده', 'همان', 'نشان', 'بسیاری', 'بعد', 'عمل', 'روز', 'اعلام', 'چند', 'آنان', 'بلکه', 'امروز'
                            ,'تمام', 'بیشتر', 'آیا', 'برخی', 'دیگری', 'ویژه', 'گذشته', 'انجام', 'حتی', 'داده', 'راه', 'سوی', 'ولی', 'زمان', 'حال'
                            ,'تنها', 'بسیار', 'یعنی', 'عنوان', 'همین', 'هیچ', 'پیش', 'وی', 'یکی', 'اینکه', 'وجود', 'شما', 'پس', 'چنین', 'میان', 'مورد', 'چه'
                            ,'اگر', 'همه', 'نه', 'دیگر', 'آنها', 'باید', 'هر', 'او', 'ما', 'من', 'تا', 'نیز', 'اما', 'یک', 'خود', 'بر', 'یا' ,'هم' ,'را'
                            ,'این', 'با', 'آن', 'برای', 'و', 'در', 'به', 'که', 'از', 'ای'
                        ]
punctuation_list = ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~']
persian_punctuation_list = ['،']
all_stop_words_list = set(persian_stop_word_list + punctuation_list + persian_punctuation_list)



# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 1: documents preprocessing 

print("1: Preprocessing Documents ...")

my_normalizer = Normalizer()
my_tokenizer = Tokenizer()
my_stemmer = FindStems()

all_news_token_dict = {}

for i in range(0, n_news):
    current_news_info = data[str(i)]
    content_str = current_news_info['content']
    # normalization
    normalized_str = my_normalizer.normalize(content_str)
    # tokenization
    token_list  = my_tokenizer.tokenize_words(normalized_str)
    # omitting stop words, stemming and creating final_token_list
    final_token_list = []
    for j in range(0, len(token_list)):
        if(token_list[j] not in all_stop_words_list):
            final_token_list.append(my_stemmer.convert_to_stem(token_list[j])) 
    # add final_token_list to dictionary
    all_news_token_dict[i] = final_token_list

print("1: Done!")



# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 2: index construction

print("2: Building Index ...")

index = {}

# def print_index():
#     for token in index.keys():
#         print(str(token) + " : " + str(index.get(token)))

def find_term_frequency_in_doc(token, docID):
    n = 0
    token_list = all_news_token_dict[docID]
    for i in range(0, len(token_list)):
        if(token_list[i] == token):
            n = n + 1
    return n

for i in range(0, n_news):
    docID = i
    current_news_token_list = list(set(all_news_token_dict[i]))

    for j in range(0, len(current_news_token_list)):
        current_token = current_news_token_list[j]

        if(current_token in index.keys()):
        # current_token exists in index.keys()  

            n_current_token = index.get(current_token)[0]
            docID_and_tf_dict = index.get(current_token)[1]

            if(docID not in docID_and_tf_dict.keys()):

                tf = find_term_frequency_in_doc(current_token, docID)

                docID_and_tf_dict[docID] = tf
                index.get(current_token)[1] = docID_and_tf_dict

                new_n_current_token = n_current_token + 1
                index.get(current_token)[0] = new_n_current_token

        else: 
        # current_token does not exist in index.keys()
            
            tf = find_term_frequency_in_doc(current_token, docID)
            n_current_token = 1

            docID_and_tf_dict = {}  
            docID_and_tf_dict = {docID : tf}

            final_list_for_token = [n_current_token, docID_and_tf_dict]

            # add new token to positional index
            index[current_token] = final_list_for_token
       
        
# print_index()

print("2: Done!")



# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 3: Create champion lists

print("3: Create champion list ...")

weight_dict = {}
champion_dict = {}
r = 10
k = 10

# def print_weight_dict():
#     for token in weight_dict.keys():
#         print(str(token) + " : " + str(weight_dict.get(token)))

# def print_champion_dict():
#     for token in champion_dict.keys():
#         print(str(token) + " : " + str(champion_dict.get(token)))

for term in index.keys():
    postings_list = index.get(term)
    df_t = postings_list[0]
    docID_and_tf_dict = postings_list[1]
    docID_and_weight_dict = {}
    for docID in docID_and_tf_dict.keys():
        tf_t = docID_and_tf_dict.get(docID)
        # calculate tf_idf weight for term in document
        # tf = 1 + log(tf_td)
        tf = 1 + math.log10(tf_t)
        # idf = log(N/df_t)
        idf = math.log10(n_news/df_t)
        # w_td = tf * idf
        w_td = tf * idf
        docID_and_weight_dict[docID] = w_td

    r_tmp = r
    if(len(docID_and_weight_dict.keys()) < r_tmp):
        r_tmp = len(docID_and_weight_dict.keys())

    sorted_weight_dict = dict(sorted(docID_and_weight_dict.items(), key=lambda x:(x[1], x[0]), reverse=True))
    weight_dict[term] = sorted_weight_dict

    A_list = list(sorted_weight_dict.keys())[0:r_tmp]
    champion_dict[term] = A_list


# print_weight_dict()
# print_champion_dict()

print("3: Done!")



# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 4: answer to query of user

print("4: Answer to Query of User ...")

def find_term_frequency_in_query(token, query_str):
    splited_query = query_str.split(" ")
    n = 0
    for i in range(0, len(splited_query)):
        if(splited_query[i] == token):
            n = n + 1
    return n

def find_doc_length(docID):
    length = 0
    for token in all_news_token_dict.get(docID):
        w_td = weight_dict.get(token).get(docID)
        length += w_td ** 2
    length = math.sqrt(length)
    return length

def print_news(docID, score):
    news_info = data[str(docID)]
    title_str = news_info['title']
    url_str = news_info['url']
    print("docID   : " + str(docID))
    print("title   : " + title_str)
    print("url     : " + url_str)
    print("score   : " + str(score))


while(True):
    print()
    print("===========================================================================")
    query_str = input("Enter your query: ")
    print()

    splited_query = query_str.split(" ")
    
    scores = {}
    for i in range(0, n_news):
        scores[i] = 0

    for query_term in splited_query:
        if(query_term in index.keys()):

            # calculate tf_idf weight for term in query
            tf_tq = find_term_frequency_in_query(query_term, query_str)
            df_t = index.get(term)[0]
            # tf = 1 + log(tf_tq)
            tf = 1 + math.log10(tf_tq)
            # idf = log(N/df_t)
            idf = math.log10(n_news/df_t)
            # w_tq = tf * idf
            w_tq = tf * idf

            champion_list = champion_dict.get(query_term)

            for docID in champion_list:
                w_td = weight_dict.get(query_term).get(docID)
                score = scores.get(docID)
                score = score + (w_td * w_tq)
                scores[docID] = score

    results_dict = {}
    for docID in scores.keys():
        if(scores.get(docID) != 0):
            doc_length = find_doc_length(docID)
            scores[docID] = scores.get(docID) / doc_length
            results_dict[docID] = scores.get(docID)

    sorted_result_dict = dict(sorted(results_dict.items(), key=lambda x:(x[1], x[0]), reverse=True))
    k_tmp = k
    if(len(sorted_result_dict) < k_tmp):
        k_tmp = len(sorted_result_dict)
    k_top_result = dict(list(sorted_result_dict.items())[0:k_tmp])


    print()
    print("<< DocID of all results >>\n")
    print(list(sorted_result_dict.keys()))

    print()
    print("<< Showing results (from 1 to 10) >>")

    for docID in k_top_result.keys():
        score = k_top_result.get(docID) 
        print()
        print_news(docID, score)
        print()    