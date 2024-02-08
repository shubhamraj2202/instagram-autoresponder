import argparse

from instagram_autoresponder import main


def execute():
    parser = argparse.ArgumentParser(
        description="Instagram Direct Message Autoresponder"
    )
    parser.add_argument("--config", type=str, help="Path to JSON configuration file")
    args = parser.parse_args()
    if args.config:
        main(args)
    else:
        print("Please provide a path to the JSON configuration file.")


if __name__ == "__main__":
    execute()
