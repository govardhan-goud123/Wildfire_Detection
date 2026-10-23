"""Train the TensorFlow wildfire detector from the command line."""

import argparse
from model_utils import train_and_save


def main():
    parser = argparse.ArgumentParser(description="Train the wildfire detector.")
    parser.add_argument("--epochs", type=int, default=5, help="Number of training epochs.")
    args = parser.parse_args()

    if args.epochs < 1:
        parser.error("--epochs must be at least 1")

    _, history, test_results = train_and_save(epochs=args.epochs)
    print("\nTest-set results:")
    for metric, value in test_results.items():
        print(f"{metric}: {value:.4f}")
    print("\nSaved model: models/wildfire_detector.keras")


if __name__ == "__main__":
    main()
