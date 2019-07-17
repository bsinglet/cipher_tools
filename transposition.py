# Filename: transposition.py
# Description: A set of functions related to transposition ciphers for
# encryption and obfuscation.
#
# Thus far includes code for arranging text in rectangles, swapping rows and
# columns of rectangles, and route ciphers (traversing rectangles in a spiral
# pattern.) No support for rail ciphers yet.
#
# Created: 07-11-2019
# Created by: Benjamin M. Singleton
import copy


def form_rectangle_horizontally(text, width, length):
    rectangle = [list() for x in range(length)]
    for y in range(length):
        rectangle[y] = [x for x in text[(y*width):(y+1)*width]]
    return rectangle


def form_rectangle_vertically(text, width, length):
    rectangle = [['' for x in range(width)] for y in range(length)]
    for x in range(width):
        for y in range(length):
            rectangle[y][x] = text[y+x*width:y+(x*width)+1]
    return rectangle


def unravel_rectangle_horizontally(rectangle):
    text = str()
    for each_row in rectangle:
        for each_letter in each_row:
            text += each_letter
    return text


def unravel_rectangle_vertically(rectangle):
    text = str()
    width = len(rectangle[0])
    for column in range(width):
        for row in range(len(rectangle)):
            text += rectangle[row][column]
    return text


def swap_rows(rectangle, row_1, row_2):
    temp_row = copy.deepcopy(rectangle[row_1])
    rectangle[row_1] = rectangle[row_2]
    rectangle[row_2] = temp_row
    return rectangle


def swap_columns(rectangle, column_1, column_2):
    for row in range(len(rectangle)):
        temp_val = copy.deepcopy(rectangle[row][column_1])
        rectangle[row][column_1] = rectangle[row][column_2]
        rectangle[row][column_2] = temp_val
    return rectangle


def write_to_location_pairs(rectangle, text, locations):
    index = 0
    for x, y in locations:
        rectangle[y][x] = text[index]
        index += 1
    return rectangle


def read_from_location_pairs(rectangle, locations):
    text = str()
    for x, y in locations:
        text += rectangle[y][x]
    return text


def get_spiral(width, length, clockwise=True, inward=True):
    """
    Returns a list of lists (xy coordinate-pairs) that signifies the order of
    locations to visit in a rectangle of width and length, following a spiral
    pattern. By default, it is a clockwise, inward-moving spiral.
    :param width: The width of the rectangle.
    :type width: int
    :param length: The length of the rectangle.
    :type length: int
    :param clockwise: True==clockwise, False==counterclockwise.
    :type clockwise: bool
    :param inward: True==inward, False==outward.
    :type inward: bool
    :return: The list of lists forming a spiral.
    :rtype: list
    """
    full_rotations = 0
    locations = list()
    # it's difficult to predict the number of locations in a spiral, so we just
    # keep trying to spiral until we run out of locations
    old_num_locations = -1
    while len(locations) > old_num_locations:
        this_rotation = list()
        old_num_locations = len(locations)
        # save the top left-to-right row
        x_positions = [x for x in range(full_rotations, (width - full_rotations))]
        current_y = full_rotations
        for each_x in x_positions:
            this_rotation.append(list())
            this_rotation[-1].append(each_x)
            this_rotation[-1].append(current_y)
        # save the right top-to-bottom column
        y_positions = [y for y in range(full_rotations + 1, (length - full_rotations))]
        current_x = width - full_rotations - 1
        for each_y in y_positions:
            this_rotation.append(list())
            this_rotation[-1].append(current_x)
            this_rotation[-1].append(each_y)
        # save the bottom right-to-left row
        x_positions = [x for x in range(full_rotations, (width - full_rotations) - 1)]
        x_positions = sorted(x_positions, reverse=True)
        current_y = length - full_rotations - 1
        for each_x in x_positions:
            this_rotation.append(list())
            this_rotation[-1].append(each_x)
            this_rotation[-1].append(current_y)
        # save the left bottom-to-top column
        y_positions = [y for y in range(full_rotations + 1, (length - full_rotations) - 1)]
        y_positions = sorted(y_positions, reverse=True)
        current_x = full_rotations
        for each_y in y_positions:
            this_rotation.append(list())
            this_rotation[-1].append(current_x)
            this_rotation[-1].append(each_y)
        # the first element visited in a rotation is the same whether traversed
        # clockwise or counter-clockwise, but the rest of the order is
        # reversed.
        if len(this_rotation) > 1 and not clockwise:
            this_rotation.reverse()
            temp_rotation = list()
            temp_rotation.append(this_rotation[-1])
            temp_rotation += this_rotation[0:-1]
            this_rotation = temp_rotation
        for each_pair in this_rotation:
            locations.append(each_pair)
        # next iteration
        full_rotations += 1
    # if we're spiraling inwards instead of outwards, we just need to reverse
    # the order that we visit locations
    if not inward:
        locations.reverse()
    return locations


def form_rectangle_spiral(text, width, length, clockwise=True, inward=True):
    rectangle = [['' for x in range(width)] for y in range(length)]
    locations = get_spiral(width, length, clockwise, inward)
    rectangle = write_to_location_pairs(rectangle, text, locations)
    """
    for each_row in rectangle:
        print(each_row)
    """
    return rectangle


def test_spiral():
    plaintext = 'The quick brown fox jumps over the lazy dog'
    plaintext = [chr(x) for x in range(ord('a'), ord('z') + 1)] * 3
    locations = get_spiral(width=8, length=8, clockwise=False, inward=True)
    rectangle = [['' for x in range(8)] for y in range(8)]
    rectangle = write_to_location_pairs(rectangle, plaintext, locations)
    for each_row in rectangle:
        print(each_row)
    crypt_text = unravel_rectangle_horizontally(rectangle)
    print(crypt_text)
    plaintext = read_from_location_pairs(rectangle, locations)
    print(plaintext)


if __name__ == '__main__':
    test_spiral()
