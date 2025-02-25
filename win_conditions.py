class WinCondition(ABC):
    @abstractmethod
    def check_winner(self, field: Field) -> PlayerId | None:



class TicTacToeWinCondition(WinCondition):
    def check_winner(self, field: Field) -> PlayerId | None:
        row_groups = [[Cell(row, k) for k in field.valid_coords] for row in field.valid_coords]
        col_groups = [[Cell(k, col) for k in field.valid_coords] for col in field.valid_coords]
        diagonals = [[Cell(k, k) for k in field.valid_coords], [Cell(k, field.grid_size - k + 1) for k in field.valid_coords]]

        for groups in [row_groups, col_groups, diagonals]:
            for group in groups:
                if (basis := field.get_symbol_at(group[0])) is not None and field.are_all_equal_to_basis(basis, group):
                    return basis  
        return None



class WildTicTacToeWinCondition(WinCondition):
    def check_winner(self, field: Field) -> PlayerId | None:
        def check_winner(self, field: Field) -> PlayerId | None:
        row_groups = [[Cell(row, k) for k in field.valid_coords] for row in field.valid_coords]
        col_groups = [[Cell(k, col) for k in field.valid_coords] for col in field.valid_coords]
        diagonals = [[Cell(k, k) for k in field.valid_coords], 
                    [Cell(k, field.grid_size - k + 1) 
                    for k in field.valid_coords]]

        for groups in [row_groups, col_groups, diagonals]:
            for group in groups:
                if (basis := self._field.get_symbol_at(group[0])) is not None and \
                        self._field.are_all_equal_to_basis(basis, group):
                    winner = self._symbol_to_player.get(basis)
                    assert winner is not None, \
                        f'Winning symbol {basis} in cell group {groups} has no associated player'

                    return winner

        return None


class WildTicTacToeWinCondition(WinCondition):
    def check_winner(self, field: Field) -> PlayerId | None:
        def check_winner(self, field: Field) -> PlayerId | None:
        row_groups = [[Cell(row, k) for k in field.valid_coords] for row in field.valid_coords]
        col_groups = [[Cell(k, col) for k in field.valid_coords] for col in field.valid_coords]
        diagonals = [[Cell(k, k) for k in field.valid_coords], 
                    [Cell(k, field.grid_size - k + 1) 
                    for k in field.valid_coords]]

        for groups in [row_groups, col_groups, diagonals]:
            for group in groups:
                if (basis := field.get_symbol_at(group[0])) is not None and field.are_all_equal_to_basis(basis, group):
                    return basis  
        return None
