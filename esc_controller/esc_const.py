class EscPwmPins:
    FRONT_RIGHT = 1
    FRONT_LEFT = 2
    BACK_RIGHT = 3
    BACK_LEFT = 4


MIN_DUTY = 0
MAX_DUTY = 0.25


def map_val(x, in_min=0, in_max=1.0, out_min=MIN_DUTY, out_max=MAX_DUTY):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


if __name__ == '__main__':
    print(map_val(0))
