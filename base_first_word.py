import data_manip_first_word as data_manip
import random
from collections import OrderedDict
from operator import itemgetter

def main():
    filename = "dataset/office.json"
    data = data_manip.fetch_data(filename)
    word_list = data_manip.generate_word_list(data)

    ## params = ["reviewerID", "asin", "reviewerName", "helpful", "reviewText",
    #  "overall", "summary", "unixReviewTime", "reviewTime"]
    ## Column 1: Review Test
    ## Column 2: Overall Score
    ## Column 3: Helpfulness
    params = ["reviewText", "overall", "helpful"]
    pulled_data = data_manip.pull_data(params, data)


    # rating = [1]
    # normalized_data_1 = data_manip.generate_markov_chain\
    #     (pulled_data[0], word_list, pulled_data[1], rating)
    # normalized_first_word_1 = normalized_data_1[1]
    # normalized_data_1 = normalized_data_1[0]
    # normalized_first_word_1 = OrderedDict(sorted(normalized_first_word_1.items(),
    #                                              key=itemgetter(1), reverse=True))

    # rating = [2]
    # normalized_data_2 = data_manip.generate_markov_chain\
    #     (pulled_data[0], word_list, pulled_data[1], rating)
    # normalized_first_word_2 = normalized_data_2[1]
    # normalized_data_2 = normalized_data_2[0]
    # normalized_first_word_2 = OrderedDict(sorted(normalized_first_word_2.items(),
    #                                              key=itemgetter(1), reverse=True))

    # rating = [3]
    # normalized_data_3 = data_manip.generate_markov_chain\
    #     (pulled_data[0], word_list, pulled_data[1], rating)
    # normalized_first_word_3 = normalized_data_3[1]
    # normalized_data_3 = normalized_data_3[0]
    # normalized_first_word_3 = OrderedDict(sorted(normalized_first_word_3.items(),
    #                                              key=itemgetter(1), reverse=True))

    # rating = [4]
    # normalized_data_4 = data_manip.generate_markov_chain\
    #     (pulled_data[0], word_list, pulled_data[1], rating)
    # normalized_first_word_4 = normalized_data_4[1]
    # normalized_data_4 = normalized_data_4[0]
    # normalized_first_word_4 = OrderedDict(sorted(normalized_first_word_4.items(),
    #                                              key=itemgetter(1), reverse=True))

    # rating = [5]
    # normalized_data_5 = data_manip.generate_markov_chain\
    #     (pulled_data[0], word_list, pulled_data[1], rating)
    # normalized_first_word_5 = normalized_data_5[1]
    # normalized_data_5 = normalized_data_5[0]
    # normalized_first_word_5 = OrderedDict(sorted(normalized_first_word_5.items(),
    #                                              key=itemgetter(1), reverse=True))

    # SENTENCE_LENGTH = 20
    # NUM_SENTENCES_PAR = 5
    #
    # num_reviews = 100
    # max_length = NUM_SENTENCES_PAR * SENTENCE_LENGTH
    # num_sentence = NUM_SENTENCES_PAR
    # print("--- 5 Star Reviews ---")
    # review_generator(normalized_data_5, num_reviews, max_length, word_list,
    #                  num_sentence, normalized_first_word_5)
    # print("\n--- 4 Star Reviews ---")
    # review_generator(normalized_data_4, num_reviews, max_length, word_list,
    #                  num_sentence, normalized_first_word_4)
    # print("\n--- 3 Star Reviews ---")
    # review_generator(normalized_data_3, num_reviews, max_length, word_list,
    #                  num_sentence, normalized_first_word_3)
    # print("\n--- 2 Star Reviews ---")
    # review_generator(normalized_data_2, num_reviews, max_length, word_list,
    #                  num_sentence, normalized_first_word_2)
    # print("\n--- 1 Star Reviews ---")
    # review_generator(normalized_data_1, num_reviews, max_length, word_list,
    #                  num_sentence, normalized_first_word_1)

    SENTENCE_LENGTH = 20
    NUM_SENTENCES_PAR = 5

    num_reviews = 100
    max_length = NUM_SENTENCES_PAR * SENTENCE_LENGTH
    num_sentence = NUM_SENTENCES_PAR

    normalized_data = {}
    for i in range(1, 6):
        rating = [i]
        normalized_data = data_manip.generate_markov_chain(pulled_data[0], word_list, pulled_data[1], rating)
        normalized_first_word = normalized_data[1]
        normalized_data = normalized_data[0]
        normalized_first_word = OrderedDict(sorted(normalized_first_word.items(),
                                                     key=itemgetter(1), reverse=True))
        print("--- " + str(i) + " Star Reviews ---")
        file_name = (str(i) + "starreviews.txt")
        review_generator(normalized_data, num_reviews, max_length, word_list, num_sentence,
                         normalized_first_word, file_name)

def review_generator(data, num_reviews, max_length, word_list, num_sentence, first_word_data, file_name):
    generated_reviews = []
    should_capitalize = ["i", "i'll", "i've"]
    text_file = open("text_data/" + file_name, "w")
    for i in range(0, num_reviews):
        first_word = random.choice(list(word_list.keys())[0:20])
        sentence = first_word.capitalize()
        prev_word = first_word
        count_sentence = 0
        new_sentence = False
        for j in range(0, max_length):
            probability = random.uniform(0, 1)
            next_word = data.get(prev_word)
            keys = list(next_word.keys())
            items = list(next_word.items())
            sum = 0
            for k in range(0, len(items)):
                sum += items[k][1]
                if sum >= probability:
                    if new_sentence:
                        new_sentence = False
                        sentence += (" " + find_first_word(first_word_data).capitalize())
                    else:
                        if keys[k] in should_capitalize:
                            sentence += (" " + keys[k].capitalize())
                        else:
                            sentence += (" " + keys[k])
                    prev_word = keys[k]
                    break

            if "." in prev_word or "!" in prev_word or "?" in prev_word:
                count_sentence += 1
                new_sentence = True
                if count_sentence == num_sentence:
                    generated_reviews.append(sentence)
                    print(sentence)
                    text_file.write(sentence + "\n")
                    break
    text_file.close()
    print("Reviews Not Generated: " + str(num_reviews - len(generated_reviews)))

def find_first_word(data):
    sum = 0
    first_word = ""
    probability = random.uniform(0, 1)
    items = list(data.items())
    for k in range(0, len(data)):
        sum += items[k][1]
        if sum >= probability:
            first_word = items[k][0]
            break
    return first_word

main()

