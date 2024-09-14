# ServoObjectTracker

A Raspberry Pi project that uses ultrasonic sensors and a servo motor to detect and align with nearby objects. The system sweeps an area, and when an object is detected within a specific range, the servo motor aligns the middle sensor towards the detected object. The project is implemented using Python, pigpio for servo control, and RPi.GPIO for sensor interaction.

## Features

- Sweeps using a servo motor to monitor the surroundings.
- Uses multiple ultrasonic sensors to measure distances to nearby objects.
- Aligns the servo motor with the closest detected object within a specified range.
- Stops sweeping when an object is detected and centers on the object.

## Hardware Components

- Raspberry Pi
- Servo motor
- Ultrasonic sensors (e.g., HC-SR04)
- Breadboard and jumper wires

## Software Requirements

- Python 3
- RPi.GPIO
- pigpio

## Setup Instructions

1. **Hardware Setup:**
    - Connect the ultrasonic sensors to the Raspberry Pi GPIO pins.
    - Connect the servo motor to a PWM-capable pin on the Raspberry Pi.
    - Refer to the GPIO pin numbers used in the code for proper wiring.

2. **Install Software Dependencies:**
    ```bash
    sudo apt-get update
    sudo apt-get install python3-pigpio
    sudo pip3 install RPi.GPIO
    ```

3. **Start the pigpio daemon:**
    ```bash
    sudo pigpiod
    ```

4. **Clone the Repository:**
    ```bash
    git clone https://github.com/yourusername/ServoObjectTracker.git
    cd ServoObjectTracker
    ```

5. **Run the Script:**
    ```bash
    python3 servo_object_tracker.py
    ```

## Code Explanation

The script performs the following tasks:

1. Initializes the GPIO pins for the ultrasonic sensors.
2. Initializes `pigpio` for servo motor control.
3. Sweeps the servo motor between 0 and 180 degrees while monitoring the distances from the ultrasonic sensors.
4. If an object is detected within 20 cm, the servo motor stops sweeping and aligns to face the detected object.
5. When no object is detected, the servo continues to sweep.

## Usage

Run the script to start the object detection and alignment system. The servo motor will sweep continuously until an object is detected within 20 cm, at which point it will align to the direction of the detected object.

## Future Enhancements

- Add more ultrasonic sensors for 360-degree coverage.
- Integrate an LED indicator for visual feedback when an object is detected.
- Implement distance-based speed control for the servo motor.

## Troubleshooting

- **Servo motor not moving:** Ensure that the pigpio daemon is running (`sudo pigpiod`) and that the servo is connected to a PWM-capable pin.
- **Ultrasonic sensor not detecting:** Verify the wiring and connections for the ultrasonic sensors and ensure the correct GPIO pins are specified in the code.
