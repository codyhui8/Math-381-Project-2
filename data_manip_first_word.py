import json
import string
from collections import OrderedDict
from operator import itemgetter

# Fetch the data from a JSON file line by line.
def fetch_data(filename):
    data = []
    with open(filename) as f:
        for line in f:
            data.append(json.loads(line))
    return data

# Generates a list of words and the count of the number of words.
def generate_word_list(data):
    word_list = {}
    count = 0
    for i in data:
        text = i["reviewText"]
        text = clean_words(text)
        for word in text:
            if word not in word_list:
                word_list[word] = 1
            else:
                word_list[word] += 1
        if count % 50000 == 0:
            print("Sentences Ingested: " + str(count))
        count += 1

    sorted_word_list = OrderedDict(sorted(word_list.items(), key=itemgetter(1), reverse=True))
    return sorted_word_list


def generate_markov_chain(sentence_data, word_list, rating_values, rating):
    keys = list(word_list.keys())
    key_length = len(keys)
    markov_dict = {}
    first_word_dict = {}
    # Initialize empty dictionaries for each word in "word_list"
    for j in range(0, len(keys)):
        markov_dict[keys[j]] = {}

    count = 0
    first_word_keys = list(first_word_dict.keys())
    # Go through each sentence
    for i in range(0, len(sentence_data)):
        # If rating for the sentence is the rating that we want to isolate.
        # print(str(rating) + ": " + str(rating_values[i]))
        if rating[0] == rating_values[i]:
            text_value = sentence_data[i]
            text = clean_words(text_value)
            length_text = len(text)
            first_word = True
            for j in range(0, length_text):
                secondary_keys = markov_dict[text[j]].keys()
                if j + 1 < length_text:
                    if text[j+1] not in secondary_keys:
                        markov_dict[text[j]][text[j + 1]] = 1
                    else:
                        markov_dict[text[j]][text[j + 1]] += 1

                    if first_word: 
                        if text[j + 1] not in first_word_keys:
                            first_word_keys.append(text[j + 1])
                            first_word_dict[text[j + 1]] = 1
                        else: 
                            first_word_dict[text[j + 1]] += 1
                        first_word = False

                    if "." in text[j + 1]:
                        first_word = True
            count += 1
        if i % 5000 == 0:
            print("Sentences Processed: " + str(i))
    first_word_dict.pop(".", None)
    first_word_dict = OrderedDict(sorted(first_word_dict.items(), key=itemgetter(1),
                                         reverse=True))
    # for i in first_word_dict.keys()[0:100]:
    #     print(str(i) + ": " + str(first_word_dict[i]))
    print("Number of Sentences Inserted: " + str(count))

    first_word_dict = normalize_single({k: first_word_dict[k] for k in
                                        list(first_word_dict.keys())[:100]})

    markov_dict = normalize(markov_dict, keys)

    for k in range(0, key_length):
        markov_dict[keys[k]] = OrderedDict(sorted(markov_dict[keys[k]].items(),
                                                  key=itemgetter(1), reverse=True))

    return [markov_dict, first_word_dict]

# Normalize the data so each row adds up to a probability of 1.
def normalize(data, keys):
    normalized_data = data
    length = len(data)
    for i in range(0, length):
        total_count = 0
        secondary_keys = list(data[keys[i]].items())
        # Count total occurences of all proceeding words
        for j in range(0, len(secondary_keys)):
            total_count += secondary_keys[j][1]

        # Normalize by the total count of the words
        for k in range(0, len(secondary_keys)):
            normalized_data[keys[i]][secondary_keys[k][0]] = 1.0 * secondary_keys[k][1] / total_count
    return normalized_data

## Normalize a single dictionary
def normalize_single(data):
    normalized_data = data
    total_count = 0
    secondary_item = list(data.keys())
    # Count total occurences of all proceeding words
    for j in range(0, len(secondary_item)):
        total_count += data[secondary_item[j]]

    # Normalize by the total count of the words
    for k in range(0, len(secondary_item)):
        normalized_data[secondary_item[k]] = 1.0 * data[secondary_item[k]] / total_count
    return normalized_data


## Clean words of improper punctuation and returns a list of the resulting words.
def clean_words(text_value):
    cleaned_text = text_value.lower().replace(".", ". ")
    cleaned_text = cleaned_text.replace(",", "")
    cleaned_text = cleaned_text.replace(")", "")
    cleaned_text = cleaned_text.replace("(", "")
    cleaned_text = cleaned_text.replace("_", "")
    cleaned_text = cleaned_text.replace('"', "")
    cleaned_text = cleaned_text.replace(':', "")
    cleaned_text = cleaned_text.replace(';', "")
    cleaned_text = cleaned_text.split()
    return cleaned_text


## Pull out data based on the parameter names.
param_names = ["reviewerID", "asin", "reviewerName", "helpful", "reviewText",
               "overall", "summary", "unixReviewTime", "reviewTime"]
def pull_data(params, data):
    return_value = []
    for i in range(0, len(params)):
        value = []
        for j in range(0, len(data)):
            value.append(data[j][params[i]])
        return_value.append(value)
        print("Params Finished: " + str(params[i]))
    return return_value