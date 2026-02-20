

import RPi.GPIO as GPIO
import time

def init_leds(all_leds):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    for pin in all_leds:
        GPIO.setup(pin, GPIO.OUT)

def clear_leds(all_leds):
    for pin in all_leds:
        turn_off_led(pin)

def cleanup():
    GPIO.cleanup()

def turn_on_led(pin):
    GPIO.output(pin, GPIO.HIGH)

def turn_off_led(pin):
    GPIO.output(pin, GPIO.LOW)

def main():
    all_leds = [17, 27, 22, 5, 6, 13]  # Example list of LED pins
    init_leds(all_leds)
    
    try:
        while True:
            for led_pin in all_leds:
                turn_on_led(led_pin)
            time.sleep(1)  # Keep the LED on for 1 second
            clear_leds(all_leds)
            time.sleep(1)  # Keep the LED off for 1 second
    except KeyboardInterrupt:
        print("\nProgram interrupted by user")
    finally:
        cleanup() 

if __name__ == "__main__":
    main()
