from warhead.protocol.ttypes import Move


class Bot(object):
    def __init__(self):
        pass

    checked_pressure = {}

    # Retruns the average number of enemy solder
    # that might attack a cell
    def calc_cell_pressure(self, world, cell):
        if cell in self.checked_pressure:
            return self.checked_pressure[cell]

        adj =  world.get_adj_cells(cell)

        if(adj == 0)
            self.checked_pressure[cell] = 0
            return 0

        adj_armies = sum([cell.armySize for cell in adj])
        self.checked_pressure[cell] = adj_armies / len(adj_armies)

        return self.checked_pressure[cell]

    #
    def sort_cells_by_pressure(self, world, cells = []):
        return cells.sort(key=(lambda x: self.calc_cell_pressure(world,x)))

    def get_move_for_turn(self, turn_num, reinforcement_count, world):
        # REset pressure
        checked_pressure = {}

        move = Move([], [])

        all_my_cells = list(world.get_my_cells())

        for _ in range(reinforcement_count):
            cell = random.choice(all_my_cells)
            world.add_reinforcement(move, cell, 1)

        all_my_adj_cells = self.sort_cells_by_pressure(wold,cell)

        for cell in all_my_cells:
            all_my_adj_cells = world.get_adj_cells(cell)
            if len(all_my_adj_cells) == 0:
                continue

            cell_army_num = cell.armySize

            all_sets_of_attacks = get_k_subsets(cell_army_num, len(all_my_adj_cells) + 1)
            attack_vector = random.choice(all_sets_of_attacks)

            for i in range(len(all_my_adj_cells)):
                adj = all_my_adj_cells[i]
                attack_size = attack_vector[i]
                world.add_action(move, cell, adj, attack_size)

        return move