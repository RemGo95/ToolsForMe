import RPi.GPIO as GPIO
import time

class StepperMotor:
    def __init__(self, enable_pin, step_pin, dir_pin, current_feedback_pin):
        self.enable_pin = enable_pin
        self.step_pin = step_pin
        self.dir_pin = dir_pin
        self.current_feedback_pin = current_feedback_pin

        # Set GPIO mode and pin numbers
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.enable_pin, GPIO.OUT)
        GPIO.setup(self.step_pin, GPIO.OUT)
        GPIO.setup(self.dir_pin, GPIO.OUT)
        GPIO.setup(self.current_feedback_pin, GPIO.IN)  # Assuming a digital current feedback signal

        # Initialize GPIO states
        GPIO.output(self.enable_pin, GPIO.LOW)
        GPIO.output(self.step_pin, GPIO.LOW)
        GPIO.output(self.dir_pin, GPIO.LOW)

    def enable(self):
        GPIO.output(self.enable_pin, GPIO.LOW)

    def disable(self):
        GPIO.output(self.enable_pin, GPIO.HIGH)

    def read_current_measure():
        # Import the necessary libraries
        import smbus

    # Define the I2C address of the device
    i2c_address = 0x48

    # Define the register address for current measurement
    register_address = 0x04

    # Open the I2C bus
    bus = smbus.SMBus(1)

    # Read the current measurement from the device
    current_measure = bus.read_word_data(i2c_address, register_address)

    # Convert the current measurement to amperes
    current_measure_amps = current_measure / 1000

    # Close the I2C bus
    bus.close()

    # Return the current measurement in amperes
          return current_measure_amps

    def set_direction(self, direction):
        GPIO.output(self.dir_pin, direction)

    def step(self, steps, delay=0.001, current_limit=0.5):
        for _ in range(steps):
            if GPIO.input(self.current_feedback_pin) == GPIO.HIGH:
                raise CurrentExceededException("Current limit exceeded")
            GPIO.output(self.step_pin, GPIO.HIGH)
            time.sleep(delay)
            GPIO.output(self.step_pin, GPIO.LOW)
            time.sleep(delay)
#Power Monitoring HAT - nakładka do monitorowania poboru prądu - do Raspberry Pi - SB Components SKU20805
    def measure_current(self):
        current = read_current_measure()  # actual current measurement
        torque = current * torque_constant  # Adjust for your specific system
        return torque

    def cleanup(self):
        GPIO.cleanup()

class CurrentExceededException(Exception):
    pass

# Example usage:
if __name__ == "__main__":
    torque_constant = 0.1  # Adjust this constant based on your hardware
    motor1 = StepperMotor(enable_pin=18, step_pin=17, dir_pin=16, current_feedback_pin=19)
    motor2 = StepperMotor(enable_pin=25, step_pin=24, dir_pin=23, current_feedback_pin=22)

    try:
        motor1.enable()
        motor2.enable()

        motor1.set_direction(GPIO.LOW)  # Set direction to forward
        motor2.set_direction(GPIO.HIGH)  # Set direction to reverse

        try:
            motor1.step(200, current_limit=1.0)  # Step motor 1 with current limit
        except CurrentExceededException as e:
            print("Motor 1 current exceeded the limit")

        torque = motor1.measure_current()
        print("Motor 1 torque:", torque)

        motor2.step(200)  # Step motor 2 200 steps
        torque = motor2.measure_current()
        print("Motor 2 torque:", torque)

    except KeyboardInterrupt:
        motor1.disable()
        motor2.disable()
        motor1.cleanup()
        motor2.cleanup()
