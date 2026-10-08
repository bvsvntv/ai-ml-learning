import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-q", "--query")

    args = parser.parse_args()
    print("query: ", args.query)


if __name__ == "__main__":
    main()
