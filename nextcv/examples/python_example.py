import nextcv


def main() -> None:
    print(nextcv.hello())
    data = bytes([0, 64, 128, 192, 255])
    print(list(nextcv.invert(data)))


if __name__ == "__main__":
    main()
