def help():
    help_text = """
? - display this help info
. - toggle row cursor on and off
h - move cursor left
l - move cursor right
^ - move cursor to beginning of the line
$ - move cursor to end of the line
w - move cursor to beginning of next word
b - move cursor to beginning of previous word
i - insert <text> before cursor
a - append <text> after cursor
x - delete character at cursor
dw - delete word and trailing spaces at cursor
u - undo previous command
r - repeat last command
s - show content
q - quit program
    """
    print(help_text)
def my_insert(content_string, cursor_position, input_text):
    new_content_string = content_string[:cursor_position] + input_text + content_string[cursor_position:]
    new_cursor_position = cursor_position
    return new_content_string, new_cursor_position
def my_append(content_string, cursor_position, input_text):
    new_content_string = content_string[:cursor_position+1] + input_text + content_string[cursor_position+1:]
    new_cursor_position = cursor_position + len(input_text)-1 
    return new_content_string, new_cursor_position
def add_to_history(content_string, cursor_position, content_history, content_idx):
    if content_idx < len(content_history)- 1:
        content_history = content_history[:content_idx+1]
    content_history.append((content_string, cursor_position))
    content_idx += 1
    return content_history, content_idx
def delete_word(content_string, cursor_position):
    l = cursor_position
    is_same_word = True
    while is_same_word:
        if l > 0 and content_string[l-1] != " ":
            l -= 1
        else:
            is_same_word = False
    r = cursor_position
    is_same_word = True
    while is_same_word:
        if r < len(content_string)-1 and content_string[r+1] != " ":
            r += 1
        else:
            is_same_word = False

    while r < len(content_string)-1 and content_string[r+1] == " ":
        r += 1
    new_content_string = content_string[:l] + content_string[r+1:]
    new_cursor_position = l
    return new_content_string, new_cursor_position
def move_to_next_word(content_string, cursor_pos):
    n = len(content_string)
    if n == 0 or cursor_pos >= n - 1:
        return cursor_pos
    pos = cursor_pos
    while pos < n and not content_string[pos].isspace():
        pos += 1
    while pos < n and content_string[pos].isspace():
        pos += 
    return min(pos, n - 1)
def move_to_prev_word(content_string, cursor_pos):
    if len(content_string) == 0 or cursor_pos <= 0:
        return cursor_pos
    pos = cursor_pos
    while pos > 0 and content_string[pos - 1].isspace():
        pos -= 1
    while pos > 0 and not content_string[pos - 1].isspace():
        pos -= 1
    return pos
def repeat_last_command(last_command, content_string, cursor_position, content_history, content_idx):
    if last_command and last_command not in ['u', 'r']:
        command = last_command
def main():
    content_history = [("", 0)]
    content_idx = 0
    cursor_visible = False
    cmd_list = []

    repeat = False
    while True:
        content_string, cursor_position = content_history[content_idx]

        if repeat == True:
            repeat = False
            cmd_list.pop()
            command = cmd_list[-1]
        else:
            command = input(">")
            cmd_list.append(command)


        if (command.startswith('#') or
            not (command == "q" or
                 command == "?" or
                 command.startswith('i') or
                 command.startswith('a') or
                 command == 'h' or
                 command == 'l' or
                 command == 'w' or
                 command == 'b' or
                 command == 'x' or
                 command == '^' or
                 command == '$' or
                 command == 'u' or
                 command == 'r' or
                 command == 'dw' or
                 command == 's' or
                 command == '.')):
            continue

        if command == "q":
            break
        elif command == "?":
            if len(command) == 1:
                help()
        elif command == ".":
            cursor_visible = not cursor_visible
        elif command == "h":
            new_pos = max(0, cursor_position - 1)
            content_history, content_idx = add_to_history(content_string, new_pos, content_history, content_idx)
        elif command == "l":
            new_pos = cursor_position + 1
            if content_string:
                new_pos = min(len(content_string), new_pos)
            else:
                new_pos = 0
            content_history, content_idx = add_to_history(content_string, new_pos, content_history, content_idx)
        elif command == "^":
            new_pos = 0
            content_history, content_idx = add_to_history(content_string, new_pos, content_history, content_idx)
        elif command == "$":
            new_pos = len(content_string)-1 if content_string else 0
            content_history, content_idx = add_to_history(content_string, new_pos, content_history, content_idx)
        elif command == "w":
            new_pos = move_to_next_word(content_string, cursor_position)
            content_history, content_idx = add_to_history(content_string, new_pos, content_history, content_idx)
        elif command == "b":
            new_pos = move_to_prev_word(content_string, cursor_position)
            content_history, content_idx = add_to_history(content_string, new_pos, content_history, content_idx)
        elif command[0] == "i":
            input_text = command[1:]
            if input_text:
                content_string, cursor_position = my_insert(content_string, cursor_position, input_text)
                content_history, content_idx = add_to_history(content_string, cursor_position, content_history, content_idx)
        elif command[0] == "a":
            input_text = command[1:]
            if input_text:
                content_string, cursor_position = my_append(content_string, cursor_position, input_text)
                content_history, content_idx = add_to_history(content_string, cursor_position, content_history, content_idx)
        elif command == "x":
            if content_string and cursor_position >= 0:
                new_content = content_string[:cursor_position] + content_string[cursor_position+1:]
                new_pos = cursor_position if cursor_position < len(new_content) else (len(new_content) - 1 if len(new_content) > 0 else 0)
                content_history, content_idx = add_to_history(new_content, new_pos, content_history, content_idx)
        elif command[0] == "u":
            cmd_list.pop()
            cmd_list.pop()
            if content_idx > 0:
                content_idx -= 1
            content_string, cursor_position = delete_word(content_string, cursor_position)

        elif command == "dw":
            content_string, cursor_position = delete_word(content_string, cursor_position)
            content_history, content_idx = add_to_history(content_string, cursor_position, content_history, content_idx)
        elif command == "r":
            repeat = True
            continue

        elif command == "s":
            pass
        if command != "":
            content_string, cursor_position = content_history[content_idx]
            if cursor_visible and 0 <= cursor_position < len(content_string):
                print(f"{content_string[:cursor_position]}\033[42m{content_string[cursor_position]}\033[0m{content_string[cursor_position+1:]}")
            else:
                print(content_string)

if __name__ == "__main__":
    main()