def print_file_lines(filename):
    # print line number and content from file
    with open(filename, 'rt') as f:
        for i, line in enumerate(f, 1):
            print(i, line)


def search_str_lines1(matching, filename):
    # search line number from file
    with open(filename, 'rt', encoding='latin-1') as f:
        for i, line in enumerate(f, 1):
            if matching in line:
                print(i, line)
                break
    return i


def search_str_lines2(matching, filename):
    # search line number from file
    with open(filename, 'rt', encoding='latin-1') as f:
        for i, line in enumerate(f, 1):
            if line == matching + '\n':
                print(i, line)
                break
    return i


if __name__ == '__main__':
    matching = "Accept-Ranges: bytes"
    filename = "Bboom.flv"
    row = search_str_lines2(matching, filename)
    print(row)
