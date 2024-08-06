import pygetwindow as gw


def list_window_sizes():
    windows = gw.getAllWindows()
    for window in windows:
        if window.visible:
            print(f"Title: '{window.title}' - Width: {window.width} - Height: {window.height}")


if __name__ == "__main__":
    list_window_sizes()
