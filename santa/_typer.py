# Utilities for typer package.

import dataclasses
import functools
import inspect
from collections.abc import Callable
from datetime import datetime
from typing import TYPE_CHECKING, Annotated, ClassVar, Protocol, TypeAlias, cast

import click
import typer

from ._langs import Lang

if TYPE_CHECKING:
    from typing import Any, Concatenate, Literal, overload

    @overload
    def transfer_signature[**P, R](
        fn: Callable[P, R],
        /,
    ) -> Callable[[Callable[..., Any]], Callable[P, R]]: ...

    @overload
    def transfer_signature[**P, R](
        fn: Callable[Concatenate[Any, P], R],
        /,
        *,
        is_method: Literal[True],
    ) -> Callable[[Callable[..., Any]], Callable[P, R]]: ...

    @overload
    def transfer_signature[**P, R](
        fn: Callable[P, Any],
        rettype: R,
        /,
    ) -> Callable[[Callable[..., Any]], Callable[P, R]]: ...

    @overload
    def transfer_signature[**P, R](
        fn: Callable[Concatenate[Any, P], Any],
        rettype: R,
        /,
        *,
        is_method: Literal[True],
    ) -> Callable[[Callable[..., Any]], Callable[P, R]]: ...


def transfer_signature(*args, **kwargs):  # type: ignore # noqa
    def decorator(fn):
        return fn

    return decorator


class Handler(Protocol):
    def __call__(self, *, ctx: typer.Context | click.Context, **kwargs) -> None: ...


app = typer.Typer()


@dataclasses.dataclass(kw_only=True, slots=True)
class CommonOpts:
    ATTRNAME: ClassVar[str] = "_common_opts_"

    year: Annotated[
        int,
        typer.Option("-y", "--year", help="Contest year"),
    ] = datetime.now().year
    day: Annotated[
        int,
        typer.Option("-d", "--day", help="Contest day"),
    ]
    lang: Annotated[
        Lang,
        typer.Option("-l", "--lang", help="Contest solution language"),
    ]


@transfer_signature(app.command)
def command(*command_args, **command_kwargs):
    def decorator(fn: Handler, /) -> Handler:
        @functools.wraps(fn)  # type: ignore
        def wrapper(*args, **kwargs):
            assert len(args) == 0, "Passed arguments must be kwargs only"

            ctx = kwargs.pop("ctx", ...)
            assert isinstance(ctx, typer.Context | click.Context), (
                f"Passed kwargs must contain typer context: {kwargs}"
            )

            opts = CommonOpts(
                **{field.name: kwargs.pop(field.name) for field in dataclasses.fields(CommonOpts)}
            )
            setattr(ctx, CommonOpts.ATTRNAME, opts)

            return fn(ctx=ctx, **kwargs)

        setattr(
            wrapper,
            "__signature__",
            inspect.Signature(
                [
                    *inspect.signature(wrapper).parameters.values(),
                    *(
                        inspect.Parameter(
                            name=field.name,
                            kind=inspect.Parameter.KEYWORD_ONLY,
                            default=field.default,
                            annotation=field.type,
                        )
                        for field in dataclasses.fields(CommonOpts)
                    ),
                ]
            ),
        )

        return cast(Handler, app.command(*command_args, **command_kwargs)(wrapper))

    return decorator


Part: TypeAlias = Annotated[
    int | None,
    typer.Option(
        "-p",
        "--part",
        help="Which part to solve. Leave blank for both parts.",
        min=1,
        max=2,
    ),
]
