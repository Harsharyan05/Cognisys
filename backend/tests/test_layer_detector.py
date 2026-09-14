from app.architecture.layer_detector import LayerDetector


def main():
    detector = LayerDetector(".")

    layers = detector.detect()

    print("\nDetected Architecture Layers")
    print("=" * 50)

    if not layers:
        print("No architectural layers detected.")
        return

    for layer, folders in layers.items():
        print(f"\n[{layer}]")

        for folder in folders:
            print(f"  ├── {folder}")

    print("\nTotal Layers Detected :", len(layers))


if __name__ == "__main__":
    main()