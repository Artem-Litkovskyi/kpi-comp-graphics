import tkinter as tk
from colors import mix_colors
from regions import find_regions, find_region_centers
from voronoi import voronoi, Point
from PIL import Image, ImageColor, ImageDraw

INPUT_DATASET_FILE_NAME = 'DS0.txt'
RESULT_IMAGE_FILE_NAME = 'DS0.png'
RESULT_IMAGE_SIZE = (960, 540)
POINT_RADIUS = 5
BG_COLOR = '#ffffff'
FG_COLOR = '#000000'
ACCENT_COLOR = '#0000ff'
DATASET_POINTS_OPACITY = 0.1


def main():
    bg_color_rgb = ImageColor.getrgb(BG_COLOR)

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

    # Find region centers
    regions = find_regions(points, RESULT_IMAGE_SIZE[0], RESULT_IMAGE_SIZE[1])
    region_centers = find_region_centers(regions)

    # Calculate voronoi diagram cells
    voronoi_cells = voronoi(
        list(map(lambda p: Point(p[0], p[1]), region_centers)),
        RESULT_IMAGE_SIZE[0], RESULT_IMAGE_SIZE[1]
    )

    # Draw dataset points
    color = mix_colors(BG_COLOR, FG_COLOR, DATASET_POINTS_OPACITY)
    color_rgb = ImageColor.getrgb(color)
    for point in points:
        canvas_point = transform_coordinates_normal_to_canvas(point, RESULT_IMAGE_SIZE[1])

        canvas.create_oval(*canvas_point, *canvas_point, width=0, fill=color)  # Draw to canvas
        result_image.putpixel(canvas_point, color_rgb)  # Draw to image

    # Draw region centers
    draw = ImageDraw.Draw(result_image)
    for region_center in region_centers:
        canvas_point = transform_coordinates_normal_to_canvas(region_center, RESULT_IMAGE_SIZE[1])

        point0 = (canvas_point[0] - POINT_RADIUS // 2, canvas_point[1] - POINT_RADIUS // 2)
        point1 = (point0[0] + POINT_RADIUS, point0[1] + POINT_RADIUS)

        canvas.create_oval(*point0, *point1, width=0, fill=ACCENT_COLOR)  # Draw to canvas
        draw.ellipse((point0, point1), fill=ACCENT_COLOR)  # Draw to image

    # Draw voronoi diagram
    draw = ImageDraw.Draw(result_image)
    voronoi_cells.sort(key=lambda c: c.points[0].x * 300 * (c.points[0].x > 400) + c.points[0].y)
    for cell in voronoi_cells:
        for i in range(len(cell.points)):
            point_a = cell.points[i].to_tuple()
            point_b = cell.points[(i + 1) % len(cell.points)].to_tuple()

            canvas_point_a = transform_coordinates_normal_to_canvas(point_a, RESULT_IMAGE_SIZE[1])
            canvas_point_b = transform_coordinates_normal_to_canvas(point_b, RESULT_IMAGE_SIZE[1])

            canvas.create_line(*canvas_point_a, *canvas_point_b, fill=ACCENT_COLOR)  # Draw to canvas
            draw.line((*canvas_point_a, *canvas_point_b), width=0, fill=ACCENT_COLOR)  # Draw to image

    # Save image
    result_image.save(RESULT_IMAGE_FILE_NAME)
    # result_image.show()

    root.mainloop()


def get_points_from_dataset_file(dataset_file_name: str):
    points = []
    with open(dataset_file_name, 'r') as dataset_file:
        line = dataset_file.readline()
        while line:
            raw_coordinates = tuple(int(substring) for substring in line.split())
            points.append(transform_coordinates_raw_to_normal(raw_coordinates))
            line = dataset_file.readline()
    return points


def transform_coordinates_raw_to_normal(raw_coordinates: tuple):
    return raw_coordinates[1], raw_coordinates[0]


def transform_coordinates_normal_to_canvas(coordinates: tuple, canvas_height: int):
    return coordinates[0], canvas_height - coordinates[1]


if __name__ == '__main__':
    main()
