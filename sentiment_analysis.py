import matplotlib.pyplot as plt

def main():
    positive_words = read_in_list("word_list/positive_words.txt")
    negative_words = read_in_list("word_list/negative_words.txt")

    positive_word_ratio = []
    negative_word_ratio = []

    for i in range(1,6):
        file_name = "text_data/office/" + str(i) + "starreviews.txt"
        data = gather_rating_data(file_name, positive_words, negative_words)
        positive_word_ratio.append(data[0] / (data[1] + data[0]))
        negative_word_ratio.append(data[1] / (data[1] + data[0]))

    generate_graph([positive_word_ratio, negative_word_ratio], "Office Supplies")


def read_in_list(file_name):
    with open(file_name) as f:
        content = f.readlines()
    new_content = []
    for i in content:
        new_content.append(i[:-1])
    return new_content

def gather_rating_data(file_name, positive, negative):
    review_data = read_in_list(file_name)
    sentiment_data = [0, 0]
    for i in review_data:
        cleaned_text = i.lower().replace(".", "")
        cleaned_text = cleaned_text.split()

        for j in cleaned_text:
            if j in positive:
                sentiment_data[0] += 1
            if j in negative:
                sentiment_data[1] += 1
    return sentiment_data

def generate_graph(data, data_name):
    fig = plt.figure(figsize=(10, 5))
    fig.set_size_inches(10, 5)
    fig.suptitle("Positive and Negative Proportions for Generated " + data_name + " Reviews")

    ax1 = fig.add_subplot(121)
    ax1.bar(range(1, 6), data[0], align='center', color="b")
    ax1.axis([0, 6, 0, 1])
    ax1.set_xlabel("Rating")
    ax1.set_ylabel("Proportion of Positive Words")
    ax1.set_title('Positive Words')

    ax2 = fig.add_subplot(122)
    ax2.bar(range(1, 6), data[1], align='center', color="r")
    ax2.axis([0, 6, 0, 1])
    ax2.set_xlabel("Rating")
    ax2.set_ylabel("Proportion of Negative Words")
    ax2.set_title('Negative Words')

    plt.show()

main()