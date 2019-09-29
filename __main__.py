import requests
import click
import textwrap

width = 0


def wrap_print(content, indent=0):
    global width
    print(
        textwrap.indent(
            textwrap.fill(content, (width if width else 80) - indent), " " * indent
        )
    )


@click.command()
def main():
    global width
    width = click.get_terminal_size()[0]

    while True:
        click.clear()

        print("Wilkommen zu ParteiDuell - Der Klieh")
        print("")

        r = requests.get("https://solver.cloud:440/list")
        json = r.json()
        wrap_print(json[0]["these"])
        print()
        wrap_print(json[0]["statement"])
        print()

        keys = list(json[0]["possibleAnswers"])
        print(", ".join(f"{i}: {answer}" for i, answer in enumerate(keys)))

        party = input("> ")
        try:
            party = int(party)
            party = keys[party]
        except ValueError as error:
            print(error)

        print()
        print()
        if json[0]["answer"] == party:
            print("Richtig!")
        else:
            print(f"Falsch, diese Aussage war von {json[0]['answer']}")
            print()
            print(f"Die Partei {party} hat folgendes Statement abgegeben:\n")
            wrap_print(json[0]["possibleAnswers"][party], indent=4)
        print()
        click.pause()


if __name__ == "__main__":
    main()
