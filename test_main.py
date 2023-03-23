import typer
from typer.testing import CliRunner

from .main import Atenea

runner = CliRunner()


app = typer.Typer()
app.command()(Atenea.main)

constants: dict[str, str] = {
    "PROMPT_STRING": "How can i help you?: %s",
    "PROMT_EXIT": "Are you sure? [y/N]: %s",
    "NEW_CHAT": "New chat created",
}
get_constant = lambda const: constants[const]


def test_prompt_exit():
    input = "\n".join(["exit", "N", "exit", "y"])
    result = runner.invoke(app, input=input)

    PROMPT_STRING = get_constant("PROMPT_STRING") % "exit"
    EXIT_YES_STRING = get_constant("PROMT_EXIT") % "y"
    EXIT_NO_STRING = get_constant("PROMT_EXIT") % "N"

    assert PROMPT_STRING in result.stdout
    assert result.stdout.count(PROMPT_STRING) == 2
    assert EXIT_YES_STRING in result.stdout
    assert result.stdout.count(EXIT_YES_STRING) == 1
    assert EXIT_NO_STRING in result.stdout
    assert result.stdout.count(EXIT_NO_STRING) == 1
    assert result.exit_code == 1


def test_confirm_exit():
    input = "\n".join(["exit", "y"])
    result = runner.invoke(app, input=input)

    assert result.exit_code == 1
    assert "Aborted." in result.stdout


def test_new_chat():
    input = "\n".join(["new", "exit", "y"])
    result = runner.invoke(app, input=input)

    PROMPT_STRING = get_constant("PROMPT_STRING") % "new"
    NEW_CHAT_STRING = get_constant("NEW_CHAT")

    assert PROMPT_STRING in result.stdout
    assert NEW_CHAT_STRING in result.stdout


def test_chat_prompt():
    question = "when the fall of the berlin wall occurred, only the year should be in the answer, without additional characters"

    input = "\n".join([question, "exit", "y"])
    result = runner.invoke(app, input=input)

    assert "1989" in result.stdout
