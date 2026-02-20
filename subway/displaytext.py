#!/usr/bin/env python3

import LCD1602


def init_lcd():
    """
    Initialize the LCD1602 display with I2C address and backlight settings.
    Returns: 0 on success, 1 on failure.
    """
    try:
        LCD1602.init(0x27, 1)  # init(slave address, background light)
        print("LCD1602 initialized successfully!")

        return 0
    except Exception as e:
        print(f"Failed to initialize LCD1602: {e}")
        return 1

def display_static_message(message1, message2):
    """Display static welcome messages on the LCD."""
    LCD1602.write(0, 0, message1)
    LCD1602.write(1, 1, message2)

def clear_lcd():
    """Clean up the LCD display."""
    try:
        LCD1602.clear()
    except Exception as e:
        print(f"Error during cleanup: {e}")

def main():
    """
    Main function - simple LCD display.
    Returns: Integer status code. 0 for success, 1 for error.
    """
    # Initialize the LCD
    if init_lcd() != 0:
        return 1
    
    try:
        # Display welcome message
        display_static_message("hi", "test")
        print("Message displayed on LCD successfully!")
        return 0
        
    except KeyboardInterrupt:
        print("\nProgram interrupted by user")
        clear_lcd()
        return 0
    except Exception as e:
        print(f"An error occurred: {e}")
        clear_lcd()
        return 1

if __name__ == "__main__":
    main()
