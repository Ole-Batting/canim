import argparse
import os

import cv2
import numpy as np
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import ImageFormatter
from tqdm import tqdm

from canim.config import load_config, Config
from canim.utils import pad
from canim.writer import VideoWriter


def syntax_highlighted_image(code: str, cfg: Config) -> np.ndarray:
    formatter = ImageFormatter(font_name=cfg.font_name, font_size=cfg.font_size, style=cfg.theme,
                               line_numbers=False, image_pad=cfg.font_size, line_pad=cfg.font_size * 2 // 3)
    image_bytes = highlight(code, PythonLexer(), formatter)
    nparr = np.asarray(bytearray(image_bytes), dtype="uint8")
    img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img_np


def read_py_file(path: str) -> str:
    with open(path, 'r') as py_file:
        py_str = py_file.read() + u'\xa0'
    lines = py_str.split("\n")
    lines_new = []
    n_chars = 0
    for l in lines[1:]:
        if "# !!" in l:
            cmd = l.split("# !!")[1]
            if cmd == "ignore":
                continue
        else:
            n_chars += len(l) + 1
            lines_new.append(l)
    py_str = "\n".join(lines_new)
    return py_str


class TypeStream:
    in_path: str
    out_path: str
    config: Config
    code_string: str
    render_mode: str
    render_mode_to_method: dict
    tail: int

    def __init__(self, in_path: str, out_folder: str, config: Config, tail: int = 0):
        self.in_path = in_path
        self.out_folder = out_folder
        self.config = config
        self.tail = tail

        self.name = os.path.basename(self.in_path.replace('.', "_"))
        self.out_path = os.path.join(self.out_folder, self.name)
        print(self.out_path)

        self.code_string = read_py_file(self.in_path)
        print(len(self.code_string))

    def run(self):
        self.animate()

    def center(self, code):
        code = pad(code, self.config)
        return code

    def animate(self):
        video_writer = VideoWriter(self.out_path, self.config)
        video_frame = None

        for i in tqdm(range(len(self.code_string))):
            sub_string = self.code_string[:i]
            sub_lines = sub_string.split('\n')
            if all([s == ' ' for s in sub_lines[-1]]) and sub_lines[-1] != "":
                continue
            code_image = syntax_highlighted_image(sub_string + chr(9612), self.config)
            video_frame = self.center(code_image)
            video_writer.write(video_frame)

        for i in range(self.tail):
            video_writer.write(video_frame)

        video_writer.release()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--in-path", type=str, required=True, help="input file path")
    parser.add_argument("--out-path", type=str, required=True, help="output file path")
    parser.add_argument("--lq", dest="config", action="store_const",
                        const="canim/configs/prototype.yaml", default="canim/configs/production.yaml",
                        help="for quick prototyping")
    parser.add_argument("--set-width", type=int, default=None, help="overwrite em width")
    parser.add_argument("--tail", type=int, default=0, help="tail frames")
    args = parser.parse_args()

    cfg = load_config(args.config)
    if args.set_width is not None:
        cfg.em_width = args.set_width

    if os.path.isdir(args.in_path):
        for in_path in os.listdir(args.in_path):
            if in_path[0] == '_':
                continue
            print(in_path)
            typestream = TypeStream(in_path=os.path.join(args.in_path, in_path), out_folder=args.out_path, config=cfg, tail=args.tail)
            typestream.run()
    else:
        typestream = TypeStream(in_path=args.in_path, out_folder=args.out_path, config=cfg, tail=args.tail)
        typestream.run()
