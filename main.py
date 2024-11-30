import os

# Global variables
screen = []
screen_width = 0
screen_height = 0
color_mode = 0
cursor_x = 0
cursor_y = 0

def clear_screen():
    """Clear the screen."""
    global screen
    screen = [[' ' for _ in range(screen_width)] for _ in range(screen_height)]

def render_screen():
    """Render the screen to the terminal."""
    os.system('clear' if os.name == 'posix' else 'cls')  # Clear terminal
    for row in screen:
        print(''.join(row))
    print("\n")

def handle_screen_setup(data):
    """Handle the screen setup command (0x1)."""
    global screen_width, screen_height, color_mode
    if len(data) < 3:
        print("Error: Invalid screen setup data")
        return
    screen_width, screen_height, color_mode = data[0], data[1], data[2]
    clear_screen()
    print(f"Screen initialized: {screen_width}x{screen_height}, Color Mode: {color_mode}")

def handle_draw_character(data):
    """Handle the draw character command (0x2)."""
    if len(data) < 4:
        print("Error: Invalid draw character data")
        return
    x, y, color, char = data[0], data[1], data[2], chr(data[3])
    if 0 <= x < screen_width and 0 <= y < screen_height:
        screen[y][x] = char

def handle_draw_line(data):
    """Handle the draw line command (0x3)."""
    if len(data) < 6:
        print("Error: Invalid draw line data")
        return
    x1, y1, x2, y2, color, char = data[0], data[1], data[2], data[3], data[4], chr(data[5])
    if x1 == x2:  # Vertical line
        for y in range(min(y1, y2), max(y1, y2) + 1):
            if 0 <= x1 < screen_width and 0 <= y < screen_height:
                screen[y][x1] = char
    elif y1 == y2:  # Horizontal line
        for x in range(min(x1, x2), max(x1, x2) + 1):
            if 0 <= x < screen_width and 0 <= y1 < screen_height:
                screen[y1][x] = char

def handle_render_text(data):
    """Handle the render text command (0x4)."""
    if len(data) < 3:
        print("Error: Invalid render text data")
        return
    x, y, color = data[0], data[1], data[2]
    text = ''.join(chr(c) for c in data[3:])
    for i, char in enumerate(text):
        if 0 <= x + i < screen_width and 0 <= y < screen_height:
            screen[y][x + i] = char

def handle_cursor_movement(data):
    """Handle the cursor movement command (0x5)."""
    global cursor_x, cursor_y
    if len(data) < 2:
        print("Error: Invalid cursor movement data")
        return
    cursor_x, cursor_y = data[0], data[1]

def handle_draw_at_cursor(data):
    """Handle the draw at cursor command (0x6)."""
    global cursor_x, cursor_y
    if len(data) < 2:
        print("Error: Invalid draw at cursor data")
        return
    char, color = chr(data[0]), data[1]
    if 0 <= cursor_x < screen_width and 0 <= cursor_y < screen_height:
        screen[cursor_y][cursor_x] = char

def process_commands(byte_stream):
    """Process the commands from the byte stream."""
    index = 0
    while index < len(byte_stream):
        command = byte_stream[index]
        index += 1

        if command == 0xFF:  # End of file
            break

        if index >= len(byte_stream):
            print("Error: Command length missing")
            break

        length = byte_stream[index]
        index += 1

        if index + length - 1 > len(byte_stream):
            print(f"Error: Insufficient data for command {command}")
            break

        data = byte_stream[index:index + length - 1]
        index += length - 1

        # Handle commands
        if command == 0x1:  # Screen setup
            handle_screen_setup(data)
        elif command == 0x2:  # Draw character
            handle_draw_character(data)
        elif command == 0x3:  # Draw line
            handle_draw_line(data)
        elif command == 0x4:  # Render text
            handle_render_text(data)
        elif command == 0x5:  # Cursor movement
            handle_cursor_movement(data)
        elif command == 0x6:  # Draw at cursor
            handle_draw_at_cursor(data)
        elif command == 0x7:  # Clear screen
            clear_screen()

        render_screen()

def main():
    """Main function to run the program."""
    # Example byte stream (modify as needed for testing)
    byte_stream = [
    0x1, 0x04, 0x14, 0x0A, 0x00,          # Screen setup: 20x10, monochrome
    0x2, 0x05, 0x05, 0x03, 0x00, ord('A'),  # Draw 'A' at (5,3)
    0x3, 0x07, 0x00, 0x00, 0x0A, 0x00, 0x00, ord('-'),  # Draw line
    0x4, 0x06, 0x02, 0x02, 0x00, ord('H'), ord('i'),  # Render text at (2,2): "Hi"
    0xFF                                   # End of file
]


    process_commands(byte_stream)

if __name__ == "__main__":
    main()
