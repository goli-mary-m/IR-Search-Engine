import json
import string
from parsivar import Normalizer
from parsivar import Tokenizer
from parsivar import FindStems
import colorama
from colorama import Fore

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
# 1-1: documents preprocessing 

print("1-1: Preprocessing Documents ...")

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

print("1-1: Done!")

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 1-2: positional index construction

print("1-2: Building a Positional Index ...")

positional_index = {}

# def print_positional_index():
#     for token in positional_index.keys():
#         print(str(token) + " : " + str(positional_index.get(token)))

def find_positions_of_token_in_doc(token, docID):
    positions_list = []
    token_list = all_news_token_dict[docID]
    for i in range(0, len(token_list)):
        if(token_list[i] == token):
            positions_list.append(i)
    return positions_list

for i in range(0, n_news):
    docID = i
    current_news_token_list = all_news_token_dict[i]
    for j in range(0, len(current_news_token_list)):
        current_token = current_news_token_list[j]

        if(current_token in positional_index.keys()):
        # current_token exists in positional_index.keys()  

            n_current_token = positional_index.get(current_token)[0]
            docID_and_positions_dict = positional_index.get(current_token)[1]

            if(docID not in docID_and_positions_dict.keys()):

                positions_list = find_positions_of_token_in_doc(current_token, docID)
                docID_and_positions_dict[docID] = positions_list
                positional_index.get(current_token)[1] = docID_and_positions_dict

                new_n_current_token = n_current_token + len(positions_list)
                positional_index.get(current_token)[0] = new_n_current_token


        else: 
        # current_token does not exist in positional_index.keys()
            
            positions_of_token = find_positions_of_token_in_doc(current_token, docID)
            n_current_token = len(positions_of_token)

            docID_and_positions_dict = {}
            docID_and_positions_dict = {docID : positions_of_token}

            final_list_for_token = [n_current_token, docID_and_positions_dict]

            # add new token to positional index
            positional_index[current_token] = final_list_for_token
        
# print_positional_index()

print("1-2: Done!")

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 1-3: answer to query of user

print("1-3: Answer to Query of User ...")

# find common docIDs between two lists
def merge(docID_list_1, docID_list_2):
    result = []
    index_1 = 0
    index_2 = 0
    while(index_1 < len(docID_list_1) and index_2 < len(docID_list_2)):
        if(docID_list_1[index_1] == docID_list_2[index_2]):
            result.append(docID_list_1[index_1])
            index_1 += 1
            index_2 += 1
        elif(docID_list_1[index_1] < docID_list_2[index_2]):
            index_1 += 1
        else:
            index_2 += 1
    return result


# finds places where the two terms appear within k words of each other 
# output = list of [docID, pos1, pos2]
def positional_merge(docID_positions_dict_1, docID_positions_dict_2, k):
    result = []
    index_1 = 0
    index_2 = 0
    while(index_1 < len(docID_positions_dict_1) and index_2 < len(docID_positions_dict_2)):
        if(list(docID_positions_dict_1.keys())[index_1] == list(docID_positions_dict_2.keys())[index_2]):
            l = []
            index_positions_1 = 0
            index_positions_2 = 0
            positions_1 = list(docID_positions_dict_1.values())[index_1]
            positions_2 = list(docID_positions_dict_2.values())[index_2]
            while(index_positions_1 < len(positions_1)):
                while(index_positions_2 < len(positions_2)):
                    if(abs(positions_1[index_positions_1] - positions_2[index_positions_2]) <= k ):
                        l.append(positions_2[index_positions_2])
                    elif(positions_2[index_positions_2] > positions_1[index_positions_1]):
                        break
                    index_positions_2 += 1
                while(len(l) > 0 and abs(l[0] - positions_1[index_positions_1]) > k):
                    del l[0]
                for pos in l:
                    docID_1 = list(docID_positions_dict_1.keys())[index_1]
                    result.append([docID_1, positions_1[index_positions_1], pos])
                index_positions_1 += 1
            index_1 += 1
            index_2 += 1
        elif(list(docID_positions_dict_1.keys())[index_1] < list(docID_positions_dict_2.keys())[index_2]):
            index_1 += 1
        else:
            index_2 += 1
    return result


def print_news(docID):
    news_info = data[str(docID)]
    title_str = news_info['title']
    url_str = news_info['url']
    print("docID   : " + str(docID))
    print("title   : " + title_str)
    print("url     : " + url_str)


while(True):
    print()
    print("===========================================================================")
    query_str = input("Enter your query: ")
    print()

    splited_query = query_str.split(" ")
    phrase_part_of_query = ""
    not_part_of_query = ""
    other_part_of_query = ""

    flag_find_phrase_part  = False
    flag_not_find_not_part = False

    final_results = []

    for i in range(0, len(splited_query)):

        # find phrase part
        if(splited_query[i].startswith("\"")):
            if(splited_query[i].endswith("\"")):
                phrase_part_of_query = splited_query[i]
                phrase_part_of_query = phrase_part_of_query[1:len(phrase_part_of_query)-1]  # phrase without "" 
            else:
                flag = False
                for i_tmp in range(i+1, len(splited_query)):
                    if(splited_query[i_tmp].endswith("\"")):
                        flag = True
                        for j in range(i, i_tmp+1):
                            phrase_part_of_query += splited_query[j] + " "
                        phrase_part_of_query = phrase_part_of_query[1:len(phrase_part_of_query)-2]  # phrase without ""    
                        break  
                if(flag == False):
                    print("Error in input! -> phrase")            

        # find NOT part
        if(splited_query[i].startswith("!")):
            if(splited_query[i] != "!"):
                print("Error in input! -> NOT")  
            else:
                not_part_of_query = splited_query[i+1]

        # find other part
        other_part_of_query = query_str.replace("\""+phrase_part_of_query+"\"", "")
        other_part_of_query = other_part_of_query.replace("! "+not_part_of_query , "")   


    # normalization
    normalized_phrase_part_str = my_normalizer.normalize(phrase_part_of_query)
    normalized_not_part_str = my_normalizer.normalize(not_part_of_query)
    normalized_other_part_str = my_normalizer.normalize(other_part_of_query)
    # tokenization
    phrase_part_token_list  = my_tokenizer.tokenize_words(normalized_phrase_part_str)
    not_part_token_list  = my_tokenizer.tokenize_words(normalized_not_part_str)
    other_part_token_list  = my_tokenizer.tokenize_words(normalized_other_part_str)
    # omitting stop words, stemming, creating final_token_list
    final_phrase_part_token_list = []
    final_not_part_token_list = []
    final_other_part_token_list = []

    for i in range(0, len(phrase_part_token_list)):
        if(phrase_part_token_list[i] not in all_stop_words_list):
            final_phrase_part_token_list.append(my_stemmer.convert_to_stem(phrase_part_token_list[i])) 
    for i in range(0, len(not_part_token_list)):
        if(not_part_token_list[i] not in all_stop_words_list):
            final_not_part_token_list.append(my_stemmer.convert_to_stem(not_part_token_list[i])) 
    for i in range(0, len(other_part_token_list)):
        if(other_part_token_list[i] not in all_stop_words_list):
            final_other_part_token_list.append(my_stemmer.convert_to_stem(other_part_token_list[i]))  




    # ====================================================================================== 
    # phrase-part
    # ====================================================================================== 

    # find docIDs for phrase part

    flag_end = False

    phrase_part_tokens_docIDs_pos_dict = {}
    final_result_phrase_part = []
    result_dict = {}
    if(len(final_phrase_part_token_list) > 0):
        for i in range(0, len(final_phrase_part_token_list)):
            if(flag_end == True):
                break
            else:
                current_token = final_phrase_part_token_list[i]
                if(current_token in positional_index.keys()):
                    current_token_docIDs_pos_dict = positional_index[current_token][1]
                    phrase_part_tokens_docIDs_pos_dict[current_token] = current_token_docIDs_pos_dict
                else:
                # this token dose not exist in dictionary => no result for user query
                    print(Fore.RED + "this token doesn't exist in dictionary! -> " + str(current_token))    
                    print(Fore.BLACK)
                    flag_end = True 

        # merge
        if(flag_end == False):
            if(len(phrase_part_tokens_docIDs_pos_dict) > 0):
                first_token = list(phrase_part_tokens_docIDs_pos_dict.keys())[0]
                first_token_docIDs_pos_dict = phrase_part_tokens_docIDs_pos_dict[first_token] 
                # initialize result_list
                result_dict = first_token_docIDs_pos_dict

            for i in range(1, len(phrase_part_tokens_docIDs_pos_dict)):       
                current_token = final_phrase_part_token_list[i]
                current_token_docIDs_pos_dict = phrase_part_tokens_docIDs_pos_dict[current_token]
                positional_merge_result = positional_merge(result_dict, current_token_docIDs_pos_dict, 1)

                result_dict = {}
                for j in range(0, len(positional_merge_result)):
                    current_list = positional_merge_result[j]
                    docID = current_list[0]
                    pos_first_word = current_list[1]
                    pos_second_word = current_list[2]
                    if(pos_second_word > pos_first_word):
                        if(docID in result_dict.keys()):
                            tmp_docID_list = result_dict[docID]
                            tmp_docID_list.append(pos_second_word)
                            result_dict[docID] = tmp_docID_list    
                        else:
                            tmp_docID_list = []
                            tmp_docID_list.append(pos_second_word)
                            result_dict[docID] = tmp_docID_list     

            final_result_phrase_part = list(result_dict.keys())

    if(len(final_phrase_part_token_list) > 0):
        if(len(final_result_phrase_part) > 0):
            flag_find_phrase_part = True
        else:
            flag_find_phrase_part = False  
            print("can't find result for user query -> because phrase-part")   
    else:
        flag_find_phrase_part = True              


    # ====================================================================================== 
    # not-part
    # ======================================================================================

    # find docIDs for not part

    not_part_tokens_docIDs_dict = {}
    final_result_not_part = []

    if(len(final_not_part_token_list) > 0):
        for i in range(0, len(final_not_part_token_list)):
            if(flag_end == True):
                break
            else:
                current_token = final_not_part_token_list[i]
                if(current_token in positional_index.keys()):
                    current_token_docIDs_list = list(positional_index[current_token][1].keys())
                    not_part_tokens_docIDs_dict[current_token] = current_token_docIDs_list 
                else:
                    print(Fore.RED + "this token doesn't exist in dictionary! -> " + str(current_token)) 
                    print(Fore.BLACK)       

        if(flag_end == False):

            if(len(not_part_tokens_docIDs_dict) > 0):
                first_token = list(not_part_tokens_docIDs_dict.keys())[0]
                first_token_docIDs_list = not_part_tokens_docIDs_dict[first_token] 
                # initialize result_list
                result_list = []

            for j in range(0, n_news):
                if(j not in first_token_docIDs_list):
                    result_list.append(j)

            for i in range(1, len(not_part_tokens_docIDs_dict)):
                current_token = final_not_part_token_list[i]
                current_token_docIDs_list = not_part_tokens_docIDs_dict[current_token]

                tmp_result_list = []
                for j in range(0, len(result_list)):
                    if(result_list[j] not in current_token_docIDs_list):
                        tmp_result_list.append(result_list[j])
                result_list = tmp_result_list
            
            final_result_not_part = result_list  

    if(len(final_not_part_token_list) > 0):
        if(len(final_result_not_part) > 0):
            flag_not_find_not_part = True
        else:
            flag_not_find_not_part = False 
            print("can't find result for user query -> because not-part")    
    else:
        flag_not_find_not_part = True          


    # ====================================================================================== 
    # merge result -> phrase-part, not-part
    # ======================================================================================

    flag_find_result_merge = True

    if(flag_find_phrase_part == True and flag_not_find_not_part == True):
        if(len(final_result_phrase_part) > 0):
            if(len(final_result_not_part) > 0):
                merged_result_phrase_not = merge(final_result_phrase_part, final_result_not_part)
                if(len(merged_result_phrase_not) == 0):
                    flag_find_result_merge = False
            else:
                merged_result_phrase_not = final_result_phrase_part
        else:
            if(len(final_result_not_part) > 0):
                merged_result_phrase_not = final_result_not_part
            else:
                merged_result_phrase_not = []
    else:
        merged_result_phrase_not = []


    # ====================================================================================== 
    # other-part
    # ======================================================================================

    # find docIDs for other part

    other_part_tokens_docIDs_dict = {}
    final_result_other_part = []
    final_result_some_other_part = []

    if(flag_find_phrase_part == True and flag_not_find_not_part == True and flag_find_result_merge == True): #continue ... [finding other-part...]

        if(len(final_other_part_token_list) > 0):
            for i in range(0, len(final_other_part_token_list)):
                current_token = final_other_part_token_list[i]
                if(current_token in positional_index.keys()):
                    current_token_docIDs_list = list(positional_index[current_token][1].keys())
                    other_part_tokens_docIDs_dict[current_token] = current_token_docIDs_list
                    final_result_some_other_part = list(set(final_result_some_other_part + current_token_docIDs_list))
                    final_result_some_other_part.sort()
                else:
                    print(Fore.RED + "this token doesn't exist in dictionary! -> " + str(current_token))    
                    print(Fore.BLACK)

            # merge
            if(len(other_part_tokens_docIDs_dict) > 0):
                first_token = list(other_part_tokens_docIDs_dict.keys())[0]
                first_token_docIDs_list = other_part_tokens_docIDs_dict[first_token] 
                # initialize result_list
                result_list = first_token_docIDs_list

            for i in range(1, len(other_part_tokens_docIDs_dict)):       
                current_token = list(other_part_tokens_docIDs_dict.keys())[i]
                current_token_docIDs_list = other_part_tokens_docIDs_dict[current_token] 
                result_list = merge(result_list, current_token_docIDs_list)

            final_result_other_part = result_list
            
            for res in final_result_some_other_part:
                if(res in final_result_other_part):
                    final_result_some_other_part.remove(res)


        # ====================================================================================== 
        # final merge result -> merged(phrase-part, not-part), other-part
        # ======================================================================================
        
        if(len(final_result_other_part) > 0):
            if(len(merged_result_phrase_not) > 0):
                final_results = merge(merged_result_phrase_not, final_result_other_part)
            else:
                final_results = final_result_other_part

            if(len(final_result_some_other_part) > 0):
                if(len(merged_result_phrase_not) > 0):
                    tmp_final_results = merge(merged_result_phrase_not, final_result_some_other_part)
                    final_results = list(final_results + tmp_final_results)
                else:
                    final_results = list(final_results + final_result_some_other_part)
        else:
            if(len(final_result_some_other_part) > 0):
                if(len(merged_result_phrase_not) > 0):
                    final_results = merge(merged_result_phrase_not, final_result_some_other_part)
                else:
                    final_results = final_result_some_other_part    
            else:
                final_results = merged_result_phrase_not


    # print results
    print("==================================================================")
    print("[Tokens]")
    print("phrase-part:                           " + str(final_phrase_part_token_list))
    print("not-part:                              " + str(final_not_part_token_list))
    print("other-part:                            " + str(final_other_part_token_list))
    print("==================================================================")
    print("[Result detail]")
    print("n_docIDs with phrase-part:             " + str(len(final_result_phrase_part)))
    print("n_docIDs with not-part:                " + str(len(final_result_not_part)))
    print("merge result -> phrase, not:           " + str(len(merged_result_phrase_not)))
    if(flag_find_phrase_part == True and flag_not_find_not_part == True and flag_find_result_merge == True):
        print("n_docIDs with other-part:              " + str(len(final_result_other_part)))
        print("n_docIDs with some other-part:         " + str(len(final_result_some_other_part)))
    print("final result -> phrase, not, other:    " + str(len(final_results)))   
    print("==================================================================")
          
    
    print()
    print("<< DocID of all results >>\n")
    print(final_results)


    # ranking results
    flag_having_all_token = True
    result_dict_all = {}
    result_dict_some = {}

    for i in range(0, len(final_results)):
        cnt_all = 0
        cnt_some = 0
        news_id = final_results[i]
        news_tokens = all_news_token_dict[news_id]
        
        for i in range(0, len(final_phrase_part_token_list)):
            if(final_phrase_part_token_list[i] not in news_tokens):
                flag_having_all_token = False
        for i in range(0, len(final_other_part_token_list)):
            if(final_other_part_token_list[i] not in news_tokens):
                flag_having_all_token = False   

        if(flag_having_all_token == True):
        # this news has all tokens of query -> calculate number of all tokens in this news
               
            # phrase_part tokens
            for j in range(0, len(final_phrase_part_token_list)):
                token = final_phrase_part_token_list[j]
                for k in range(0, len(news_tokens)):
                    if(news_tokens[k] == token):
                        cnt_all += 1
            # other_part tokens
            for j in range(0, len(final_other_part_token_list)):
                token = final_other_part_token_list[j]
                for k in range(0, len(news_tokens)):
                    if(news_tokens[k] == token):
                        cnt_all += 1

            result_dict_all[news_id] = cnt_all            

        else:

            # phrase_part tokens
            for j in range(0, len(final_phrase_part_token_list)):
                token = final_phrase_part_token_list[j]
                for k in range(0, len(news_tokens)):
                    if(news_tokens[k] == token):
                        cnt_some += 1
            # other_part tokens
            for j in range(0, len(final_other_part_token_list)):
                token = final_other_part_token_list[j]
                for k in range(0, len(news_tokens)):
                    if(news_tokens[k] == token):
                        cnt_some += 1

            result_dict_some[news_id] = cnt_some 

    sorted_cnt_all = sorted(result_dict_all.values(), reverse=True) # Sort the values
    ranked_result_dict_all = {}
    for cnt_all in sorted_cnt_all:
        for news_id in result_dict_all.keys():
            if(result_dict_all[news_id] == cnt_all):
                ranked_result_dict_all[news_id] = cnt_all
                break    

    sorted_cnt_some = sorted(result_dict_some.values(), reverse=True) # Sort the values
    ranked_result_dict_some = {}
    for cnt_some in sorted_cnt_some:
        for news_id in result_dict_some.keys():
            if(result_dict_some[news_id] == cnt_some):
                ranked_result_dict_some[news_id] = cnt_some
                break 


    ranked_final_results = []
    for i in range(0, len(ranked_result_dict_all)):
        news_id = list(ranked_result_dict_all.keys())[i]
        ranked_final_results.append(news_id)     
    for i in range(0, len(ranked_result_dict_some)):
        news_id = list(ranked_result_dict_some.keys())[i]
        ranked_final_results.append(news_id)           

    print()
    print("<< Showing results (from 1 to 20) >>")
    n_results = len(ranked_final_results)
    if(n_results > 20):
        n_results = 20
    for i in range(0, n_results):
        news_id = ranked_final_results[i] 
        print()
        print_news(news_id)
        if(news_id in ranked_result_dict_all.keys()):
            print("[ [Type = All]  - Number of query tokens in this news: " + str(ranked_result_dict_all[news_id]) + " ]")
        else:
            print("[ [Type = Some] - Number of query tokens in this news: " + str(ranked_result_dict_some[news_id]) + " ]")

        print()
        