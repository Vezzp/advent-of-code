import enum
from types import MappingProxyType


class Lang(str, enum.Enum):
    PYTHON = "python"
    CPP = "cpp"
    GOLANG = "go"
    RUST = "rust"


LANG_TO_FILE_EXT = MappingProxyType(
    {
        Lang.PYTHON: ".py",
        Lang.CPP: ".cpp",
        Lang.GOLANG: ".go",
        Lang.RUST: ".rs",
    }
)

assert len(Lang) == len(LANG_TO_FILE_EXT), "Not all registered languages have extension"
assert all(ext.startswith(".") for ext in LANG_TO_FILE_EXT.values()), (
    "Not all extensions start with a period"
)
