white = 0xFFFFFF
black = 0x000000
red = 0xFF0000
green = 0x00FF00
blue = 0x0000FF
magenta = 0xFF00FF
yellow = 0x00FFFF
cyan = 0xFFFF00

def add(color1, color2):
    r = min(color1[0] + color2[0], 255)
    g = min(color1[1] + color2[1], 255)
    b = min(color1[2] + color2[2], 255)
    return r, g, b

def get_random_color():
    import random
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
