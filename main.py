import os

import openai
import typer
from dotenv import load_dotenv
from rich import print
from rich.console import Console
from rich.table import Table

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


class Atenea(object):
    __context = {"role": "system", "content": "Test content"}
    __messages = [__context]

    @classmethod
    def main(cls) -> None:
        print("🤖 [bold green]Atenea[/bold green]")
        table = Table("Command", "Description", header_style="green")
        table.add_row("exit", "exit application")
        table.add_row("new", "Create new chat")
        print(table)

        console = Console()
        while True:
            content = cls.__parse_prompt()
            cls.__messages.append({"role": "user", "content": content})

            with console.status("[bold green]"):
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo", messages=cls.__messages
                )
            response_content = response.choices[0].message.content

            cls.__messages.append({"role": "assistant", "content": response_content})

            print(f"🤖: [white]{response_content}[/white]")

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
        return typer.prompt("\nHow can i help you?")

    @classmethod
    def __confirm_exit(cls) -> None:
        exit = typer.confirm("Are you sure?")
        if exit:
            raise typer.Abort()

    @classmethod
    def __new_chat(cls) -> None:
        cls.__messages = [cls.__context]
        print("🤖 New chat created")


if __name__ == "__main__":
    typer.run(Atenea.main)
