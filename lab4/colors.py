from PIL import ImageColor

def mix_colors(bg_color_hex, fg_color_hex, t):
    bg_color_rgb = ImageColor.getrgb(bg_color_hex)
    fg_color_rgb = ImageColor.getrgb(fg_color_hex)

    color_rgb = tuple(int(lerp(bg_color_rgb[i], fg_color_rgb[i], t)) for i in range(3))

    return rgb_to_hex(color_rgb)

def rgb_to_hex(color_rgb):
    return '#%02x%02x%02x' % color_rgb

def lerp(a, b, t):
    return a + (b - a) * t
