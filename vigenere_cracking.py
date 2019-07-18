# Filename: vigenere_cracking.py
# Description: A set of functions for analysis and cracking of vigenere ciphers
# Created: 07-17-2019
# Created by: Benjamin M. Singleton
from cipher_tools import vigenere_encode, vigenere_decode
import copy


def find_matches(text, pattern, candidate_locations):
    """
    Find all matches of pattern in text, assuming it can only be found at the
    list of indices in candidate_locations.
    :param text: The text to search for pattern matches in.
    :type text: str
    :param pattern: The pattern to search for matches of.
    :type pattern: str
    :param candidate_locations: The list of indices in text to look for pattern.
    :type candidate_locations: list
    :return: The list of indices where pattern occurs in text.
    :rtype: list
    """
    matches = list()
    for each in candidate_locations:
        if each + len(pattern) > len(text):
            continue
        if text[each:each+len(pattern)] == pattern:
            matches.append(each)
    return matches


def get_pattern_distances(patterns):
    """
    Returns a list of the periods of consistently repeating patterns. Each
    pattern in patterns has to always repeat in the same number of characters
    or it won't be included in the list.
    :param patterns: The dictionary whose keys are the repeating patterns
    (str), and whose values are the lists of their occurrences in crypt_text.
    :type patterns: dict
    :return: The list of periods of consistently repeating patterns.
    :rtype: list
    """
    pattern_distances = list()
    for each_paterrn in patterns.keys():
        # given a set of locations of a pattern, find the difference between
        # each location, and save this difference if it's consistent, otherwise
        # throw it out.
        indices = patterns[each_paterrn]
        a = patterns[each_paterrn][:-1]
        b = indices[1:]
        deltas = set(map(int.__sub__, b, a))
        if len(deltas) > 1:
            continue
        pattern_distances.append(list(deltas)[0])
    return list(set(pattern_distances))


def get_factors(number):
    """
    Returns a list of the factors of a given number, in ascending order.
    :param number: The number to factor.
    :type number: int
    :return: The list of factors (int) of number.
    :rtype: list
    """
    factors = list()
    for i in range(1, number+1):
        if number % i == 0:
            factors.append(i)
    return factors


def maximize_patterns(crypt_text, patterns, maximum_pattern_length):
    """
    Looks at all of the known patterns in the dictionary of patterns and match
    locations, tries to find patterns that are one character longer, and
    continues recursively until no more patterns are found.
    :param crypt_text: The text to search for patterns in.
    :type crypt_text: str
    :param patterns: The dictionary whose keys are the repeating patterns
    (str), and whose values are the lists of their occurrences in crypt_text.
    :type patterns: dict
    :param maximum_pattern_length: The maximum length of patterns (inclusive).
    :type maximum_pattern_length: int
    :return: The dictionary whose keys are the repeating patterns (str), and
    whose values are the lists of their occurrences in crypt_text.
    :rtype: dict
    """
    changed = False
    new_patterns = dict()
    for each_pattern in patterns.keys():
        tentative_pattern_length = len(each_pattern) + 1
        if tentative_pattern_length > maximum_pattern_length:
            continue
        for each_occurence in range(len(patterns[each_pattern])):
            index = patterns[each_pattern][each_occurence]
            tentative_pattern = crypt_text[index:index+tentative_pattern_length]
            matches = find_matches(crypt_text, tentative_pattern, patterns[each_pattern])
            if len(matches) > 1:
                new_patterns[tentative_pattern] = matches
                changed = True
    if changed:
        recursive_patterns = maximize_patterns(crypt_text, new_patterns, maximum_pattern_length)
        for each_pattern in recursive_patterns.keys():
            patterns[each_pattern] = recursive_patterns[each_pattern]
    return patterns


def initialize_patterns(crypt_text, minimum_pattern_length=3):
    """
    Creates a dictionary, whose keys are strings of repeating patterns in the
    crypt_text and whose values are lists of their occurences in the
    crypt_text.
    :param crypt_text: The text encrypted with a vigenere cipher.
    :type crypt_text: str
    :param minimum_pattern_length: The length (in characters) of repeating
    patterns.
    :return: The dictionary of patterns mentioned in the description of this
    function.
    :rtype: dict
    """
    patterns = dict()
    for index in range(len(crypt_text)):
        if index + minimum_pattern_length > len(crypt_text):
            break
        current_pattern = crypt_text[index:index+minimum_pattern_length]
        if current_pattern in patterns.keys():
            patterns[current_pattern].append(index)
        else:
            patterns[current_pattern] = list()
            patterns[current_pattern].append(index)
    # remove any patterns that only occur once
    copy_patterns = dict()
    patterns = sorted(patterns.items(), key=lambda x: len(x[1]), reverse=True)
    for each_pair in patterns:
        if len(each_pair[1]) <= 1:
            break
        copy_patterns[each_pair[0]] = each_pair[1]
    return copy_patterns


def remove_redundant_patterns(patterns):
    """
    Given a dict whose keys are patterns (strings) and whose values are the
    locations of their occurrences in a cipher text, remove any redundant
    patterns. Patterns are redundant if and only if every occurrence of that
    pattern coincides with the occurrences of a single, larger pattern that
    incorporates it. For example, if "OW" only occurs inside occurrences of
    "COW", then we can dismiss "OW" as redundant.
    :param patterns: The dict to eliminate redundancies from.
    :type patterns: dict
    :return: The resulting dict with all redundancies removed.
    :rtype: dict
    """
    changed = False
    keys_to_delete = list()
    non_redundant_patterns = copy.deepcopy(patterns)
    for suspect_key in non_redundant_patterns.keys():
        for larger_key in non_redundant_patterns.keys():
            if len(suspect_key) >= len(larger_key):
                continue
            if suspect_key not in larger_key:
                continue
            if len(non_redundant_patterns[suspect_key]) != len(non_redundant_patterns[larger_key]):
                continue
            difference = larger_key.index(suspect_key)
            # if suspect_key is NOT at the beginning of larger_key, adjust the
            # indices accordingly
            if difference > 0:
                adjusted = [x - difference for x in non_redundant_patterns[suspect_key]]
            elif difference == 0:
                adjusted = non_redundant_patterns[suspect_key]
            else:
                assert 2 + 2 == 5, "Someone changed the code to examine larger_key instances that don't contain suspect_key!"
            if adjusted == non_redundant_patterns[larger_key]:
                # mark the suspect key for deletion
                keys_to_delete.append(suspect_key)
                changed = True
                # we don't need to see if suspect_key perfectly coincides with
                # any other larger_keys if it does with one of them.
                break
    if changed:
        for each_key in keys_to_delete:
            del non_redundant_patterns[each_key]
        non_redundant_patterns = remove_redundant_patterns(non_redundant_patterns)
    return non_redundant_patterns


def brute_force_vigenere_key(crypt_text, patterns, key_length):
    candidate_list = list()
    for key in candidate_list:
        possible_solution = vigenere_decode(crypt_text, key)
        assert 2 + 2 == 5
        return key
    return -1


def vigenere_kasiski_test(crypt_text, minimum_pattern_length=3, maximum_pattern_length=6):
    patterns = initialize_patterns(crypt_text, minimum_pattern_length=minimum_pattern_length)
    # get the patterns of increasingly large length, if possible
    patterns = maximize_patterns(crypt_text, patterns, maximum_pattern_length)
    patterns = remove_redundant_patterns(patterns)
    # find the periods of all patterns
    pattern_distances = list(set(get_pattern_distances(patterns)))
    # compute possible key lengths from above
    factors_of_distances = [get_factors(x) for x in pattern_distances]
    # get the intersections of all sets of factors
    possible_key_lengths = factors_of_distances[0]
    for each_set in factors_of_distances[1:]:
        # possible_key_lengths = intersection of possible_key_lengths and each_set
        possible_key_lengths = list(set(possible_key_lengths) & set(each_set))
    possible_key_lengths = sorted(possible_key_lengths, reverse=True)
    return possible_key_lengths


def crack_vigenere_cipher(crypt_text, minimum_pattern_length, maximum_pattern_length, minimum_key_size, maximum_key_size):
    # use the kasiski test to find possible key lengths for the crypt_text
    possible_key_lengths = vigenere_kasiski_test(crypt_text, minimum_pattern_length, maximum_pattern_length)
    # pare down list of possible key lengths according to specified maximums and minimums
    temp_list = list()
    for each in possible_key_lengths:
        if each > maximum_key_size:
            continue
        elif each < minimum_key_size:
            break
        temp_list.append(each)
    possible_key_lengths = temp_list
    # find the best-fitting key for each possible key length
    for each_length in possible_key_lengths:
        pass
    # we've narrowed the candidate keys down to one key for each possible key
    # length, so now we select the best out of this list
    print('This functionality has not been implemented yet.')
    return -1


def test_vigenere_cracking():
    plain_text = 'CRYPTOISSHORTFORCRYPTOGRAPHY'.lower()
    crypt_text = vigenere_encode(plain_text, 'abcd')
    print(crypt_text)
    assert vigenere_decode(crypt_text, 'abcd') == plain_text
    patterns = initialize_patterns(crypt_text, minimum_pattern_length=3)
    """
    for each_key in patterns.keys():
        print(each_key + ' ' + str(patterns[each_key]))
    print('\n')
    """
    patterns = maximize_patterns(crypt_text, patterns, maximum_pattern_length=6)
    """
    for each_key in patterns.keys():
        print(each_key + ' ' + str(patterns[each_key]))
    print('\n')
    """
    possible_key_lengths = vigenere_kasiski_test(crypt_text, minimum_pattern_length=3, maximum_pattern_length=6)
    print('Possible key lengths are:')
    print(possible_key_lengths)


if __name__ == '__main__':
    test_vigenere_cracking()
