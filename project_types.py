from dataclasses import dataclass
from enum import Enum, auto
from collections.abc import Iterable


# Probably better as `typing.NewType('PlayerId', int)`
type PlayerId = int

type Symbol = str


@dataclass(frozen=True)
class Cell:
    row: int
    col: int


class Feedback(Enum):
    VALID = auto()
    OUT_OF_BOUNDS = auto()
    OCCUPIED = auto()
    INVALID_SYMBOL = auto()
    GAME_OVER = auto()


class Field:
    def __init__(self, grid_size: int):
        self._grid_size = grid_size
        self._valid_coords = list(range(1, self._grid_size + 1))
        self._valid_cells = set(
            Cell(r, c)
            for r in self._valid_coords
            for c in self._valid_coords
        )
        self._grid: dict[Cell, Symbol | None] = {
            cell: None for cell in self._valid_cells
        }

    @property
    def valid_coords(self):
        return list(self._valid_coords)

    @property
    def valid_cells(self):
        return list(self._valid_cells)

    @property
    def grid_size(self):
        return self._grid_size

    @property
    def occupied_cells(self) -> dict[Cell, Symbol]:
        return {
            cell: symbol for cell, symbol in self._grid.items()
            if symbol is not None
        }

    def is_within_bounds(self, cell: Cell) -> bool:
        return (
            1 <= cell.row <= self._grid_size and
            1 <= cell.col <= self._grid_size
        )

    def place_symbol(self, symbol: Symbol, cell: Cell):
        assert self.is_within_bounds(cell)

        self._grid[cell] = symbol

    def get_symbol_at(self, cell: Cell) -> Symbol | None:
        return self._grid.get(cell)

    def has_unoccupied_cell(self):
        return any(
            True for cell in self.valid_cells
            if self.get_symbol_at(cell) is None
        )

    def are_all_equal_to_basis(self, basis: Symbol, group: Iterable[Cell]):
        return all(self.get_symbol_at(cell) == basis for cell in group)
