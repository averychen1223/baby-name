"""
Baby Names Project
"""

import tkinter
import babynames
import babygraphicsgui as gui

FILENAMES = [
    "data/baby-1900.txt",
    "data/baby-1910.txt",
    "data/baby-1920.txt",
    "data/baby-1930.txt",
    "data/baby-1940.txt",
    "data/baby-1950.txt",
    "data/baby-1960.txt",
    "data/baby-1970.txt",
    "data/baby-1980.txt",
    "data/baby-1990.txt",
    "data/baby-2000.txt",
    "data/baby-2010.txt",
]
CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 600
YEARS = [1900, 1910, 1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010]
GRAPH_MARGIN_SIZE = 20
COLORS = ["red", "purple", "green", "blue"]
TEXT_DX = 2
LINE_WIDTH = 2
MAX_RANK = 1000


def get_x_coordinate(width, year_index):
    """
    Given the width of the canvas and the index of the current year
    in the YEARS list, returns the x coordinate of the vertical
    line associated with that year.

    Input:
        width (int): The width of the canvas
        year_index (int): The index of the current year in the YEARS list
    Returns:
        x_coordinate (int): The x coordinate of the vertical line associated
                              with the specified year.
    """
    space = (width - 2 * GRAPH_MARGIN_SIZE) / len(YEARS)
    return GRAPH_MARGIN_SIZE + year_index * space


def draw_fixed_lines(canvas):
    """
    Erases all existing information on the given canvas and then
    draws the fixed background lines on it.

    Input:
        canvas (Tkinter Canvas): The canvas on which we are drawing.

    Returns:
        This function does not return any value.
    """
    canvas.delete("all")  # delete all existing lines from the canvas

    canvas.create_line(
        GRAPH_MARGIN_SIZE,
        GRAPH_MARGIN_SIZE,
        CANVAS_WIDTH - GRAPH_MARGIN_SIZE,
        GRAPH_MARGIN_SIZE,
    )
    canvas.create_line(
        GRAPH_MARGIN_SIZE,
        CANVAS_HEIGHT - GRAPH_MARGIN_SIZE,
        CANVAS_WIDTH - GRAPH_MARGIN_SIZE,
        CANVAS_HEIGHT - GRAPH_MARGIN_SIZE,
    )
    canvas.create_line(GRAPH_MARGIN_SIZE, 0, GRAPH_MARGIN_SIZE, CANVAS_HEIGHT)

    for i in range(len(YEARS)):
        x_coord = get_x_coordinate(CANVAS_WIDTH, i)
        canvas.create_line(x_coord, 0, x_coord, CANVAS_HEIGHT)
        canvas.create_text(
            x_coord + TEXT_DX,
            CANVAS_HEIGHT - GRAPH_MARGIN_SIZE,
            text=YEARS[i],
            anchor=tkinter.NW,
        )


def draw_names(canvas, name_data, lookup_names):
    """
    Given a dict of baby name data and a list of name, plots
    the historical trend of those names onto the canvas.

    Input:
        canvas (Tkinter Canvas): The canvas on which we are drawing.
        name_data (dict): Dictionary holding baby name data
        lookup_names (List[str]): A list of names whose data you want to plot

    Returns:
        This function does not return any value.
    """
    draw_fixed_lines(canvas)  # draw the fixed background grid

    cnt = 0
    for name in lookup_names:
        data = name_data[name]
        for i in range(len(YEARS) - 1):
            year1 = str(YEARS[i])
            year2 = str(YEARS[i + 1])

            if year1 in data:
                rank1 = int(data[year1])
            else:
                rank1 = 1000
            x_coord1 = get_x_coordinate(CANVAS_WIDTH, i)
            y_coord1 = max(rank1 * 600 / 1000, GRAPH_MARGIN_SIZE)
            y_coord1 = min(y_coord1, CANVAS_HEIGHT - GRAPH_MARGIN_SIZE)

            if year2 in data:
                rank2 = int(data[year2])
            else:
                rank2 = 1000

            x_coord2 = get_x_coordinate(CANVAS_WIDTH, i + 1)
            y_coord2 = max(rank2 * 600 / 1000, GRAPH_MARGIN_SIZE)
            y_coord2 = min(y_coord2, CANVAS_HEIGHT - GRAPH_MARGIN_SIZE)

            color = COLORS[cnt % len(COLORS)]
            canvas.create_line(x_coord1, y_coord1, x_coord2, y_coord2, fill=color)

            if rank1 == 1000:
                rank1 = "*"
            canvas.create_text(
                x_coord1 + TEXT_DX,
                y_coord1,
                text=name + " " + str(rank1),
                fill=color,
                anchor=tkinter.NW,
            )

            if i == len(YEARS) - 2:
                if rank2 == 1000:
                    rank2 = "*"
                canvas.create_text(
                    x_coord2 + TEXT_DX,
                    y_coord2,
                    text=name + " " + str(rank2),
                    fill=color,
                    anchor=tkinter.NW,
                )
        cnt += 1


def main():
    # Load data
    name_data = babynames.read_files(FILENAMES)

    # Create the window and the canvas
    top = tkinter.Tk()
    top.wm_title("Baby Names")
    canvas = gui.make_gui(
        top, CANVAS_WIDTH, CANVAS_HEIGHT, name_data, draw_names, babynames.search_names
    )

    # Call draw_fixed_lines() once at startup so we have the lines
    # even before the user types anything.
    draw_fixed_lines(canvas)

    # This line starts the graphical loop that is responsible for
    # processing user interactions and plotting data
    top.mainloop()


if __name__ == "__main__":
    main()
