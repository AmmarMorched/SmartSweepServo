import RPi.GPIO as GPIO
import time
import pigpio

# Servo motor pin
SERVO_PIN = 18

# Ultrasonic sensor pins
TRIG_PINS = [23, 27, 22]  # Left, middle, right
ECHO_PINS = [24, 17, 6]

# Servo movement limits
SERVO_MIN_ANGLE = 0
SERVO_MAX_ANGLE = 180
SWEEP_DELAY = 0.01  #  sweep speed

# Initialize GPIO
GPIO.setmode(GPIO.BCM)

# Initialize ultrasonic sensors
for trig in TRIG_PINS:
    GPIO.setup(trig, GPIO.OUT)
    GPIO.output(trig, False)

for echo in ECHO_PINS:
    GPIO.setup(echo, GPIO.IN)

# Initialize pigpio for controlling servo motor
pi = pigpio.pi()
if not pi.connected:
    exit(0)

# Function to measure distance using ultrasonic sensor
def get_distance(trig, echo, timeout=1.0):
    # Trigger the ultrasonic burst
    GPIO.output(trig, True)
    time.sleep(0.00001)
    GPIO.output(trig, False)

    # Wait for the echo to start
    pulse_start = time.time()
    while GPIO.input(echo) == 0:
        if time.time() - pulse_start > timeout:
            return None  # if timeout is reached

    # Wait for the echo to stop
    pulse_end = time.time()
    while GPIO.input(echo) == 1:
        if time.time() - pulse_start > timeout:
            return None  # if timeout is reached
        pulse_end = time.time()

    # Calculate distance in cm
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)

    return distance

# Function to move the servo to a specific angle
def set_servo_angle(angle):
    # Convert angle to duty cycle
    duty_cycle = 500 + (angle / 180) * 2000  # Map angle to 500-2500 microseconds
    pi.set_servo_pulsewidth(SERVO_PIN, duty_cycle)

# Improved sweep and object detection logic
def sweep_and_detect():
    direction = 1  
    angle = SERVO_MIN_ANGLE
    
    while True:
        # Sweep the servo motor
        set_servo_angle(angle)
        time.sleep(SWEEP_DELAY)
        
        # Get distances from sensors
        distances = [get_distance(trig, echo) for trig, echo in zip(TRIG_PINS, ECHO_PINS)]
        print(f"Distances: {distances}")

        # Check if any sensor detects an object within 20 cm
        if any(distance is not None and distance <= 20 for distance in distances):
            # Stop sweeping and align the middle sensor to the detected object
            detected_index = distances.index(min(d for d in distances if d is not None and d <= 20))

            if detected_index == 0:
                set_servo_angle(0)  # Turn left
            elif detected_index == 1:
                set_servo_angle(90)  # Face forward
            else:
                set_servo_angle(180)  # Turn right

            print(f"Object detected by Sensor {detected_index + 1}. Moving servo.")
            time.sleep(0.5)  # Wait for the servo to align and recheck
            continue  # Continue to the next loop iteration

        #no object detected, continue sweeping
        angle += direction
        if angle >= SERVO_MAX_ANGLE or angle <= SERVO_MIN_ANGLE:
            direction *= -1  # Reverse the sweep direction

        time.sleep(0.05)  # Small delay to reduce CPU load

try:
    sweep_and_detect()

except KeyboardInterrupt:
    print("Stopping the script...")
finally:
    pi.set_servo_pulsewidth(SERVO_PIN, 0)  # Stop the servo
    pi.stop()
    GPIO.cleanup()
    print("GPIO cleanup completed.")
