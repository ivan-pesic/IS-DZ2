import copy


class Algorithm:
    def get_algorithm_steps(self, tiles, variables, words):
        pass


class Field:
    def __init__(self, field, orientation, x, y, length, position):
        self.field = field
        self.x = x
        self.y = y
        self.orientation = orientation
        self.length = length
        self.position = position

    def __str__(self):
        details = ''
        details += f'Position    : {self.position}\n'
        details += f'Field       : {self.field}\n'
        details += f'X coordinate: {self.x}\n'
        details += f'Y coordinate: {self.y}\n'
        details += f'Orientation : {self.orientation}\n'
        details += f'Length      : {self.length}\n'
        return details


class ExampleAlgorithm(Algorithm):
    def get_algorithm_steps(self, tiles, variables, words):
        moves_list = [['0h', 0], ['0v', 2], ['1v', 1], ['2h', 1], ['4h', None],
                      ['2h', None], ['1v', None], [
                          '0v', 3], ['1v', 1], ['2h', 1],
                      ['4h', 4], ['5v', 5]]

        domains = {var: [word for word in words] for var in variables}
        solution = []
        for move in moves_list:
            solution.append([move[0], move[1], domains])

        return solution


def update_domains(domains, variables):
    for var in variables:
        length = variables[var]
        domains[var] = [item for item in domains[var] if len(item) == length]


def is_consistent_assignment(field, word, matrix):
    for idx, letter in enumerate(word):
        if field.orientation == 'h':
            if matrix[field.x][field.y + idx] != 0 and matrix[field.x][field.y + idx] != letter:
                return False
        else:
            if matrix[field.x + idx][field.y] != 0 and matrix[field.x + idx][field.y] != letter:
                return False
    return True


def update_matrix(matrix, field, word):
    if field.orientation == 'h':
        for idx, letter in enumerate(word):
            matrix[field.x][field.y + idx] = letter
    else:
        for idx, letter in enumerate(word):
            matrix[field.x + idx][field.y] = letter


def backtrack(vars, domains, solution, lvl, matrix, fields):
    if lvl == len(vars):
        return True
    position = vars[lvl]
    field = fields[position]
    for idx, word in enumerate(domains[position]):
        if is_consistent_assignment(field, word, matrix):
            new_matrix = copy.deepcopy(matrix)
            update_matrix(new_matrix, field, word)
            solution.append([position, idx, domains])
            new_dom = copy.deepcopy(domains)
            if backtrack(vars, new_dom, solution, lvl+1, new_matrix, fields):
                return True
    solution.append([position, None, domains])
    return False


def get_all_arcs(graph):
    return [[key, x] for key in graph for x in graph[key]]


def get_intersection(pos1, pos2):
    if pos1.orientation == 'h':
        return pos2.y - pos1.y, pos1.x - pos2.x
    else:
        return pos2.x - pos1.x, pos1.y - pos2.y


def intersection_is_same_letter(word1, word2, pos1, pos2):
    idx1, idx2 = get_intersection(pos1, pos2)
    return word1[idx1] == word2[idx2]


def satisfies_constraint(val_x, val_y, x, y, matrix, fields):
    return is_consistent_assignment(fields[x], val_x, matrix) and is_consistent_assignment(fields[y], val_y, matrix) and intersection_is_same_letter(val_x, val_y, fields[x], fields[y])


def are_constrained(p1, p2, fields):
    return are_adjacent(fields[p1], fields[p2])


def arc_consistency(vars, domains, matrix, fields, graph):
    arc_list = get_all_arcs(graph)
    while arc_list:
        x, y = arc_list.pop(0)
        x_vals_to_del = []
        for val_x in domains[x]:
            y_no_val = True
            for val_y in domains[y]:
                if satisfies_constraint(val_x, val_y, x, y, matrix, fields):
                    y_no_val = False
                    break
            if y_no_val:
                x_vals_to_del.append(val_x)
        if x_vals_to_del:
            domains[x] = [v for v in domains[x] if v not in x_vals_to_del]
            if not domains[x]:
                return False
            for v in vars:
                if v != x and are_constrained(v, x, fields):
                    arc_list.append((v, x))
    return True


def backtrack_fc_ac(vars, domains, solution, lvl, matrix, fields, graph):
    if lvl == len(vars):
        return True
    position = vars[lvl]
    field = fields[position]
    for idx, word in enumerate(domains[position]):
        is_consistent = True
        if is_consistent_assignment(field, word, matrix):
            new_matrix = copy.deepcopy(matrix)
            update_matrix(new_matrix, field, word)
            new_dom = copy.deepcopy(domains)
            new_dom[position] = [word]
            for constraint_position in new_dom:
                if constraint_position == position:
                    continue
                new_list = [item for item in new_dom[constraint_position] if is_consistent_assignment(
                    fields[constraint_position], item, new_matrix)]
                new_dom[constraint_position] = new_list
                if len(new_list) == 0:
                    is_consistent = False
                    break
            if not is_consistent:
                solution.append([position, 0, new_dom])
                continue
            if not arc_consistency(vars, new_dom, matrix, fields, graph):
                solution.append([position, None, domains])
                continue

            solution.append([position, 0, new_dom])
            if backtrack_fc(vars, new_dom, solution, lvl+1, new_matrix, fields):
                return True
    solution.append([position, None, domains])
    return False


def backtrack_fc_ac_2(vars, domains, solution, lvl, matrix, fields, graph):
    if lvl == len(vars):
        return True
    position = vars[lvl]
    field = fields[position]
    for idx, word in enumerate(domains[position]):
        is_consistent = True
        if is_consistent_assignment(field, word, matrix):
            solution.append([position, idx, domains])
            new_matrix = copy.deepcopy(matrix)
            update_matrix(new_matrix, field, word)
            new_dom = copy.deepcopy(domains)
            new_dom[position] = [word]
            for var in vars:
                if var != position and are_adjacent(fields[var], fields[position]):
                    new_list = [item for item in new_dom[var] if is_consistent_assignment(
                        fields[var], item, new_matrix)]
                    new_dom[var] = new_list
                    if len(new_list) == 0:
                        is_consistent = False
                        break
            if not is_consistent:
                continue
            if not arc_consistency(vars, new_dom, matrix, fields, graph):
                continue
            if backtrack_fc_2(vars, new_dom, solution, lvl+1, new_matrix, fields):
                return True
    solution.append([position, None, domains])
    return False


def backtrack_ac(vars, domains, solution, lvl, matrix, fields, graph):
    if lvl == len(vars):
        return True
    position = vars[lvl]
    field = fields[position]
    for idx, word in enumerate(domains[position]):
        if is_consistent_assignment(field, word, matrix):
            new_matrix = copy.deepcopy(matrix)
            update_matrix(new_matrix, field, word)
            solution.append([position, idx, domains])
            new_dom = copy.deepcopy(domains)
            if not arc_consistency(vars, new_dom, matrix, fields, graph):
                solution.append([position, None, domains])
                continue
            if backtrack_ac(vars, new_dom, solution, lvl+1, new_matrix, fields, graph):
                return True
    solution.append([position, None, domains])
    return False


def backtrack_fc(vars, domains, solution, lvl, matrix, fields):
    if lvl == len(vars):
        return True
    position = vars[lvl]
    field = fields[position]
    for idx, word in enumerate(domains[position]):
        is_consistent = True
        if is_consistent_assignment(field, word, matrix):
            new_matrix = copy.deepcopy(matrix)
            update_matrix(new_matrix, field, word)
            new_dom = copy.deepcopy(domains)
            new_dom[position] = [word]
            for constraint_position in new_dom:
                if constraint_position == position:
                    continue
                new_list = [item for item in new_dom[constraint_position] if is_consistent_assignment(
                    fields[constraint_position], item, new_matrix)]
                new_dom[constraint_position] = new_list
                if len(new_list) == 0:
                    is_consistent = False
                    break
            if not is_consistent:
                solution.append([position, 0, new_dom])
                continue

            solution.append([position, 0, new_dom])
            if backtrack_fc(vars, new_dom, solution, lvl+1, new_matrix, fields):
                return True
    solution.append([position, None, domains])
    return False


def update_domain(domain, position, word, matrix):
    pass


def backtrack_fc_2(vars, domains, solution, lvl, matrix, fields):
    if lvl == len(vars):
        return True
    position = vars[lvl]
    field = fields[position]
    for idx, word in enumerate(domains[position]):
        is_consistent = True
        if is_consistent_assignment(field, word, matrix):
            solution.append([position, idx, domains])
            new_matrix = copy.deepcopy(matrix)
            update_matrix(new_matrix, field, word)
            new_dom = copy.deepcopy(domains)
            new_dom[position] = [word]
            for var in vars:
                if var != position and are_adjacent(fields[var], fields[position]):
                    new_list = [item for item in new_dom[var] if is_consistent_assignment(
                        fields[var], item, new_matrix)]
                    new_dom[var] = new_list
                    if len(new_list) == 0:
                        is_consistent = False
                        break
            if not is_consistent:
                continue
            if backtrack_fc_2(vars, new_dom, solution, lvl+1, new_matrix, fields):
                return True
    solution.append([position, None, domains])
    return False


def get_fields(variables, tiles):
    vars = copy.deepcopy(variables)
    for var in variables:
        field_num = int(var[:-1])
        orientation = var[-1]
        x, y = int(field_num / len(tiles[0])), int(field_num % len(tiles[0]))
        vars[var] = Field(field_num, orientation, x, y, variables[var], var)
    return vars


class Backtracking(Algorithm):
    def get_algorithm_steps(self, tiles, variables, words):
        matrix = [[0 for i in range(len(tiles[0]))] for i in range(len(tiles))]
        solution = []
        vars = [var for var in variables]
        domains = {var: [word for word in words] for var in variables}
        update_domains(domains, variables)
        fields = get_fields(variables, tiles)
        backtrack(vars, domains, solution, 0, matrix, fields)
        return solution


class ForwardChecking(Algorithm):
    def get_algorithm_steps(self, tiles, variables, words):
        matrix = [[0 for i in range(len(tiles[0]))] for i in range(len(tiles))]
        solution = []
        vars = [var for var in variables]
        domains = {var: [word for word in words] for var in variables}
        update_domains(domains, variables)
        fields = get_fields(variables, tiles)
        backtrack_fc_2(vars, domains, solution, 0, matrix, fields)
        return solution


def are_adjacent(field1, field2):
    if field1.orientation == field2.orientation:
        return False

    x1, y1 = field1.x, field1.y
    x2, y2 = field2.x, field2.y
    # print(f"{x1},{y1}: {field1.position}; {x2},{y2}: {field2.position}")

    if field1.orientation == 'v':
        return (x1 <= x2 < x1 + field1.length) and (y2 <= y1 < y2 + field2.length)
    elif field1.orientation == 'h':
        return (x2 <= x1 < x2 + field2.length) and (y1 <= y2 < y1 + field1.length)


def create_graph(fields):
    return {field: [second_field for second_field in fields if second_field != field and are_adjacent(fields[field], fields[second_field])] for field in fields}


class ArcConsistency(Algorithm):
    def get_algorithm_steps(self, tiles, variables, words):
        matrix = [[0 for i in range(len(tiles[0]))] for i in range(len(tiles))]
        solution = []
        vars = [var for var in variables]
        domains = {var: [word for word in words] for var in variables}
        update_domains(domains, variables)
        fields = get_fields(variables, tiles)
        # print(fields)
        graph = create_graph(fields)
        # print(get_all_arcs(graph))
        arc_consistency(vars, domains, matrix, fields, graph)
        backtrack_fc_ac_2(vars, domains, solution, 0, matrix, fields, graph)
        return solution
