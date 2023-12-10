def voronoi(points: list, image_width: int, image_height: int):
    cells = []

    for i, point_a in enumerate(points):
        cell = Cell([
            Point(0, 0),
            Point(0, image_height),
            Point(image_width, image_height),
            Point(image_width, 0)
        ])

        for j, point_b in enumerate(points):
            if j == i:
                continue

            separator = Line.separating(point_a, point_b)

            # Get points of intersection with cell
            intersections = cell.get_intersections(separator)

            if len(intersections) < 2:
                continue

            # Update cell
            new_cell = Cell(list(intersections))
            point_div = separator.diversion(point_a)

            for cell_point in cell.points:
                cell_point_div = separator.diversion(cell_point)

                if point_div < 0 < cell_point_div or cell_point_div < 0 < point_div:
                    continue  # ignore old cell points that are on the other side

                new_cell.points.append(cell_point)

            cell = new_cell
            cell.sort_counterclockwise()

        cells.append(cell)

    return cells


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def to_tuple(self):
        return self.x, self.y

    def slope(self, other):
        if self.x == other.x:
            return -float('inf')
        return (other.y - self.y) / (other.x - self.x)

    def __repr__(self):
        return '[' + str(self.x) + ', ' + str(self.y) + ']'

    def __hash__(self):
        return hash(self.x) * 11 + hash(self.y) * 17

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Line:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    @staticmethod
    def separating(point0, point1):
        a = point1.x - point0.x
        b = point1.y - point0.y
        c = -(a * (point0.x + point1.x) + b * (point0.y + point1.y)) / 2
        return Line(a, b, c)

    @staticmethod
    def connecting(point0, point1):
        if point0.x == point1.x:
            return Line(1, 0, -point0.x)

        if point0.y == point1.y:
            return Line(0, 1, -point0.y)

        a = 1 / (point1.x - point0.x)
        b = -1 / (point1.y - point0.y)
        c = -(a * point0.x + b * point0.y)
        return Line(a, b, c)

    def get_x(self, y):
        return -(self.b * y + self.c) / self.a

    def get_y(self, x):
        return -(self.a * x + self.c) / self.b

    def diversion(self, point):
        return self.a * point.x + self.b * point.y + self.c

    def intersection(self, other):
        try:
            if self.a == 0:
                y = self.get_y(0)
                return Point(other.get_x(y), y)

            if self.b == 0:
                x = self.get_x(0)
                return Point(x, other.get_y(x))

            y = ((other.a * self.c) / self.a - other.c) / (other.b - self.b * other.a / self.a)
            x = self.get_x(y)
            return Point(x, y)
        except ZeroDivisionError:
            return

    def __repr__(self):
        return str(self.a) + ' * x + ' + str(self.b) + ' * y + ' + str(self.c) + ' = 0'


class Cell:
    def __init__(self, points):
        self.points = points

    def get_intersections(self, line):
        intersections = set()

        for i in range(len(self.points)):
            point0 = self.points[i]
            point1 = self.points[(i + 1) % len(self.points)]

            cell_line = Line.connecting(point0, point1)

            intersection = line.intersection(cell_line)

            if not intersection:
                continue

            if intersection.x < min(point0.x, point1.x) or max(point0.x, point1.x) < intersection.x:
                continue

            if intersection.y < min(point0.y, point1.y) or max(point0.y, point1.y) < intersection.y:
                continue

            intersections.add(intersection)

        return intersections

    def sort_counterclockwise(self):
        reference_point_i = 0

        for i in range(1, len(self.points)):
            reference_point_x = self.points[reference_point_i].x
            current_point_x = self.points[i].x

            if current_point_x < reference_point_x:
                reference_point_i = i  # select the leftmost point
            elif current_point_x == reference_point_x and self.points[i].y > self.points[reference_point_i].y:
                reference_point_i = i  # select the topmost point if there are multiple leftmost points

        reference_point = self.points[reference_point_i]

        self.points.pop(reference_point_i)
        self.points = sorted(self.points, key=lambda p: reference_point.slope(p))
        self.points.insert(0, reference_point)
