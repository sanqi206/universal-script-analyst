from src.analyzer import analyze_script


def main():
    import argparse
    import json
    import pathlib

    parser = argparse.ArgumentParser(description="Run script analyzer on a file")
    parser.add_argument("file", help="Path to script file")
    parser.add_argument("--mode", choices=["local", "llm"], default="local")
    parser.add_argument("--title", default=None)
    args = parser.parse_args()

    text = pathlib.Path(args.file).read_text(encoding="utf-8")
    result = analyze_script(text, title=args.title or args.file, fmt="plain", mode=args.mode)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
