# Command-Based Terminal Screen Rendering Program

## Overview

This program simulates a basic screen rendering system where it processes commands from a byte stream to control drawing 
operations on a terminal screen. The commands allow for screen setup, drawing characters, lines, text, and cursor 
movements. The program displays these operations in real-time by rendering the screen after each command is processed.

## Features

- **Screen Setup**: Initialize screen dimensions and color mode.
- **Draw Character**: Draw a character at a specific position on the screen.
- **Draw Line**: Draw either horizontal or vertical lines on the screen.
- **Render Text**: Render a string of text at a specific position.
- **Cursor Movement**: Move the cursor to a specified position.
- **Draw at Cursor**: Draw a character at the current cursor position.
- **Clear Screen**: Clear the entire screen.
- **End of File**: End the byte stream processing.

## Requirements

- Python 3.x
- Terminal or Command Prompt for rendering output

## How It Works

### 1. **Global Variables**:
   The program maintains several global variables to manage the screen and cursor:
   - `screen`: A 2D list representing the screen grid.
   - `screen_width`: Width of the screen.
   - `screen_height`: Height of the screen.
   - `color_mode`: The color mode of the screen (though currently monochrome).
   - `cursor_x`, `cursor_y`: The current position of the cursor on the screen.

### 2. **Main Functions**:
   Each function corresponds to a specific command in the byte stream.

#### `clear_screen()`
   - Clears the entire screen, resetting it to a grid of spaces.
   
#### `render_screen()`
   - Renders the screen to the terminal by printing each row of characters from the `screen` list.

#### `handle_screen_setup(data)`
   - Sets up the screen dimensions and color mode.
   - Parameters: `data` should contain the width, height, and color mode.
   - It also calls `clear_screen()` to reset the screen after setup.

#### `handle_draw_character(data)`
   - Draws a character at a specified position on the screen.
   - Parameters: `data` should contain the x and y coordinates, color (not used here), and the ASCII value of the 
character to be drawn.

#### `handle_draw_line(data)`
   - Draws either a vertical or horizontal line based on the provided coordinates.
   - Parameters: `data` should contain the start and end coordinates for the line, the color (not used), and the 
character to draw.

#### `handle_render_text(data)`
   - Renders a string of text at a specified position on the screen.
   - Parameters: `data` should contain the starting x, y coordinates, color (not used), and the text to render.

#### `handle_cursor_movement(data)`
   - Moves the cursor to a specified position without drawing anything.
   - Parameters: `data` should contain the new x and y coordinates for the cursor.

#### `handle_draw_at_cursor(data)`
   - Draws a character at the current cursor position.
   - Parameters: `data` should contain the ASCII value of the character and the color (not used here).

#### `process_commands(byte_stream)`
   - Processes each command in the byte stream one by one.
   - Each command is followed by a length indicating how much data will be processed.
   - Commands are handled by matching the command byte with the appropriate handler function.
   - After each operation, the screen is re-rendered.

### 3. **Byte Stream**
   The byte stream contains a sequence of commands and data. The program processes the commands in the following format:
   - **Command Byte**: The first byte specifies the command (e.g., 0x1 for screen setup, 0x2 for drawing a character).
   - **Length Byte**: The second byte specifies how many bytes of data follow for the current command.
   - **Data**: The subsequent bytes contain the data needed for the operation.

   **Example Byte Stream:**
   ```python
   byte_stream = [
       0x1, 0x04, 0x14, 0x0A, 0x00,  # Screen setup: 20x10, monochrome
       0x2, 0x05, 0x05, 0x03, 0x00, ord('A'),  # Draw 'A' at (5,3)
       0x3, 0x07, 0x00, 0x00, 0x0A, 0x00, 0x00, ord('-'),  # Draw line
       0x4, 0x06, 0x02, 0x02, 0x00, ord('H'), ord('i'),  # Render text at (2,2): "Hi"
       0xFF  # End of file
   ]
## Byte Stream Breakdown

This byte stream will:

1. Set up the screen to be 20x10 with monochrome color.
2. Draw the character 'A' at coordinates (5, 3).
3. Draw a line at coordinates (0, 0) to (10, 0) using the '-' character.
4. Render the text "Hi" starting at coordinates (2, 2).
5. End the command sequence.

## Main Program Flow

- The `main()` function initializes a sample byte stream and calls `process_commands()`, which handles each command in 
sequence.
- The program will render the screen after each command to display the changes.

## Example Usage
to run the program use the following command 
```bash
$ python3 main.py
