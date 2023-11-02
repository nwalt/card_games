"""General utilties, fragment as needed."""

def right_pad(string, length, character):
    """Pad a string to a certain length on the right side"""
    add_len = length - len(string)
    return f'{string}{character * add_len}'

def validate_character(char, acceptable_characters):
    while True:
        check = input(char)
        if len(check) > 1:
            print('Please enter only one character')
            continue
        if check not in acceptable_characters:
            print('Invalid selection, try again')
            continue
        return check
