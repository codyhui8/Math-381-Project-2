import data_manip_pairs as data_manip
import random

def main():
    filename = "dataset/instruments.json"
    data = data_manip.fetch_data(filename)
    word_list = data_manip.generate_word_list(data)

    # print("Number of Elements in Data: " + str(len(data)))
    # print("Length of Word List: " + str(len(word_list)))
    # temp_list_keys = list(word_list.keys())
    # temp_list_values = list(word_list.values())
    # for i in range(0, 100):
    #     print("Word: " + str(temp_list_keys[i]) + "     Count of Word: " + str(temp_list_values[i]))

    ## params = ["reviewerID", "asin", "reviewerName", "helpful", "reviewText", "overall", "summary", "unixReviewTime", "reviewTime"]
    ## Column 1: Review Test
    ## Column 2: Overall Score
    ## Column 3: Helpfulness
    params = ["reviewText", "overall", "helpful"]
    pulled_data = data_manip.pull_data(params, data)


    # rating = [1]
    # normalized_data_1 = data_manip.generate_markov_chain(pulled_data[0], word_list, pulled_data[1], rating)
    # rating = [2]
    # normalized_data_2 = data_manip.generate_markov_chain(pulled_data[0], word_list, pulled_data[1], rating)
    # rating = [3]
    # normalized_data_3 = data_manip.generate_markov_chain(pulled_data[0], word_list, pulled_data[1], rating)
    # rating = [4]
    # normalized_data_4 = data_manip.generate_markov_chain(pulled_data[0], word_list, pulled_data[1], rating)
    # rating = [5]
    # normalized_data_5 = data_manip.generate_markov_chain(pulled_data[0], word_list, pulled_data[1], rating)
    #
    # SENTENCE_LENGTH = 20
    # NUM_SENTENCES_PAR = 5
    #
    # num_reviews = 100
    # max_length = NUM_SENTENCES_PAR * SENTENCE_LENGTH
    # num_sentence = NUM_SENTENCES_PAR
    # print("--- 5 Star Reviews ---")
    # review_generator(normalized_data_5, num_reviews, max_length, word_list, num_sentence)
    # print("\n--- 4 Star Reviews ---")
    # review_generator(normalized_data_4, num_reviews, max_length, word_list, num_sentence)
    # print("\n--- 3 Star Reviews ---")
    # review_generator(normalized_data_3, num_reviews, max_length, word_list, num_sentence)
    # print("\n--- 2 Star Reviews ---")
    # review_generator(normalized_data_2, num_reviews, max_length, word_list, num_sentence)
    # print("\n--- 1 Star Reviews ---")
    # review_generator(normalized_data_1, num_reviews, max_length, word_list, num_sentence)

    SENTENCE_LENGTH = 20
    NUM_SENTENCES_PAR = 1

    num_reviews = 1000
    max_length = NUM_SENTENCES_PAR * SENTENCE_LENGTH
    num_sentence = NUM_SENTENCES_PAR

    normalized_data = {}
    for i in range(1, 6):
        rating = [i]
        normalized_data = data_manip.generate_markov_chain(pulled_data[0], word_list, pulled_data[1], rating)
        print("--- " + str(i) + " Star Reviews ---")
        file_name = (str(i) + "starreviews.txt")
        review_generator(normalized_data, num_reviews, max_length, word_list, num_sentence, file_name)

    # ## Calculate average rating
    # mean_value = 0
    # for i in range(0, len(pulled_data[1])):
    #     mean_value += pulled_data[1][i]
    # print(mean_value)
    # mean_value = mean_value / len(pulled_data[1])
    # print("Mean Rating Value: " + str(mean_value))
    #
    # ## Calculate average helpfulness. If 0 people rated the helpfulmess, then it isnt considered
    # mean_help_value = 0
    # for i in range(0, len(pulled_data[2])):
    #     if pulled_data[2][i][1] != 0:
    #         mean_help_value += pulled_data[2][i][0] / pulled_data[2][i][1]
    # print(mean_help_value)
    # mean_help_value = mean_help_value / len(pulled_data[2])
    # print("Mean Help Value: " + str(mean_help_value))

def review_generator(data, num_reviews, max_length, word_list, num_sentence, file_name):
    generated_reviews = []
    should_capitalize = ["i", "i'll", "i've"]
    text_file = open("text_data/" + file_name, "w")
    for i in range(0, num_reviews):
        first_word = random.choice(list(data.keys())[0:20]).split()
        sentence = first_word[0].capitalize() + " " + first_word[1]
        prev_word = first_word[0] + " " + first_word[1]
        prev_single_word = first_word[1]
        count_sentence = 0
        new_sentence = False
        for j in range(0, max_length):
            probability = random.uniform(0, 1)
            next_word = data[prev_word]
            keys = list(next_word.keys())
            items = list(next_word.items())
            sum = 0
            for k in range(0, len(items)):
                sum += items[k][1]
                if sum >= probability:
                    if new_sentence:
                        new_sentence = False
                        sentence += (" " + keys[k].capitalize())
                    else:
                        if keys[k] in should_capitalize:
                            sentence += (" " + keys[k].capitalize())
                        else:
                            sentence += (" " + keys[k])
                    prev_word = prev_single_word + " " + keys[k]
                    prev_single_word = keys[k]
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

main()

