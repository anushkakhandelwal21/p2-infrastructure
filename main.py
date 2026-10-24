
from recorder import save_run


def main():
    print("P2 - Autonomous Bug Resolution")
    print("Infrastructure module is starting...")

    record_path = save_run({
        "status": "started",
        "module": "P2 infrastructure"
    })

    print(f"Run record saved: {record_path}")


if __name__ == "__main__":
    main()
