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
        backtrack_fc(vars, domains, solution, 0, matrix, fields)
        return solution


class ArcConsistency(Algorithm):
    def get_algorithm_steps(self, tiles, variables, words):
        pass
