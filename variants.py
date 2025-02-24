from abc import ABC, abstractmethod

from project_types import Symbol, Cell, Feedback, Field
class SymbolPlacer(ABC):
    @abstractmethod
    def place_symbol(self, symbol: Symbol, cell:Cell, is_game_over: bool, get_symbol_choices: list[Symbol], field: Field) -> Feedback:




class TicTacToeSymbolPlacer(SymbolPlacer):
    def place_symbol(self, symbol: Symbol, cell:Cell, is_game_over: bool, get_symbol_choices: list[Symbol], field: Field) -> Feedback:
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

