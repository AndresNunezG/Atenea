import os

import openai
import typer
from dotenv import load_dotenv
from rich import box, print
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table


class Atenea(object):
    __context = {"role": "system", "content": "Test content"}
    __messages = [__context]

    @classmethod
    def __config(cls):
        load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")

    @classmethod
    def main(cls) -> None:
        console = Console()
        cls.__print_intro()
        cls.__config()
        while True:
            content = cls.__parse_prompt()
            cls.__messages.append({"role": "user", "content": content})

            with console.status("[slate_blue3]", spinner="aesthetic"):
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo", messages=cls.__messages
                )
            response_content = response.choices[0].message.content

            cls.__messages.append({"role": "assistant", "content": response_content})

            md = Markdown(response_content)
            console.print(Panel(md, padding=1))

    @classmethod
    def __print_intro(cls) -> None:
        print("✨ [bold slate_blue3]Camsky[/bold slate_blue3]", end=" ")
        print("- [bold italic grey66]ChatGPT 3.5[/bold italic grey66]")
        table = Table(box=box.ROUNDED)
        table.add_column("Command", style="slate_blue3")
        table.add_column("Description", style="white")
        table.add_row("exit", "exit application")
        table.add_row("new", "create new chat")
        print(table)

    @classmethod
    def __parse_prompt(cls) -> str:
        prompt = cls.__ask_prompt()

        if prompt == "exit":
            cls.__confirm_exit()
            cls.__parse_prompt()
        if prompt == "new":
            cls.__new_chat()

        return prompt

    @classmethod
    def __ask_prompt(cls) -> str:
        return typer.prompt("\n▲ How can i help you?")

    @classmethod
    def __confirm_exit(cls) -> None:
        exit = typer.confirm("Are you sure?")
        if exit:
            raise typer.Abort()

    @classmethod
    def __new_chat(cls) -> None:
        cls.__messages = [cls.__context]
        print("💬 New chat created")


if __name__ == "__main__":
    typer.run(Atenea.main)
