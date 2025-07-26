def main():
    print("Hello from 11-agent-sdk!")


if __name__ == "__main__":
    main()


def hello(name: str) -> str:
    if not isinstance(name , str):
        raise TypeError("Name must be string")


hello(12) # This will throw error due to type error

