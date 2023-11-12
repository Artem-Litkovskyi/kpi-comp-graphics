# import random
import tkinter as tk
from PIL import Image, ImageColor, ImageDraw

INPUT_DATASET_FILE_NAME = 'DS0.txt'
RESULT_DATASET_FILE_NAME = 'DS0_convex_hull.txt'
RESULT_IMAGE_FILE_NAME = 'DS0.png'
RESULT_IMAGE_SIZE = (960, 540)
POINT_RADIUS = 10
BG_COLOR = '#ffffff'
FG_COLOR = '#000000'
LINE_COLOR = '#0000ff'


def main():
    bg_color_rgb = ImageColor.getrgb(BG_COLOR)
    fg_color_rgb = ImageColor.getrgb(FG_COLOR)

    # Create image
    result_image = Image.new('RGB', RESULT_IMAGE_SIZE, bg_color_rgb)

    # Set up GUI
    root = tk.Tk()
    root.geometry('%ix%i' % RESULT_IMAGE_SIZE)
    root.title(RESULT_IMAGE_FILE_NAME)
    canvas = tk.Canvas(root, bg=BG_COLOR, width=RESULT_IMAGE_SIZE[0], height=RESULT_IMAGE_SIZE[1])
    canvas.place(x=0, y=0)

    # Get points from dataset
    points = get_points_from_dataset_file(INPUT_DATASET_FILE_NAME)
    # points = [
    #     (100, 200),
    #     (100, 100),
    #     (200, 100),
    #     (300, 0),
    #     (400, 200),
    #     (500, 200),
    #     (300, 300),
    # ]
    # random.shuffle(points)
    # points = [
    #     (random.randint(0, RESULT_IMAGE_SIZE[0]), random.randint(0, RESULT_IMAGE_SIZE[1])) for i in range(10)
    # ]

    # Calculate convex hull
    convex_hull = calculate_convex_hull(points)

    # Draw dataset points
    for point in points:
        canvas_point = transform_coordinates_normal_to_canvas(point, RESULT_IMAGE_SIZE[1])
        canvas.create_oval(*canvas_point, *canvas_point, width=0, fill=FG_COLOR)  # Draw to canvas
        result_image.putpixel(canvas_point, fg_color_rgb)  # Draw to image

    # Draw convex hull
    draw = ImageDraw.Draw(result_image)
    for i in range(len(convex_hull)):
        point_a = points[convex_hull[i]]
        point_b = points[convex_hull[(i+1) % len(convex_hull)]]
        canvas_point_a = transform_coordinates_normal_to_canvas(point_a, RESULT_IMAGE_SIZE[1])
        canvas_point_b = transform_coordinates_normal_to_canvas(point_b, RESULT_IMAGE_SIZE[1])
        canvas.create_line(*canvas_point_a, *canvas_point_b, fill=LINE_COLOR)  # Draw to canvas
        draw.line((*canvas_point_a, *canvas_point_b), width=0, fill=LINE_COLOR)  # Draw to image

    # Save image and convex hull points' coordinates
    result_image.save(RESULT_IMAGE_FILE_NAME)
    save_points_to_dataset_file(
        map(lambda x: transform_coordinates_raw_to_normal(points[x]), convex_hull),
        RESULT_DATASET_FILE_NAME
    )
    # result_image.show()

    root.mainloop()


def calculate_convex_hull(points: list):
    convex_hull = []

    # Get the starting point
    starting_point_i = get_starting_point_i(points)
    starting_point = points[starting_point_i]

    # Sort other points counterclockwise
    points.pop(starting_point_i)
    points.sort(key=lambda x: slope(starting_point, x))
    points.insert(0, starting_point)

    # Initial hull point
    convex_hull.append(0)

    # Find other points
    next_point_i = 0
    while True:
        if len(convex_hull) < 2:
            convex_hull.append(next_point_i)
            next_point_i += 1

        last_point_i = convex_hull[-1]  # Get the first item from the "stack"
        prev_point_i = convex_hull[-2]  # Get the second item from the "stack"

        left_turn = cross_product(points[prev_point_i], points[last_point_i], points[next_point_i]) > 0

        if left_turn:
            convex_hull.append(next_point_i)  # Add to "stack" if left_turn
            next_point_i += 1
            if next_point_i == len(points):
                break
        else:
            convex_hull.pop()  # Remove from "stack" while not left_turn

    return convex_hull


def get_starting_point_i(points: iter):
    starting_point_i = 0

    for i in range(1, len(points)):
        starting_point_x = points[starting_point_i][0]
        current_point_x = points[i][0]

        if current_point_x < starting_point_x:
            starting_point_i = i  # select the leftmost point
        elif current_point_x == starting_point_x and points[i][1] > points[starting_point_i][1]:
            starting_point_i = i  # select the topmost point if there are multiple leftmost points

    return starting_point_i


def get_points_from_dataset_file(dataset_file_name: str):
    points = []
    with open(dataset_file_name, 'r') as dataset_file:
        line = dataset_file.readline()
        while line:
            raw_coordinates = tuple(int(substring) for substring in line.split())
            points.append(transform_coordinates_raw_to_normal(raw_coordinates))
            line = dataset_file.readline()
    return points


def save_points_to_dataset_file(points: iter, dataset_file_name: str):
    with open(dataset_file_name, 'w') as dataset_file:
        for point in points:
            raw_coordinates = transform_coordinates_raw_to_normal(point)
            dataset_file.write('{0} {1}\n'.format(*raw_coordinates))


def transform_coordinates_raw_to_normal(raw_coordinates: tuple):
    return raw_coordinates[1], raw_coordinates[0]


def transform_coordinates_normal_to_canvas(coordinates: tuple, canvas_height: int):
    return coordinates[0], canvas_height - coordinates[1]


def slope(p1, p2):
    if p1[0] == p2[0]:
        return -float('inf')
    return (p2[1] - p1[1]) / (p2[0] - p1[0])


def cross_product(p1, p2, p3):
    return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])


if __name__ == '__main__':
    main()
