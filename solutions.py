from collections.abc import Sequence
from .project_types import PlayerId, Cell, Symbol, Feedback, Field
from .win_conditions import WinCondition
from .symbol_managers import SymbolManager


class GridGameModel:
    def __init__(
        self, grid_size: int, player_symbols: Sequence[Symbol], 
        player_count: int, win_condition: WinCondition, symbol_manager: SymbolManager, variant: str):
        if player_count <= 1:
            raise ValueError(f'Must have at least two players (found {player_count})')

        self._field = Field(grid_size)
        self._player_count = player_count
        self._win_condition = win_condition
        self._symbol_manager = symbol_manager
        self._current_player: PlayerId = 1

    @property
    def occupied_cells(self) -> dict[Cell, Symbol]:
        return self._field.occupied_cells

    @property
    def grid_size(self):
        return self._field.grid_size

    @property
    def is_game_over(self):
        return self.winner is not None or not self._field.has_unoccupied_cell()

    @property
    def current_player(self) -> PlayerId:
        return self._current_player

    @property
    def next_player(self) -> PlayerId:
        return 1 if self._current_player == self._player_count else self._current_player + 1

    @property
    def winner(self) -> PlayerId | None:
        return self._win_condition.check_winner(self._field)

    def get_symbol_choices(self, player: PlayerId) -> list[Symbol]:
        return self._symbol_manager.get_valid_symbols(player)

    def place_symbol(self, symbol: Symbol, cell: Cell) -> Feedback:
        if self.is_game_over:
            return Feedback.GAME_OVER

        if symbol not in self.get_symbol_choices(self.current_player):
            return Feedback.INVALID_SYMBOL

        if not self._field.is_within_bounds(cell):
            return Feedback.OUT_OF_BOUNDS

        if self._field.get_symbol_at(cell) is not None:
            return Feedback.OCCUPIED

        self._field.place_symbol(symbol, cell)
        self._switch_to_next_player()
        return Feedback.VALID

    def _switch_to_next_player(self):
        self._current_player = self.next_player





from abc import ABC, abstractmethod
from .project_types import Field, PlayerId


class WinCondition(ABC):
    @abstractmethod
    def check_winner(self, field: Field) -> PlayerId | None:
        pass



from .win_conditions import WinCondition
from .project_types import Field, Cell

class TicTacToeWinCondition(WinCondition):
    def check_winner(self, field: Field) -> PlayerId | None:
        row_groups = [[Cell(row, k) for k in field.valid_coords] for row in field.valid_coords]
        col_groups = [[Cell(k, col) for k in field.valid_coords] for col in field.valid_coords]
        diagonals = [[Cell(k, k) for k in field.valid_coords], [Cell(k, field.grid_size - k + 1) for k in field.valid_coords]]

        for groups in [row_groups, col_groups, diagonals]:
            for group in groups:
                if (basis := field.get_symbol_at(group[0])) is not None and field.are_all_equal_to_basis(basis, group):
                    return basis  # Assuming symbols map to player IDs
        return None




from abc import ABC, abstractmethod
from .project_types import PlayerId, Symbol


class SymbolManager(ABC):
    @abstractmethod
    def get_valid_symbols(self, player: PlayerId) -> list[Symbol]:
        pass




class TicTacToeSymbolManager(SymbolManager):
    def __init__(self, player_symbols: dict[PlayerId, Symbol]):
        self._player_to_symbol = player_symbols

    def get_valid_symbols(self, player: PlayerId) -> list[Symbol]:
        return [self._player_to_symbol[player]]







def make_model(grid_size, player_count, variant, symbols):
    if variant == "tictactoe":
        return GridGameModel(grid_size, symbols, player_count, TicTacToeWinCondition(), TicTacToeSymbolManager(symbols))
    elif variant == "wild":
        return GridGameModel(grid_size, symbols, player_count, WildTicTacToeWinCondition(), WildTicTacToeSymbolManager(symbols))
    elif variant == "notakto":
        if len(symbols) != 1:
            raise ValueError("Notakto requires exactly one symbol")
        return GridGameModel(grid_size, symbols, player_count, NotaktoWinCondition(), NotaktoSymbolManager(symbols))
    elif variant == "pick15":
        if symbols:
            raise ValueError("Pick15 does not accept symbols")
        return GridGameModel(grid_size, symbols, player_count, Pick15WinCondition(), Pick15SymbolManager())



