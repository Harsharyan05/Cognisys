from app.architecture.service_detector import ServiceDetector


def main():

    detector = ServiceDetector(".")

    services = detector.detect()

    print("\nDetected Services")
    print("=" * 60)

    if not services:
        print("No services detected.")
        return

    for service in services:

        print(service)


if __name__ == "__main__":
    main()