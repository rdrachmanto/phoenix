# Translation of ard/orp2.ino to python
# TODO: TEST! Untested code

import time
from grove.adc import ADC

VOLTAGE = 5.0
ARRAY_LENGTH = 40

adc = ADC()

offset = 0
is_calibrated = False
wait_count = 5

orp_array = [0] * ARRAY_LENGTH
index = 0


def average_array(arr):
    if len(arr) < 5:
        return sum(arr) / len(arr)

    mn = min(arr)
    mx = max(arr)

    total = sum(arr) - mn - mx
    return total / (len(arr) - 2)


while True:
    raw = adc.read(0)

    # convert 12-bit ADC to Arduino-style 10-bit reading
    value = raw * 1023 / 4095

    orp_array[index] = value
    index = (index + 1) % ARRAY_LENGTH

    avg = average_array(orp_array)

    orp_value = (
        (30 * VOLTAGE * 1000)
        - (75 * avg * VOLTAGE * 1000 / 1024)
    ) / 75 - offset

    if not is_calibrated:
        if wait_count == 0:
            offset = int(orp_value)
            is_calibrated = True
        wait_count -= 1
    else:
        print(int(orp_value))

    time.sleep(0.3)
