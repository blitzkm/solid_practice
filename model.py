from collections.abc import Sequence

from .project_types import PlayerId, Cell, Symbol, Feedback, Field


class WinConditions:
    def winner(self, field: Field, _symbol_to_player: dict[Symbol, PlayerId]) -> PlayerId | None:
        raise NotImplementedError

    def get_valid_symbols(self, player: PlayerId, _player_to_symbol: dict[PlayerId, Symbol]) -> list[Symbol]:
        return [_player_to_symbol[player]]


class TicTacToeWinConditions(WinConditions):
    def winner(self, field: Field, _symbol_to_player: dict[Symbol, PlayerId]) -> PlayerId | None:
        row_groups = [[Cell(row, k) for k in field.valid_coords] for row in field.valid_coords]
        col_groups = [[Cell(k, col) for k in field.valid_coords] for col in field.valid_coords]
        diagonals = [
            [Cell(k, k) for k in field.valid_coords],
            [Cell(k, field.grid_size - k + 1) for k in field.valid_coords],
        ]
        for groups in (row_groups, col_groups, diagonals):
            for group in groups:
                basis: Symbol | None = field.get_symbol_at(group[0])
                if basis is not None and field.are_all_equal_to_basis(basis, group):
                    winner: PlayerId | None = _symbol_to_player.get(basis)
                    assert winner is not None, f'Winning symbol {basis} in cell group {group} has no associated player'
                    return winner
        return None


class NotaktoWinConditions(WinConditions):
    def check_winner(self, field: Field, symbol_to_player: dict[Symbol, PlayerId]) -> PlayerId | None:
        return TicTacToeWinConditions().winner(field, symbol_to_player)


class WildTicTacToeWinConditions(WinConditions):
    def get_valid_symbols(self, player: PlayerId, player_to_symbol: dict[PlayerId, Symbol]) -> list[Symbol]:
        return list(player_to_symbol.values())

    def check_winner(self, field: Field, symbol_to_player: dict[Symbol, PlayerId]) -> PlayerId | None:
        return TicTacToeWinConditions().winner(field, symbol_to_player)


class Pick15WinConditions(WinConditions):
    def check_winner(self, field: Field, symbol_to_player: dict[Symbol, PlayerId]) -> PlayerId | None:
        target_sum: int = (field.grid_size * (field.grid_size ** 2 + 1)) // 2
        row_groups: list[list[Cell]] = [[Cell(row, k) for k in field.valid_coords] for row in field.valid_coords]
        col_groups: list[list[Cell]] = [[Cell(k, col) for k in field.valid_coords] for col in field.valid_coords]
        diagonals: list[list[Cell]] = [
            [Cell(k, k) for k in field.valid_coords],
            [Cell(k, field.grid_size - k - 1) for k in field.valid_coords],
        ]
        
        for groups in (row_groups, col_groups, diagonals):
            for group in groups:
                symbols: list[Symbol | None] = [field.get_symbol_at(cell) for cell in group]
                if all(symbol is not None for symbol in symbols):
                    symbol_values: list[int] = [int(symbol) for symbol in symbols if symbol is not None]
                    if sum(symbol_values) == target_sum:
                        last_symbol: Symbol | None = symbols[-1]
                        assert last_symbol is not None, f'Last symbol in winning group {group} is None'
                        winner: PlayerId | None = symbol_to_player.get(last_symbol)
                        assert winner is not None, f'Winning symbol {last_symbol} in cell group {group} has no associated player'
                        return winner
        return None



class GridGameModel:
    def __init__(self, grid_size: int, player_symbols: Sequence[Symbol], player_count: int, variant: str):
        if player_count <= 1:
            raise ValueError(f'Must have at least two players (found {player_count})')

        unique_symbols = set(player_symbols)
        if len(unique_symbols) != len(player_symbols):
            raise ValueError(f'Player symbols must be unique (was {player_symbols}')
        if len(player_symbols) != player_count:
            raise ValueError(f'Player symbols must be exactly {player_count} (was {player_symbols})')

        self._field = Field(grid_size)
        self._player_count = player_count
        self._player_to_symbol: dict[PlayerId, Symbol] = {k: symbol for k, symbol in enumerate(player_symbols, start=1)}
        self._symbol_to_player: dict[Symbol, PlayerId] = {symbol: k for k, symbol in self._player_to_symbol.items()}
        self._current_player: PlayerId = 1
        self._win_conditions = self._get_win_conditions(variant)

    def _get_win_conditions(self, variant: str) -> WinConditions:
        match variant:
            case "tictactoe":
                return TicTacToeWinConditions()
            case "notakto":
                return NotaktoWinConditions()
            case "wild":
                return WildTicTacToeWinConditions()
            case "pick15":
                return Pick15WinConditions()
            case _:
                raise ValueError(f'Unknown variant: {variant}')

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
    def player_count(self):
        return self._player_count

    @property
    def next_player(self) -> PlayerId:
        return self.current_player + 1 if self.current_player != self.player_count else 1

    @property
    def winner(self) -> PlayerId | None:
        return self._win_conditions.winner(self._field, self._symbol_to_player)

    def get_symbol_choices(self, player: PlayerId) -> list[Symbol]:
        return self._win_conditions.get_valid_symbols(player, self._player_to_symbol)

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



