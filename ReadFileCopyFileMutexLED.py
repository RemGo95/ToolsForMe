from gpiozero import LED
import fcntl

with open('modelGraph.txt', 'r') as f:
    fcntl.flock(f, fcntl.LOCK_EX)
    diskReadLED=LED(17)
    led.on()
    data = f.read()
    with open('modelGraphSave.txt', 'w') as copy:
        copy.write(data)
    fcntl.flock(f, fcntl.LOCK_UN)
	print(data)
	led.off()
