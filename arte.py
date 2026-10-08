import re
import shutil


_SOURCE_ART = """\n
                        \033[31mS H A R I N G A N\033[0;0;0m
\033[0;0;0m⠀⠀\033[34m⢈⣿⣏\033[0;0;0m⠈⢏⠉⠉⠉⠉⠉⠉⢉⣿⢝⢝⢝⢝⢝⢝⢝⢝⢝⢝⢝⢝⢝⢝⢝⢝⣿⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⢿⣿⠉⢩⣍⠙⠉⣹⠟⠉⢈⠏⠉⢹⢡
⠀⠀⠀\033[34m⣤\033[0;0;0m⡿\033[34m⠂⠀\033[0;0;0m⠑⠄⠀⠀⠀⠀⢸⣗⢕⢕⢕⢕⢕⢕⢕⢕⢕⢕⢕⢕⢕⢕⢕⣵⡟⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠳⠤⠄⠀⡴⠋⠀⢀⡜⠀⠀⡼⠀
⠀⠀⠀\033[34m⢿⣅⠀\033[0;0;0m⠛⠀⠀⠀⠀⠀⠀⢸⣗⢕⢕⢕⢕⢕⢕⢕⢕⢕⢕⢕⢕⢕⢕⢿⣿⠁⠀⠀⠀⢰⡀⠘⠄⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢺⡇⠀⢀⠏⠀⠀⠀⡇⠀
\033[0;0;0m⡄⠀\033[34m⠐⢆\033[0;0;0m⢙⢷⣤⡀⠀⠀⠀⠀⠀⠘⣷⣕⢕⢕⢕⢕⢕⢕⢕⢕⢕⢕⢕⢕⡿⠁⠀⠀⠀⠀⠀⣸⠁⠀⢰⠀⠀⠸⠀⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠉⠀⠀⡏⠀⠀⠀⠀⡇⠀
\033[34m⣷⡶⣶⠏\033[0;0;0m⢹⣕⢽⣗⢷⣦⢄⣀⠀⠀⠈⠛⠷⣵⣵⣕⣵⣕⣵⢕⢕⢕⣵⠟⠁⠀⢠⣄⠀⠀⠀⡇⠀⠀⢸⠀⠀⠀⠂⠈⡇⠘⡄⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⢠⠃⠀⢀⡔⠀⠀⠀⠀⠀⠇⠀
\033[34m⡿⠀⠀⠀\033[0;0;0m⢸⣿⣗⢵⢵⣝⢽⣽⢵⢷⢶⣄⢤⣀⠀⠈⠉⠉⠙⠛⠛⠛⠏⠀⠀⠄⢸⣿⢷⣤⣤⠀⣤⡄⠈⠀⠀⠀⠀⡸⠁⠀⡇⠀⠀⠀⢠⠚⠁⠈⢀⠀⠀⡠⠋⠀⣤⠀⠀⠀⠀⠀⠀⠀⠠⣼
\033[34m⡇⠀⠀⠀\033[0;0;0m⢸⣿⠅⠐⢿⣷⢽⢕⢕⢕⢕⢝⢝⢷⣝⢷⢴⣄⣄⢀⢀⠠⠤⠤⢀⡀⢸⣗⢕⣵⠗⠀⠰⠁⢶⣄⣀⣀⣀⡁⣀⡄⠁⠀⠀⠀⠏⠀⠀⠀⠛⠒⠉⠀⠀⠰⠧⢄⡀⠀⠀⠀⣠⠂\033[34m⠠⢹
\033[34m⣿⡀\033[0;0;0m⣠⣟⢽⣗⠀⠀⢐⣝⢽⢕⢕⢕⢕⢕⢕⢕⢕⢕⢵⣝⢿⣝⢗⢷⣵⣴⣔⣄⣄⠙⠛⠟⢁⡀⠀⠀⢙⣿⣝⣽⠟⠁⠁⠀⢷⣶⣤⡤⠴⠒⠿⣤⣀⣀⣀⡀⠀⠀⠀⠀⠈⢶⠀⠘⠃⠀⠀⣾
\033[0;0;0m⣉⣵⠟⠁⢹⣗⠀⠀⢿⣗⢽⢕⢕⢕⣟⠛⠛⠟⠷⠷⢷⣿⣷⣝⢕⢷⣕⢕⢕⢝⢝⢷⣄⢄⠀⠠⠀⠀⠀⠀⠉⠁⢀⣀⣴⠶⠷⠅⠉⠁⠒⠛⠒⠦⠤⠀⠈⢷⡀⠀⠀⠀⠀⠘⠀⠀⣰⡄⠀\033[34m⢻
\033[0;0;0m⣟⡵⠁⢀⡀⢻⣄⠀⠀⢽⢕⢕⢕⢕⢝⣕⢿⣷⢷⡇⠀⠀⢉⣙⠷⢄⠙⢷⣵⣕⢕⢕⢝⢟⢗⢴⣷⢷⢷⢔⣴⠶⠋⣡⡄\033[31m⢠⡄⣰⢆\033[0;0;0m⣿⣶⣾⡟⠀⠊⠀⠀⠈⢷⡀⠀⠀⠀⠀⠀⠸⢟⢿⠀\033[34m⣾
\033[0;0;0m⣷⠁⠀⣼⠁⠀⠹⣷⣔⢟⢕⢕⢕⢕⢕⢕⢕⢕⢝⢷⢶⢶⢟⢟⢷⢖⢄⣄⣄⢵⣵⢕⢕⢕⢟⢝⢵⣷⢝⢁⢥⣴⢾⢿⢷\033[31m⣭⣞⣕\033[0;0;0m⣿⢿⢟⣅⣴⢷⢷⣄⣄⠀⠈⢷⡀⠀⠀⠀⣀⡄⠈⣗⢵⣼
\033[0;0;0m⡏⠀⠘⡏⠀⠀⠀⢹⣷⣗⢵⢕⢕⢕⢕⢕⢕⢕⢕⢕⢕⢕⢕⢕⢗⢝⢝⢕⢕⣷⣵⠷⠟⠛⠛⠙⠛⠃⢹⣷⢗⢕⢕⢕⢕⢷⣕⢕⢵⢗⢟⢝⢕⢕⢕⢕⢝⢷⡄⠈⣷⠀⠀⣸⠁⠀⠀⢰⢕⢽
\033[0;0;0m⡇⠀⠀⡇⠀⠀⠀⠀⠙⠁⠹⣗⢕⢕⢕⢕⢕⢕⢕⢕⢕⢕⢕⢕⣕⣵⠷⠟⠋⠁⠀⠀⠀⠀⠀⠀⢹⡄⠀⠙⢷⣵⣕⢕⢕⢕⣷⢕⣿⢕⢕⢕⢕⢕⢕⢕⢕⣿⠁⣰⠿⠀⠀⢻⠀⠀⠀⠀⣕⢽
\033[0;0;0m⡇⠀⠀⣇⠀⠀⠀⠀⠀⠀⠀⠻⢷⣕⢕⢕⢕⢕⢕⣕⣵⡵⠟⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⠆⠀⢣⠀⠀⠀⠀⠙⠻⢷⣵⣟⢕⣽⢕⢕⢕⢕⢕⢕⢕⣽⢅⠀⠀⠀⠀⠀⢸⠀⠀⠀⠀⣗⢽
\033[0;0;0m⡇⡀⠀⢹⠀⠀⠀⠀⠀⠀⠀⢢⠀⠉⠛⠷⠷⠟⠛⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⢇⠀⠀⠀⠀⠀⠀⠉⠛⠱⢷⣵⣕⣕⣕⣕⣵⡿⠇⠀⠀⠀⠀⠀⠀⢸⠀⠀⠀⠀⢗⢽
\033[0;0;0m⣇⢁⠀⠈⣇⠀⠀⠀⠀⠀⠀⠘⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⠀⠀⠀⠈⢆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠉⠉⠁⢠⠂⠀⠀⠀⠀⠀⠀⢸⠀⠀⠀⢸⢕⢽
\033[0;0;0m⣟⠄⠆⠀⠘⡄⠀⢀⠀⠀⠀⠀⢹⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⠀⠀⠀⠘⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠏⠀⠀⠀⠀⠀⠀⢀⡏⠀⠀⠀⢖⢕⢽
\033[0;0;0m⣗⢕⠈⠀⠀⠹⡄⠈⠀⠀⠀⠀⠀⢳⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡸⠀⠀⠀⠀⠀⢰⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡞⠀⠀⠀⠀⠀⠀⠀⡼⠀⠀⠀⣸⢕⢕⢽
\033[0;0;0m⣗⣕⣵⣀⣀⣀⣹⣆⡀⠀⠀⠀⠀⠈⣳⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣠⣊⣀⠀⠀⠀⢀⣀⣌⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣸⡁⠀⠀⡀⠀⣀⣀⣼⣁⣀⣀⣠⣗⣕⣕⣽\033[0;0;0m
"""

def compact_art(source: str, columns: int) -> str:
    reset = '\033[0m'
    lines = source.strip('\n').splitlines()
    title = lines[0].strip()
    picture = []
    color = reset

    # Read visible cells separately from ANSI colors before cropping the frame.
    for line in lines[1:]:
        cells = []
        for token in re.findall(r'\x1b\[[0-9;]*m|[^\x1b]', line):
            if token.startswith('\033['):
                color = token
            else:
                cells.append((token, color))
        picture.append(cells)

    picture = [line[1:-1] for line in picture[1:-1]]
    source_width = min(len(line) for line in picture)
    source_height = len(picture)
    max_width = max(1, columns - 1)
    # A short terminal panel must not squash the drawing into a few lines.
    max_height = 12
    # Keep the original width when it fits, compressing only the height.
    width = min(source_width, max_width)
    height = min(source_height, max_height)

    # Resize the individual Braille dots, not whole text lines, to retain detail.
    dots = ((0, 3), (1, 4), (2, 5), (6, 7))
    rendered = []
    for y in range(height):
        output = []
        active_color = reset
        for x in range(width):
            mask = 0
            colors = []
            for dy in range(4):
                sy = min(source_height * 4 - 1,
                         int((y * 4 + dy + 0.5) * source_height / height))
                for dx in range(2):
                    sx = min(source_width * 2 - 1,
                             int((x * 2 + dx + 0.5) * source_width / width))
                    char, dot_color = picture[sy // 4][sx // 2]
                    value = ord(char) - 0x2800
                    if 0 <= value <= 255 and value & (1 << dots[sy % 4][sx % 2]):
                        mask |= 1 << dots[dy][dx]
                        colors.append(dot_color)
            cell_color = max(colors, key=colors.count) if colors else active_color
            if cell_color != active_color:
                output.append(cell_color)
                active_color = cell_color
            output.append(chr(0x2800 + mask))
        rendered.append(''.join(output) + reset)

    # The Japanese title occupies 17 terminal columns.
    if max_width >= 17:
        rendered.insert(0, ' ' * max(0, (width - 17) // 2) + title + reset)
    return '\n'.join(rendered)


terminal = shutil.get_terminal_size(fallback=(80, 24))
ART = compact_art(_SOURCE_ART, terminal.columns)

if __name__ == '__main__':
    print(ART)
