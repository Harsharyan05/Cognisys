from app.architecture.entry_point_detector import EntryPointDetector


def main():
    detector = EntryPointDetector(".")

    results = detector.detect()

    print("\nDetected Entry Points\n" + "-" * 40)

    if not results:
        print("No entry points found.")
        return

    for entry in results:
        print(f"File       : {entry['file']}")
        print(f"Path       : {entry['path']}")
        print(f"Framework  : {entry['framework']}")
        print(f"Confidence : {entry['confidence']}")
        print("-" * 40)


if __name__ == "__main__":
    main()