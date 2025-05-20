def obtain_header(path) -> str:
    with open(path, "r") as file:
        header = file.readline().strip()
    return header
