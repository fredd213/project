# Show the available commands
def show_help():
    commands = [
        ("?", "display this help info"),
        (".", "toggle character cursor on and off"),
        (";", "toggle line cursor on and off"),
        ("h", "move cursor left"),
        ("j", "move cursor up"),
        ("k", "move cursor down"),
        ("l", "move cursor right"),
        ("^", "move cursor to beginning of the line"),
        ("$", "move cursor to end of the line"),
        ("w", "move cursor to beginning of next word"),
        ("b", "move cursor to beginning of previous word"),
        ("i", "insert <text> before cursor"),
        ("a", "append <text> after cursor"),
        ("x", "delete character at cursor"),
        ("dw", "delete word and trailing spaces at cursor"),
        ("yy", "copy current line to memory"),
        ("p", "paste copied line(s) below line cursor"),
        ("P", "paste copied line(s) above line cursor"),
        ("dd", "delete line"),
        ("o", "insert empty line below"),
        ("O", "insert empty line above"),
        ("u", "undo previous command"),
        ("r", "repeat last command"),
        ("s", "show content"),
        ("q", "quit program")
    ]
    for cmd, desc in commands:
        print(f"{cmd} - {desc}")

running = True  # To make program keep running
output = ['']  # List of lines on the text
line_pos = 0  # Position of the cursor 
char_pos = 0  # Position of the cursor 
char_mode = False  # Cursor is in character mode or not
line_mode = False  # Cursor is in line mode or not
undo_stack = []  # Stack to hold previous to undo functionality
command_stack = []  # Stack to hold commands to repeat functionality
clipboard = None  # Clipboard for copy and paste 
has_output_started = False  # To check if content is being displayed

# Function to display the content of the editor
def display_content():
    global has_output_started
    if output != [''] or has_output_started:
        has_output_started = True
        # Iterate over each line and print it with appropriate cursor highlighting
        for i, text in enumerate(output):
            prefix = '*' if line_mode and i == line_pos else ' '
            if char_mode and i == line_pos and text:
                cursor_idx = min(char_pos, len(text)-1)
                text = text[:cursor_idx] + "\033[42m" + text[cursor_idx] + "\033[0m" + text[cursor_idx+1:]
            print(prefix + text)

def save_command(cmd):
    undo_stack.append((output.copy(), line_pos, char_pos, char_mode, line_mode))
    command_stack.append(cmd)

# Restore the previous from the undo stack
def restore_previous():
    global output, line_pos, char_pos, char_mode, line_mode, has_output_started
    if undo_stack:
        state = undo_stack.pop()
        if command_stack:
            command_stack.pop()
        output, line_pos, char_pos, char_mode, line_mode = state
        has_output_started = (output != [''])

# Repeat the last command 
def repeat_last():
    if command_stack:
        last_cmd = command_stack[-1]
        run_command(last_cmd, repeatable=False)
        save_command(last_cmd)  # Save the repeated command to undo stack

# Cursor Movement: Left
def move_right():
    global char_pos
    if char_pos < len(output[line_pos]):
        char_pos += 1

# Cursor Movement: Left
def move_left():
    global char_pos
    if char_pos > 0:
        char_pos -= 1


# Cursor Movement: Move to the beginning of the current line
def move_to_start():
    global char_pos
    char_pos = 0

# Cursor Movement: Move to the end of the current line
def move_to_end():
    global char_pos
    char_pos = max(0, len(output[line_pos]) - 1)

# Cursor Movement: Move to the beginning of the next word
def move_to_next_word():
    global char_pos
    text = output[line_pos]
    i = char_pos
    while i < len(text) and text[i] != ' ':
        i += 1
    while i < len(text) and text[i] == ' ':
        i += 1
    char_pos = i if i < len(text) else char_pos

# Cursor Movement: Move to the previous of the next word
def move_to_prev_word():
    global char_pos
    text = output[line_pos]
    i = char_pos
    while i > 0 and text[i - 1] == ' ':
        i -= 1
    while i > 0 and text[i - 1] != ' ':
        i -= 1
    char_pos = i

# Cursor Movement: Move cursor up by one line
def move_up():
    global line_pos, char_pos
    if line_pos > 0:
        line_pos -= 1
        char_pos = min(char_pos, max(0, len(output[line_pos]) - 1))

# Cursor Movement: Move cursor down by one line 
def move_down():
    global line_pos, char_pos
    if line_pos < len(output) - 1:
        line_pos += 1
        char_pos = min(char_pos, max(0, len(output[line_pos]) - 1))

# Insert text before the cursor on current line
def insert_before(text):
    line = output[line_pos]
    output[line_pos] = line[:char_pos] + text + line[char_pos:]

# Append/insert text after the cursor on the current line
def append_after(text):
    global char_pos
    line = output[line_pos]
    output[line_pos] = line[:char_pos + 1] + text + line[char_pos + 1:]
    char_pos += len(text)

# Remove the character at the cursor position
def remove_char():
    line = output[line_pos]
    if char_pos < len(line):
        output[line_pos] = line[:char_pos] + line[char_pos + 1:]

# Remove the word at and after the cursor position
def remove_word():
    global char_pos
    line = output[line_pos]
    i = char_pos
    while i < len(line) and line[i] != ' ':
        i += 1
    while i < len(line) and line[i] == ' ':
        i += 1
    output[line_pos] = line[:char_pos] + line[i:]
    if char_pos > len(output[line_pos]) - 1 and char_pos > 0:
        char_pos = len(output[line_pos]) - 1

# Copy the current line to the clipboard
def copy_current():
    global clipboard
    clipboard = output[line_pos]

# Paste the copied content after the current line
def paste_after():
    global line_pos
    if clipboard is not None:
        output.insert(line_pos + 1, clipboard)
        line_pos += 1

# Paste the copied content before the current line
def paste_before():
    if clipboard is not None:
        output.insert(line_pos, clipboard)

# Remove the current line
def remove_line():
    global line_pos, char_pos, has_output_started
    if output:
        output.pop(line_pos)
        if not output:
            output.append('')
            has_output_started = False
        line_pos = min(line_pos, len(output) - 1)
        char_pos = min(char_pos, max(0, len(output[line_pos]) - 1))

# Insert an empty line above the current line
def insert_newline_above():
    global char_pos, has_output_started
    if not has_output_started:
        has_output_started = True
    else:
        output.insert(line_pos, '')
        char_pos = 0

# Insert an empty line below the current line
def insert_newline_below():
    global line_pos, char_pos, has_output_started
    if not has_output_started:
        has_output_started = True
    else:
        output.insert(line_pos + 1, '')
        line_pos += 1
        char_pos = 0

# Function to run the commands
def run_command(cmd, repeatable=True):
    global running, char_mode, line_mode

    not_save = {'?', 's', '.', ';', 'u', 'r', 'q'}
    if cmd == '?':
        show_help()  # Show help
        return
    if cmd == 's':
        display_content()  # Show current content
        return
    if cmd == '.':
        char_mode = not char_mode  # Toggle character cursor 
        display_content()
    elif cmd == ';':
        line_mode = not line_mode  # Toggle line cursor 
        display_content()
    elif cmd == 'u':
        restore_previous()  # Undo previous action
        display_content()
        return
    elif cmd == 'r':
        repeat_last()  # Repeat last command
        return
    elif cmd == 'q':
        running = False  # Quit the program
        return
    else:
        handled = True
        if   cmd == 'h'  : move_left()
        elif cmd == 'l': move_right()
        elif cmd == '^': move_to_start()
        elif cmd == '$': move_to_end()
        elif cmd == 'w': move_to_next_word()
        elif cmd == 'b': move_to_prev_word()
        elif cmd == 'j': move_up()
        elif cmd == 'k': move_down()
        elif cmd.startswith('i'): insert_before(cmd[1:])
        elif cmd.startswith('a'): append_after(cmd[1:])
        elif cmd == 'x': remove_char()
        elif cmd == 'dw': remove_word()
        elif cmd == 'yy': copy_current()
        elif cmd == 'p': paste_after()
        elif cmd == 'P': paste_before()
        elif cmd == 'dd': remove_line()
        elif cmd == 'o': insert_newline_below()
        elif cmd == 'O': insert_newline_above()
        else:
            handled = False

        if handled:
            if repeatable and cmd not in not_save:
                save_command(cmd)  
            display_content()

# Main loop
def main():
    while running:
        user_input = input('>')
        if user_input:
            run_command(user_input)
            
main() # start the loop
