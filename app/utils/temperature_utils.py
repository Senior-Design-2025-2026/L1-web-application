from gradpyent.gradient import Gradient, RGB

MAX = 122
MIN = 32

START_COLOR = "#F0E68C"  # khaki
END_COLOR = "#DC143C"    # crimson

def c_to_f(celsius):
    return celsius * 9 / 5 + 32

def f_to_c(fahrenheit):
    return (fahrenheit - 32) * 5 / 9

def get_heat_color(temp, unit):
    if unit.lower() == "c":
        temp = c_to_f(temp)

    temp = max(MIN, min(MAX, temp))

    t = (temp - MIN) / (MAX - MIN)

    gg = Gradient(gradient_start=START_COLOR, gradient_end=END_COLOR)

    color: RGB = str(gg.get_color_at(t=t))

    # the guy's package doesnt work??? 
    # using iter/tuple to unpack (as it seems from source code) and using attributes doesnt work. 
    # manually parsing... 

    parts = color.strip()[4:-1].split(",")
    r, g, b = (int(p.strip()) for p in parts)
    hex = f"#{r:02x}{g:02x}{b:02x}"

    return hex
