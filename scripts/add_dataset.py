from argparse import ArgumentParser


def main():
    ap = ArgumentParser()
    ap.add_argument("DATASET")
    ap.add_argument("CORPUS_NAME")
    args = ap.parse_args()


if __name__ == "__main__":
    main()
