from ..etc import CustomEnum


class CompoundType(CustomEnum):
    ARRAY = "array"
    KEYMAP = "keymap"

    @staticmethod
    def translate(s: str) -> str:
        dct = {
            CompoundType.ARRAY: "ARRAY",
            CompoundType.KEYMAP: "KEYMAP",
        }
        return dct[s]
