def parse_file(file_name, stop_words):
    """
    Parse the file, remove non-letter characters, and convert to lowercase.
    Return a list of words with stop words removed.
    """
    words = []
    with open(file_name, 'r', encoding='utf-8') as file:
        for line in file:
            line_words = line.split()
            for word in line_words:
                cleaned_word = ''.join(char for char in word if char.isalpha()).lower()
                if cleaned_word and cleaned_word not in stop_words:
                    words.append(cleaned_word)
    return words

def generate_word_length_sets(words):
    """
    Generate a dictionary of word sets by their lengths.
    """
    word_length_sets = {}
    for word in words:
        length = len(word)
        if length not in word_length_sets:
            word_length_sets[length] = set()
        word_length_sets[length].add(word)
    return word_length_sets

def print_word_length_sets(word_length_sets):
    """
    Print the number of distinct words for each word length, with at most six words listed.
    Adds two spaces at the beginning of each line for formatting.
    """
    max_length = max(word_length_sets.keys(), default=9)
    for length in range(1, max_length + 1):
        words = sorted(word_length_sets.get(length, []))
        word_count = len(words)
        print("  {:2d}: {:3d}:".format(length, word_count), end="")
        if word_count > 0:
            if word_count > 6:
                words_display = " ".join(words[:3]) + " ... " + " ".join(words[-3:])
            else:
                words_display = " ".join(words)
            print(" " + words_display)
        else:
            print()

# Example usage
stop_words = {"and", "the", "to", "of", "a"}
words = parse_file("example.txt", stop_words)
word_length_sets = generate_word_length_sets(words)
print_word_length_sets(word_length_sets)


def calculate_average_word_length(words):
    """
    Calculate the average word length for a list of words.
    """
    total_length = sum(len(word) for word in words)
    return total_length / len(words) if words else 0

def calculate_ratio_distinct_to_total(words):
    """
    Calculate the ratio of distinct words to total words.
    """
    distinct_words = set(words)
    return len(distinct_words) / len(words) if words else 0

def generate_word_pairs(words, max_sep):
    """
    Generate distinct word pairs with a separation of max_sep or fewer.
    """
    word_pairs = set()
    for i in range(len(words)):
        for j in range(i + 1, min(i + 1 + max_sep, len(words))):
            pair = tuple(sorted([words[i], words[j]]))  # To avoid (word1, word2) and (word2, word1) being counted separately
            word_pairs.add(pair)
    return word_pairs

def calculate_distinct_word_pair_ratio(words, max_sep):
    """
    Calculate the ratio of distinct word pairs to the total number of valid word pairs.
    Only pairs with separation of max_sep or fewer are considered.
    """
    total_pairs = 0
    distinct_pairs = set()

    # Generate all pairs with max_sep constraint
    for i in range(len(words)):
        for j in range(i + 1, min(i + 1 + max_sep, len(words))):
            pair = tuple(sorted([words[i], words[j]]))
            distinct_pairs.add(pair)
            total_pairs += 1

    # Calculate the ratio of distinct pairs to total pairs
    return len(distinct_pairs) / total_pairs if total_pairs > 0 else 0

def print_word_pairs(word_pairs):
    """
    Print the first 5 and last 5 distinct word pairs in alphabetical order.
    """
    word_pairs_list = sorted(word_pairs)
    distinct_pair_count = len(word_pairs)
    print("  {} distinct pairs".format(distinct_pair_count))

    # Only print unique pairs, the first 5 and last 5 without repeating them
    if distinct_pair_count > 10:
        # Print the first 5 pairs
        for pair in word_pairs_list[:5]:
            print("  " + " ".join(pair))  # Adds 2 spaces before each pair

        # Ellipsis to indicate more pairs in between
        print("  ...")

        # Print the last 5 pairs
        for pair in word_pairs_list[-5:]:
            print("  " + " ".join(pair))  # Adds 2 spaces before each pair
    else:
        # If there are 10 or fewer pairs, print all pairs without ellipsis
        for pair in word_pairs_list:
            print("  " + " ".join(pair))  # Adds 2 spaces before each pair

def calculate_jaccard_similarity(set1, set2):
    """
    Calculate the Jaccard similarity between two sets.
    """
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    return intersection / union if union else 0

def main():
    # Step 1: Load stop words
    stop_words = set(parse_file("stop.txt", []))

    # Step 2: Get file names and max_sep value from user
    doc1_file = input("Enter the first file to analyze and compare ==> ").strip()
    print(doc1_file)
    doc2_file = input("Enter the second file to analyze and compare ==> ").strip()
    print(doc2_file)
    max_sep = int(input("Enter the maximum separation between words in a pair ==> ").strip())
    print((max_sep))
    print('\n', end="")

    # Step 3: Parse documents and remove stop words
    doc1_words = parse_file(doc1_file, stop_words)
    doc2_words = parse_file(doc2_file, stop_words)

    # Step 4: Generate word length sets
    word_length_sets_doc1 = generate_word_length_sets(doc1_words)
    word_length_sets_doc2 = generate_word_length_sets(doc2_words)

    # Step 5: Word Analysis for Document 1
    print("Evaluating document {}".format(doc1_file))
    avg_word_length_doc1 = calculate_average_word_length(doc1_words)
    print("1. Average word length: {:.2f}".format(avg_word_length_doc1))

    ratio_distinct_to_total_doc1 = calculate_ratio_distinct_to_total(doc1_words)
    print("2. Ratio of distinct words to total words: {:.3f}".format(ratio_distinct_to_total_doc1))

    print("3. Word sets for document{}:".format(" " + doc1_file))
    print_word_length_sets(word_length_sets_doc1)

    word_pairs_doc1 = generate_word_pairs(doc1_words, max_sep)
    print("4. Word pairs for document{}".format(" " + doc1_file))
    print_word_pairs(word_pairs_doc1)

    ratio_distinct_pairs_doc1 = calculate_distinct_word_pair_ratio(doc1_words, max_sep)
    print("5. Ratio of distinct word pairs to total: {:.3f}".format(ratio_distinct_pairs_doc1))
    print("\n", end="")

    # Step 6: Word Analysis for Document 2
    print("Evaluating document {}".format(doc2_file))
    avg_word_length_doc2 = calculate_average_word_length(doc2_words)
    print("1. Average word length: {:.2f}".format(avg_word_length_doc2))

    ratio_distinct_to_total_doc2 = calculate_ratio_distinct_to_total(doc2_words)
    print("2. Ratio of distinct words to total words: {:.3f}".format(ratio_distinct_to_total_doc2))

    print("3. Word sets for document{}:".format(" " + doc2_file))
    print_word_length_sets(word_length_sets_doc2)

    word_pairs_doc2 = generate_word_pairs(doc2_words, max_sep)
    print("4. Word pairs for document {}".format(doc2_file))
    print_word_pairs(word_pairs_doc2)

    ratio_distinct_pairs_doc2 = calculate_distinct_word_pair_ratio(doc2_words, max_sep)
    print("5. Ratio of distinct word pairs to total: {:.3f}".format(ratio_distinct_pairs_doc2))
    print("\n", end="")

    # Step 7: Comparison
    print("Summary comparison")

    if avg_word_length_doc1 > avg_word_length_doc2:
        print("1. {} on average uses longer words than {}".format(doc1_file, doc2_file))
    elif avg_word_length_doc1 < avg_word_length_doc2:
        print("1. {} on average uses longer words than {}".format(doc2_file, doc1_file))
    else:
        print("1. {} and {} have the same average word length.".format(doc1_file, doc2_file))

    overall_similarity = calculate_jaccard_similarity(set(doc1_words), set(doc2_words))
    print("2. Overall word use similarity: {:.3f}".format(overall_similarity))
    print('3. Word use similarity by length:')

    max_length = max(max(len(word) for word in doc1_words), max(len(word) for word in doc2_words))
    for length in range(1, max_length + 1):
        set1 = set(word for word in doc1_words if len(word) == length)
        set2 = set(word for word in doc2_words if len(word) == length)
        length_similarity = calculate_jaccard_similarity(set1, set2)

        print("   {}: {:.4f}".format(length, length_similarity) if length < 10 else "  {}: {:.4f}".format(length, length_similarity))


    word_pairs_similarity = calculate_jaccard_similarity(set(word_pairs_doc1), set(word_pairs_doc2))
    print("4. Word pair similarity: {:.4f}".format(word_pairs_similarity))



if __name__ == "__main__":
    main()
