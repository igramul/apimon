weiss = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
magenta = (255,0,255)

def add(color1, color2):
    r = min(color1[0] + color2[0], 255)
    g = min(color1[1] + color2[1], 255)
    b = min(color1[2] + color2[2], 255)
    return r, g, b
