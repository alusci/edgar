import argparse

# Import the ChatApplication from utils
from utils.story_generator import ChatApplication
from utils.cli import cli_main
from utils.ui import ui_main

def main():
    parser = argparse.ArgumentParser(description="EDGAR - AI Story Generator")
    parser.add_argument("--ui", action="store_true", help="Launch the Gradio UI")
    parser.add_argument("--input", type=str, default="data/inputs/stone_giant_heroons.json",
                        help="Path to the JSON input file (default: data/inputs/stone_giant_heroons.json)")
    args = parser.parse_args()
    
    if args.ui:
        ui_main()
    else:
        cli_main(input_file=args.input)

if __name__ == "__main__":
    main()
