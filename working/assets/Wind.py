import math

def calculate_wind_resistance(degrees, speed=50):
    left_speed = 0
    right_speed = 0
    up_speed = 0
    down_speed = 0

    wind_direction = math.pi * degrees / 180

    x = math.sin(wind_direction)
    y = math.cos(wind_direction)

    right_speed = x
    left_speed = -x
    up_speed = y 
    down_speed = -y

    print(f"right: {right_speed} left: {left_speed} up: {up_speed} down: {down_speed}")

    return left_speed, right_speed, up_speed, down_speed

if __name__ == '__main__':
    calculate_wind_resistance(90)