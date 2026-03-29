import typer


def add(a: int, b: int) -> None:
    print(f"{a} + {b} = {a+b}")


def main():
    typer.run(add)
