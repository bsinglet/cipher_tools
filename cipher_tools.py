# Filename: cipher_tools.py
# Description: A set of functions for analysis and decryption of basic ciphers
# Created: 07-07-2019
# Created by: Benjamin M. Singleton
import math


def rotate_letter(letter, rotate_by):
    """
    Performs a Caesar shift on a single letter of plaintext, shifing it by
    rotate_by number of spaces.
    :param letter: The plaintext letter to shift.
    :type letter: str
    :param rotate_by: The number of spaces in the alphabet to shift the letter by.
    :type rotate_by: int
    :return: The shifted letter.
    :rtype: str
    """
    if ord(letter) in range(ord('a'), ord('z') + 1):
        base = ord('a')
    elif ord(letter) in range(ord('A'), ord('Z')+1):
        base = ord('A')
    else:
        return letter
    return str(chr(((ord(letter) - base + rotate_by) % 26) + base))


def rotate(plaintext, rotate_by):
    """
    Performs a Caesar shift, rotating each letter in plaintext by rotate_by
    number of spaces in the alphabet.
    :param plaintext: The text to encrypt with the Caesar cipher.
    :type plaintext: str
    :param rotate_by: The number of spaces to shift each letter of plaintext.
    :type rotate_by: int
    :return: The encrypted text.
    :rtype: str
    """
    rotated = list()
    rotated_text = str()
    for x in plaintext:
        rotated.append(rotate_letter(x, rotate_by))
    for each in rotated:
        rotated_text += each
    return rotated_text


def get_all_rotations(crypt_text):
    """
    Returns a list of all 26 possible Caesar shifts of the crypt_text.
    :param crypt_text: The text believed to be encrypted with a Caesar shift cipher.
    :type crypt_text: str
    :return: The list of strings of shifted text.
    :rtype: list
    """
    rotations = [x for x in [rotate(crypt_text, y) for y in range(26)]]
    return rotations


def vigenere_encode(text, key):
    """
    An implementation of the Vigenere encryption algorithm. Vigenere simply
    performs the Caesar shift one letter at a time, each letter shifted
    according to a repeating key text. For example, given a key of 'cat', the
    algorithm shifts the first letter of plaintext by a = c, the second by
    a = a, the third by a = t, the fourth by a = c again, and so on.
    :param text:
    :type text: str
    :param key:
    :type key: str
    :return:
    :rtype: str
    """
    assert len(text) >= len(key)
    crypt_text = str()
    crypt_text_list = list()
    # first we create the key text, a list that tells the number of places to rotate a given letter in the plaintext
    key = key.lower()
    key_list = [x for x in key]
    key_list = [(ord(x) - ord('a')) for x in key_list]  # a = 0, b = 1...
    key_text_list = key_list * math.floor(len(text)/len(key))
    remaining = key_list[0:len(text) % len(key)]
    for each in remaining:
        key_text_list.append(each)
    # second, we rotate one letter of plaintext at a time, according to our key text
    for x in range(len(text)):
        crypt_text_list.append(rotate_letter(text[x], key_text_list[x]))
    # third, we convert the list of encrypted letters to a string
    for each in crypt_text_list:
        crypt_text += each
    return crypt_text


def vigenere_decode(crypt_text, key):
    """
    We avoid duplicating code by using the vigenere_encrpt function, supplying
    it with an inverted key. For example, a message encrypted with the key
    'cat'can be decrypted by encrypting it again with the key 'yah'.
    :param crypt_text:
    :type crypt_text: str
    :param key:
    :type key: str
    :return:
    :rtype: str
    """
    assert len(crypt_text) >= len(key)
    key = key.lower()
    decryption_key = str()
    # mirror the key around a. (that is, a = a, b = z, c = y, etc)
    for each in key:
        decryption_key += str(chr((26 - (ord(each) - ord('a'))) % 26 + ord('a')))
    print(decryption_key)
    # encoding with the inverted key is the same as decoding
    return vigenere_encode(crypt_text, decryption_key)


def get_letter_counts(text):
    text = text.upper()
    counts = dict()
    for x in range(ord('A'), ord('Z')+1):
        counts[chr(x)] = 0
    for each in text:
        if ord(each) not in range(ord('A'), ord('Z')+1):
            continue
        counts[each] += 1
    return counts


def sort_dict_of_str_to_int(unsorted_dict):
    """
    Sorts a dictionary whose keys are strings and values are integers by their
    integers, in descending order.
    :param unsorted_dict: The dict of str:int to sort.
    :type unsorted_dict: dict
    :return: A list of two-element lists, sorted in descending order by the
    second element.
    :rtype: list
    """
    return sorted(unsorted_dict.items(), key=lambda x: x[1], reverse=True)


def substitute_alphabet(text, origin_to_destination):
    """
    Performs a simple alphabetic substitution on plaintext text using the dict
    in origin_to_destination.
    :param text: The plaintext whose letters we're changing.
    :type text: str
    :param origin_to_destination: The dict whose keys are the letters in the
    plaintext and whose values are the corresponding letters to substitute in
    their place.
    :type origin_to_destination: dict
    :return: The resulting text, encrypted with the cipher.
    :rtype: str
    """
    updated_text = str()
    for letter in text:
        if letter not in origin_to_destination.keys():
            updated_text += letter
        else:
            updated_text += origin_to_destination[letter]
    return updated_text


def get_n_graphs(words, n=2):
    """
    Gets all n-graphs (digraphs for n=2, trigraphs n=3, etc) from a list of
    words, even if they only occur once.
    :param words: The list of words (strings) to look for n-graphs in.
    :type words: list
    :param n: The number of letters to look for at a time.
    :type n: int
    :return: The dict whose keys are the n-graphs found and values are the
    number of times they occur in words.
    :rtype: dict
    """
    n_graphs = dict()
    for each_word in words:
        index = 0
        while index + n <= len(each_word):
            this_digraph = each_word[index:index + n]
            if this_digraph not in n_graphs.keys():
                n_graphs[this_digraph] = 1
            else:
                n_graphs[this_digraph] += 1
            index += 1
    return n_graphs


def get_n_graphs_by_count(words, n=2):
    """
    Gets all n-graphs (digraphs for n=2, trigraphs n=3, etc) from a list of
    words, removes those that only occur once, and sorts them by the number of
    times they're used.
    :param words: The list of words (strings) to look for n-graphs in.
    :type words: list
    :param n: The number of letters to look for at a time.
    :type n: int
    :return: The list whose elements are two-element lists of n-graphs and the
    number of times they occur in words, sortec by the number of times they
    occur.
    :rtype: list
    """
    filtered = filter(lambda x: x[1] > 1, get_n_graphs(words, n).items())
    n_graphs = sorted(filtered, key=lambda x: x[1], reverse=True)
    return n_graphs


def get_n_graph_prefixes(words, n=2):
    """
    Gets all n-graph (digraphs for n=2, trigraphs n=3, etc) prefixes from a
    list of words, even if they only occur once.
    :param words: The list of words (strings) to look for n-graphs in.
    :type words: list
    :param n: The number of letters to look for at a time.
    :type n: int
    :return: The dict whose keys are the n-graphs found and values are the
    number of times they occur in words.
    :rtype: dict
    """
    n_graphs = dict()
    for each_word in words:
        index = 0
        if index + n > len(each_word):
            continue
        this_digraph = each_word[index:index + n]
        if this_digraph not in n_graphs.keys():
            n_graphs[this_digraph] = 1
        else:
            n_graphs[this_digraph] += 1
    return n_graphs


def get_n_graph_suffixes(words, n=2):
    """
    Gets all n-graph (digraphs for n=2, trigraphs n=3, etc) suffixes from a
    list of words, even if they only occur once.
    :param words: The list of words (strings) to look for n-graphs in.
    :type words: list
    :param n: The number of letters to look for at a time.
    :type n: int
    :return: The dict whose keys are the n-graphs found and values are the
    number of times they occur in words.
    :rtype: dict
    """
    n_graphs = dict()
    for each_word in words:
        index = len(each_word) - n
        if index < 0 or index > len(each_word):
            continue
        this_digraph = each_word[index:index + n]
        if this_digraph not in n_graphs.keys():
            n_graphs[this_digraph] = 1
        else:
            n_graphs[this_digraph] += 1
    return n_graphs


def get_n_graph_prefixes_by_count(words, n=2):
    """
    Gets all n-graphs (digraphs for n=2, trigraphs n=3, etc) prefixes in a list
    of words, removes those that only occur once, and sorts them by the number
    of times they're used.
    :param words: The list of words (strings) to look for n-graphs in.
    :type words: list
    :param n: The number of letters to look for at a time.
    :type n: int
    :return: The list whose elements are two-element lists of n-graphs and the
    number of times they occur in words, sortec by the number of times they
    occur.
    :rtype: list
    """
    filtered = filter(lambda x: x[1] > 1, get_n_graph_prefixes(words, n).items())
    n_graphs = sorted(filtered, key=lambda x: x[1], reverse=True)
    return n_graphs


def get_n_graph_suffixes_by_count(words, n=2):
    """
    Gets all n-graphs (digraphs for n=2, trigraphs n=3, etc) suffixes in a list
    of words, removes those that only occur once, and sorts them by the number
    of times they're used.
    :param words: The list of words (strings) to look for n-graphs in.
    :type words: list
    :param n: The number of letters to look for at a time.
    :type n: int
    :return: The list whose elements are two-element lists of n-graphs and the
    number of times they occur in words, sortec by the number of times they
    occur.
    :rtype: list
    """
    filtered = filter(lambda x: x[1] > 1, get_n_graph_suffixes(words, n).items())
    n_graphs = sorted(filtered, key=lambda x: x[1], reverse=True)
    return n_graphs


def naive_substitution(sorted_counts):
    """
    Given a list of lists containing letters (sorted by descending frequency)
    and their counts, produces a dict mapping encrypted text letters to
    plaintext letters under the assumption that the text matches common english
    letter frequency.
    :param sorted_counts: A list of lists, presorted by the second subelement
    in each element. E.g., [['E', 15], ['T', 13]...]
    :type sorted_counts: list
    :return: The dictionary/lookup table to decipher the text. Keys are strings
    and so are values.
    :rtype: dict
    """
    substitution_cipher = dict()
    for each_key in [chr(x) for x in range(ord('A'), ord('Z') + 1)]:
        substitution_cipher[each_key] = '-'
    letters_by_english_frequency = 'etaoinshrdlcumwfgypbvkjxqz'.upper()
    for index in range(len(sorted_counts)):
        if sorted_counts[index][1] == 0:
            break
        substitution_cipher[sorted_counts[index][0]] = letters_by_english_frequency[index]
    for each_key in substitution_cipher.keys():
        print(each_key + ' = ' + substitution_cipher[each_key])
    return substitution_cipher


def main():
    """"
    plain_text = str()
    for x in range(ord('a'), ord('z')+1):
        plain_text += str(chr(x))
    print('plain_text is ' + plain_text)
    print('rotate 1 is ' + rotate(plain_text, 1))
    print('unrotate 1 of that is ' + rotate(rotate(plain_text, 1), -1))
    # plain_text = 'ATTACKATDAWNUSINGLASERGUN'
    rectangle = form_rectangle_horizontally(plain_text, 5, 5)
    for y in rectangle:
        print(y)
    print('\n')
    rectangle = swap_columns(rectangle, 0, 2)
    rectangle = swap_rows(rectangle, 1, 4)
    for y in rectangle:
        print(y)
    crypt_text = unravel_rectangle_horizontally(rectangle)
    print(crypt_text)
    """


if __name__ == '__main__':
    main()
