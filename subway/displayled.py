

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
    led_pin = 17  # Example GPIO pin number
    init_leds([led_pin])
    
    try:
        while True:
            turn_on_led(led_pin)
            time.sleep(1)  # Keep the LED on for 1 second
            turn_off_led(led_pin)
            time.sleep(1)  # Keep the LED off for 1 second
    except KeyboardInterrupt:
        print("\nProgram interrupted by user")
    finally:
        cleanup() 

if __name__ == "__main__":
    main()
