from warhead.protocol.ttypes import *
import math

_direction_to_vector = {
    Direction.UP: (0, -1),
    Direction.RIGHT: (1, 0),
    Direction.DOWN: (0, 1),
    Direction.LEFT: (-1, 0)
}

def direction_to_vector(direction):
    """Converts a direction to an int tuple ``(x, y)``

    :param direction: Direction
    :type direction: Direction
    :returns: A tuple with ``(x, y)`` coordinates
    :rtype: tuple(int, int)
    :raises: KeyError
    """
    return _direction_to_vector[direction]

def direction_from_vector(dx, dy):
    """Converts a vector to a direction, if appropriate

    :param dx: X component (``-1``, ``0`` or ``1``)
    :type dx: int
    :param dy: X component (``-1``, ``0`` or ``1``)
    :type dy: int
    :returns: Corresponding direction, or ``None``
    :rtype: Direction
    :raises: KeyError
    """
    if dy == 0:
        if dx == -1:
            return Direction.LEFT
        elif dx == 1:
            return Direction.RIGHT
    if dx == 0:
        if dy == -1:
            return Direction.UP
        elif dy == 1:
            return Direction.DOWN
    return KeyError(str((dx, dy)) + ' does not have an equivalent Direction')

class World:
    def __init__(self, board, team):
        """Constructor. Bots do not need to invoke this, as they take a World
        instance as argument.
        
        :param board: Two-dimensional array of cells.
        :param team: Bot's team property
        """
        self.board = board
        self.team = team
        self.size = (len(self.board), len(self.board[0]))

    def get_my_team(self):
        """Obtain the Bot's team property.
        Useful for interpreting ownership of cells, as outlined in the following
        code snippet.

        ::

            cell = ...;
            if cell.team == world.get_my_team():
                pass # cell belongs to me
            elif cell.team is None:
                pass # cell is unoccupied
            else:
                pass # cell belongs to enemy

        :returns: The Bot's team property.
        :rtype: Team
        """
        return self.team

    def get_size(self):
        """Obtain the dimensioins of the game board. In this contest, this value
        is assured to be constant, i.e. same as::

            return (6, 6)

        :returns: Dimensions of the game board as a tuple.
        :rtype: tuple(int, int)
        """
        return self.size

    def get_all_cells(self):
        """Obtain a list of all cells (tiles) on the board. Note that this
        includes cells with ``OBSTACLE`` terrain.
        
        :returns: List of all cells on the board.
        :rtype: list(Cell)
        """
        for x, column in enumerate(self.board):
            for y, cell in enumerate(column):
                yield cell

    def get_my_cells(self):
        """Obtain a list of cells occupied by the Bot.  The Bot may assume that
        the returned list is non-empty.
        
        :returns: List of cells occupied by the Bot.
        :rtype: list(Cell)
        """
        for cell in self.get_all_cells():
            if cell.team == self.team:
                yield cell

    def get_cell_if_valid(self, x, y):
        """Obtain a reference to a ``Cell`` based on its location on the board.
        The cell is "valid" if ``(x, y)`` points to a location inside the board,
        and the cell at that location does not have ``OBSTACLE`` terrain.
        
        :param x: x-coordinate of specified location
        :type x: int
        :param y: y-coordinate of specified location
        :type y: int
        :returns: The cell at the specified location, or ``None`` if such ``Cell`` is not valid
        :rtype: Cell or None
        """
        if 0 <= x < self.size[0] and 0 <= y < self.size[1]:
            cell = self.board[x][y]
            if cell.terrain != Terrain.OBSTACLE:
                return cell

        return None

    def get_adj_cells(self, cell):
        """Obtain a list of cells that are adjacent to the specified cell.
        
        This function can be effectively used to traverse the board as a
        bidirectional graph. The function is useful in combination with
        add_action::

            for adj in world.get_adj_cells(cell):
                # Suppose we decided to move units from cell to adj
                unitsToMove = ...
                world.add_action(move, cell, adj, unitsToMove)

        The caller may assume the returned list is non-empty, as the valid tiles
        on the board are always connected.
        
        :param cell: the specified cell
        :returns: A list of cells that are adjacent to argument cell and are
                  valid.
        :rtype: list(Cell)
        """
        result = []
        for dx, dy in _direction_to_vector.values():
            x = cell.x + dx
            y = cell.y + dy
            adj = self.get_cell_if_valid(x, y)
            if adj is not None:
                result.append(adj)
        return result

    def add_reinforcement(self, move, cell, armySize):
        """Adds a reinforcement command to the list of commands issued this
        turn, given a cell and the amount of units requested.
        
        Accounts for this many units being added to the cell, so its armySize
        will reflect the updated amount that may still move away from it in this
        turn, assuming the command is legal.
        
        :param move: The bot's move for this turn.
        :type move: Move
        :param cell: Argument cell to reinforce
        :type cell: Cell
        :param armySize: Amount of units requested
        :type armySize: int
        """
        r = Reinforcement()
        r.x = cell.x
        r.y = cell.y
        r.armySize = armySize
        cell.armySize += armySize
        move.reinforcements.append(r)

    def add_action(self, move, src, dst, armySize):
        """Adds an action (movement) command to the list of commands issued this
        turn, given a source cell, destination cell and an amount of units to
        move.
        
        Accounts for this many units moving away from the source cell, so its
        ``armySize`` will reflect the amount that may still move out of it in
        this turn.

        :param move: The bot's move for this turn.
        :type move: Move
        :param src: Source cell.
        :type src: Cell
        :param dst: Destination cell.
        :type dst: Cell
        :raises: KeyError if src and dst are not adjacent cells.
        """
        a = Action()
        a.x = src.x
        a.y = src.y
        a.armySize = armySize
        a.direction = direction_from_vector(dst.x - src.x, dst.y - src.y)
        src.armySize -= armySize
        move.actions.append(a)

    def simulate_combat_at_cell(self, cell, my_army_size, enemy_army_size):
        """Simulates combat in a tile given its current ownership.
        The outcome of the simulation is an integer, with the following
        semantics:
        
        - ``x`` (given some ``x > 0``) if Bot would win with ``x`` units
          remaining
        - ``0`` if both sides would lose all units
        - ``-x`` (given some ``x > 0``) if enemy would win with ``x`` units
          remaining

        :param cell: The cell to consider combat in.
        :type cell: Cell
        :param my_army_size: Bot's unit count in the cell (prior to combat)
        :type my_army_size: int
        :param enemy_army_size: Enemy's unit count in the cell (prior to combat)
        :type enemy_army_size: int
        :returns: outcome, as specified in description.
        :rtype: int
        """
        my_def = False
        enemy_def = False
        if cell.team == self.team:
            my_def = True
        elif cell.team is not None:
            enemy_def = True

        return simulate_combat_on_terrain(cell.terrain, my_def, enemy_def, my_army_size, enemy_army_size)

def _fight_logic(sizes, effectiveness):
    if sizes[0] > 0 and sizes[1] > 0:
        str = [float(sizes[i] * effectiveness[i]) for i in xrange(2)]

        ttl = [sizes[i] / str[1-i] for i in xrange(2)]

        t = min(ttl)
        rem = [int(math.floor(sizes[i] - str[1-i] * t)) for i in xrange(2)]
    else:
        rem = sizes

    if rem[0] <= 0 and rem[1] <= 0:
        return None, 0

    if rem[0] <= 0:
        return 1, rem[1]
    else:
        return 0, rem[0]

def get_combat_effectiveness(is_defender, terrain):
    """Gets the combat effectiveness rating per unit (as described by game
    rules) given the terrain type and whether or not they are defending.
    
    :param is_defender: Whether units are defending.
    :type is_defender: bool
    :param terrain: ``Terrain`` the combat takes place on.
    :type terrain: Terrain
    :return: Combat effectiveness rating.
    :rtype: int
    """
    if is_defender:
        eff_by_terrain = {
            Terrain.NORMAL: 5,
            Terrain.DEF_ADV: 6,
            Terrain.ATT_ADV: 4,
            Terrain.OBSTACLE: 1 # Impossible to fight in, but let's not crash bot for running this
        }
    else:
        eff_by_terrain = {
            Terrain.NORMAL: 4,
            Terrain.DEF_ADV: 3,
            Terrain.ATT_ADV: 5,
            Terrain.OBSTACLE: 1 # Impossible to fight in, but let's not crash bot for running this
        }
    return eff_by_terrain.get(terrain)

def simulate_combat_on_terrain(terrain, my_def, enemy_def, my_army_size, enemy_army_size):
    """Simulates combat on a given terrain type. Caller must specify which side
    (if any) is defending.
    
    Outcome is returned with the same semantics as ``simulate_combat_at_cell``.
    
    :param terrain: ``Terrain`` to simulate combat on
    :type terrain: Terrain
    :param my_def: ``True`` if Bot is defending
    :type my_def: bool
    :param enemy_def: ``True`` if enemy is defending
    :type enemy_def: bool
    :param my_army_size: Bot's unit count participating in combat
    :type my_army_size: int
    :param enemy_army_size: Enemy unit count participating in combat
    :type enemy_army_size: int
    :return: Outcome, as specified in description.
    :rtype: int
    """
    my_eff = get_combat_effectiveness(my_def, terrain)
    enemy_eff = get_combat_effectiveness(enemy_def, terrain)

    return get_combat_outcome(my_army_size, enemy_army_size, my_eff, enemy_eff)

def get_combat_outcome(n0, n1, e0, e1):
    """Core algorithm used to determine combat outcome given the amount of units
    and the effectiveness per unit of each side Outcome has the same semantics
    as explained in ``simulate_combat_at_cell``.
    
    :param n0: Number of units on Bot's side.
    :type n0: int
    :param n1: Number of units on enemy's side.
    :type n1: int
    :param e0: Combat effectiveness on Bot's side.
    :type e0: int
    :param e1: Combat effectiveness on enemy's side.
    :type e1: int
    :return: Outcome, as specified in description.
    :rtype: int
    """
    sizes = (n0, n1)
    eff = (e0, e1)

    winner, remaining_units = _fight_logic(sizes, eff)

    if winner == 0:
        return remaining_units
    elif winner == 1:
        return -remaining_units
    else:
        return 0
