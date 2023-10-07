import tkinter as tk
from PIL import Image, ImageColor

DATASET_FILE_NAME = 'DS0.txt'
RESULT_FILE_NAME = 'DS0.png'
RESULT_IMAGE_SIZE = (960, 540)
BG_COLOR = '#ffffff'
FG_COLOR = '#000000'


def main():
    bg_color_rgb = ImageColor.getrgb(BG_COLOR)
    fg_color_rgb = ImageColor.getrgb(FG_COLOR)

    # Create image
    result_image = Image.new('RGB', RESULT_IMAGE_SIZE, bg_color_rgb)

    # Set up GUI
    root = tk.Tk()
    root.geometry('%ix%i' % RESULT_IMAGE_SIZE)
    root.title(RESULT_FILE_NAME)
    canvas = tk.Canvas(root, bg=BG_COLOR, width=RESULT_IMAGE_SIZE[0], height=RESULT_IMAGE_SIZE[1])
    canvas.place(x=0, y=0)

    # Draw pixels
    with open(DATASET_FILE_NAME, 'r') as dataset_file:
        line = dataset_file.readline()
        while line:
            raw_coordinates = tuple(int(substring) for substring in line.split())
            coordinates = transform_coordinates(raw_coordinates)

            canvas.create_oval(*coordinates, *coordinates, width=0, fill=FG_COLOR)  # Draw to canvas
            result_image.putpixel(coordinates, fg_color_rgb)  # Draw to image

            line = dataset_file.readline()

    # Save image
    result_image.save(RESULT_FILE_NAME)
    # result_image.show()

    root.mainloop()


def transform_coordinates(raw_coordinates: tuple):
    return raw_coordinates[1], RESULT_IMAGE_SIZE[1] - raw_coordinates[0]


if __name__ == '__main__':
    main()
