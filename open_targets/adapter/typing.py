from typing import TypeAlias

AdaptedType: TypeAlias = int | float | str | bool | list["AdaptedType"] | dict["AdaptedType", "AdaptedType"] | bytearray
