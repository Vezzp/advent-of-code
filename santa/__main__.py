from . import _initer, _solver, _tester
from ._typer import app, command

command(
    name="init",
    help="Init directory and draft template for daily puzzle",
)(_initer.init_handler)

command(
    name="solve",
    help="Solve puzzle",
)(_solver.solve_handler)

command(
    name="test",
    help="Test puzzle",
)(_tester.test_handler)

app()
