class Bot(object):
    def __init__(self):
        pass

    #
    def sort_cells_by_pressure(self, ):
        # TOOD:
        return []

    def get_move_for_turn(self, turn_num, reinforcement_count, world):
        move = Move([], [])

        all_my_cells = list(world.get_my_cells())

        for _ in range(reinforcement_count):
            cell = random.choice(all_my_cells)
            world.add_reinforcement(move, cell, 1)

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