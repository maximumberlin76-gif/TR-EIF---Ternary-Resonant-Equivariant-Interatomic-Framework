"""Execution eligibility for balanced ternary transitions in TR-EIF."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TernaryExecutionGuard:
    """Eligibility controls for one ternary execution step."""

    allow_neutral_entry: bool = True
    allow_neutral_exit: bool = True

    def __post_init__(self) -> None:
        if not isinstance(self.allow_neutral_entry, bool):
            raise TypeError(
                "allow_neutral_entry must be a boolean value."
            )

        if not isinstance(self.allow_neutral_exit, bool):
            raise TypeError(
                "allow_neutral_exit must be a boolean value."
            )

    @classmethod
    def unrestricted(cls) -> TernaryExecutionGuard:
        """Return a guard permitting both neutral entry and neutral exit."""

        return cls(
            allow_neutral_entry=True,
            allow_neutral_exit=True,
        )

    @classmethod
    def hold(cls) -> TernaryExecutionGuard:
        """Return a guard permitting neither neutral entry nor neutral exit."""

        return cls(
            allow_neutral_entry=False,
            allow_neutral_exit=False,
        )

    @classmethod
    def neutral_entry_only(cls) -> TernaryExecutionGuard:
        """Return a guard permitting active-neutral entry only."""

        return cls(
            allow_neutral_entry=True,
            allow_neutral_exit=False,
        )

    @classmethod
    def neutral_exit_only(cls) -> TernaryExecutionGuard:
        """Return a guard permitting active-neutral exit only."""

        return cls(
            allow_neutral_entry=False,
            allow_neutral_exit=True,
        )
