#!/usr/bin/env python3
import argparse
import pathlib
from src.analyzer import analyze_script

parser = argparse.ArgumentParser(description='Run script analyzer on a file')
parser.add_argument('file', help='Path to script file')
parser.add_argument('--mode', choices=['local','llm'], default='local')
parser.add_argument('--title', default=None)
args = parser.parse_args()

text = pathlib.Path(args.file).read_text(encoding='utf-8')
res = analyze_script(text, title=args.title or args.file, mode=args.mode)
import json
print(json.dumps(res, ensure_ascii=False, indent=2))
