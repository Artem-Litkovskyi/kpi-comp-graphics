def find_regions(points: list, image_width: int, image_height: int):
    regions = []

    visited = get_empty_bitmap(image_width, image_height)
    bitmap = get_image_bitmap(points, image_width, image_height)

    start_point_i = 0

    while True:
        region = []

        # Find the first point of the region
        start_point_i = get_start_point_i(points, visited, start_point_i)

        if start_point_i == -1:
            break

        to_visit = [points[start_point_i]]

        # Find other points of the region
        while to_visit:
            # Visit a point
            point = to_visit[-1]
            to_visit.pop()

            visited[point[0]][point[1]] = True

            # Add it to the component
            region.append(point)

            # Find neighbour points
            for x_delta in range(-1, 2):
                for y_delta in range(-1, 2):
                    neighbour_point_x = point[0] + x_delta
                    neighbour_point_y = point[1] + y_delta

                    if not bitmap[neighbour_point_x][neighbour_point_y]:
                        continue

                    if visited[neighbour_point_x][neighbour_point_y]:
                        continue

                    to_visit.append((neighbour_point_x, neighbour_point_y))

        regions.append(region)

    return regions


def find_region_centers(regions: list):
    region_centers = []

    for region in regions:
        center_x = sum(map(lambda p: p[0], region)) / len(region)
        center_y = sum(map(lambda p: p[1], region)) / len(region)

        region_centers.append((center_x, center_y))

    return region_centers


def get_start_point_i(points: list, visited: list, last_start_point_i: int):
    for i in range(last_start_point_i, len(points)):
        point = points[i]

        if visited[point[0]][point[1]]:
            continue

        return i
    return -1


def get_empty_bitmap(image_width: int, image_height: int):
    return [[False for i in range(image_height)] for j in range(image_width)]


def get_image_bitmap(points: list, image_width: int, image_height: int):
    bitmap = get_empty_bitmap(image_width, image_height)
    for point in points:
        bitmap[point[0]][point[1]] = True
    return bitmap
