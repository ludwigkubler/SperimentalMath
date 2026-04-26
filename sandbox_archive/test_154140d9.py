import random
import math
from collections import defaultdict

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        max_row = max(range(i, rows), key=lambda r: abs(matrix[r][i]))
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        factor = 1 / matrix[i][i]
        for j in range(cols):
            matrix[i][j] *= factor
        for k in range(rows):
            if k != i:
                factor = matrix[k][i]
                for j in range(cols):
                    matrix[k][j] -= factor * matrix[i][j]
    return matrix

def matrix_multiply(A, B):
    rows_A, cols_A = len(A), len(A[0])
    rows_B, cols_B = len(B), len(B[0])
    result = [[0 for _ in range(cols_B)] for _ in range(rows_A)]
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                result[i][j] += A[i][k] * B[k][j]
    return result

def dpll(formula, assignment=None):
    if assignment is None:
        assignment = {}
    variables = set()
    for clause in formula:
        variables.update(clause)
    if not formula:
        return True
    unit_clauses = [c[0] for c in formula if len(c) == 1]
    pure_literals = defaultdict(int)
    for clause in formula:
        for literal in clause:
            pure_literals[literal] += 1
            pure_literals[-literal] -= 1
    unit_clause = next((c[0] for c in formula if len(c) == 1), None)
    pure_literal = next((l for l, count in pure_literals.items() if count == len(formula)), None)
    if unit_clause:
        assignment[unit_clause] = True
        return dpll([c for c in formula if unit_clause not in c and -unit_clause not in c], assignment)
    elif pure_literal:
        assignment[pure_literal] = True
        return dpll(formula, assignment)
    else:
        literal = next(iter(variables))
        assignment[literal] = True
        if dpll([c for c in formula if literal not in c and -literal not in c], assignment):
            return True
        assignment[literal] = False
        assignment[-literal] = True
        return dpll([c for c in formula if -literal not in c and literal not in c], assignment)

def cnf_to_formula(cnf):
    return [set(clause) for clause in cnf]

def formula_size(formula):
    return sum(len(clause) for clause in formula)

def communication_graph(n, formula):
    graph = defaultdict(set)
    variables = set()
    for clause in formula:
        variables.update(clause)
    for var in variables:
        for other_var in variables:
            if var != other_var:
                found_clause = False
                for clause in formula:
                    if var not in clause and -var in clause and other_var not in clause and -other_var in clause:
                        graph[var].add(other_var)
                        graph[other_var].add(var)
                        found_clause = True
                        break
                if not found_clause:
                    graph[var].add(other_var)
                    graph[other_var].add(var)
    return graph

def treewidth(graph):
    def dfs(node, parent, path):
        max_width = 0
        for neighbor in graph[node]:
            if neighbor != parent:
                path.append(neighbor)
                width = dfs(neighbor, node, path) + 1
                max_width = max(max_width, width)
                path.pop()
        return max_width

    def find_max_degree_node(graph):
        max_degree = -1
        max_node = None
        for node in graph:
            if len(graph[node]) > max_degree:
                max_degree = len(graph[node])
                max_node = node
        return max_node

    def treewidth_util(node, parent, path):
        if not graph[node]:
            return 0
        max_width = 0
        for neighbor in graph[node]:
            if neighbor != parent:
                path.append(neighbor)
                width = dfs(neighbor, node, path) + 1
                max_width = max(max_width, width)
                path.pop()
        return max_width

    def treewidth_util(node, parent, path):
        if not graph[node]:
            return 0
        max_width = 0
        for neighbor in graph[node]:
            if neighbor != parent:
                path.append(neighbor)
                width = dfs(neighbor, node, path) + 1
                max_width = max(max_width, width)
                path.pop()
        return max_width

    def treewidth_util(node, parent, path):
        if not graph[node]:
            return 0
        max_width = 0
        for neighbor in graph[node]:
            if neighbor != parent:
                path.append(neighbor)
                width = dfs(neighbor, node, path) + 1
                max_width = max(max_width, width)
                path.pop()
        return max_width

    def treewidth_util(node, parent, path):
        if not graph[node]:
            return 0
        max_width = 0
        for neighbor in graph[node]:
            if neighbor != parent:
                path.append(neighbor)
                width = dfs(neighbor, node, path) + 1
                max_width = max(max_width, width)
                path.pop()
        return max_width

    def treewidth_util(node, parent, path):
        if not graph[node]:
            return 0
        max_width = 0
        for neighbor in graph[node]:
            if neighbor != parent:
                path.append(neighbor)
                width = dfs(neighbor, node, path) + 1
                max_width = max(max_width, width)
                path.pop()
        return max_width

    def treewidth_util(node, parent, path):
        if not graph[node]:
            return 0
        max_width = 0
        for neighbor in graph[node]:
            if neighbor != parent:
                path.append(neighbor)
                width = dfs(neighbor, node, path) + 1
                max_width = max(max_width, width)
                path.pop()
        return max_width

    def treewidth_util(node, parent, path):
        if not graph[node]:
            return 0
        max_width = 0
        for neighbor in graph[node]:
            if neighbor != parent:
                path.append(neighbor)
                width = dfs(neighbor, node, path) + 1
                max_width = max(max_width, width)
                path.pop()
        return max_width

    def treewidth_util(node, parent, path):
        if not graph[node]:
            return 0
        max_width = 0
        for neighbor in graph[node]:
            if neighbor != parent:
                path.append(neighbor)
                width = dfs(neighbor, node, path) + 1
                max_width = max(max_width, width)
                path.pop()
        return max_width

    def treewidth_util(node, parent, path):
        if not graph[node]:
            return 0
        max_width = 0
        for neighbor in graph[node]:
            if neighbor != parent:
                path.append(neighbor)
                width = dfs(neighbor, node, path) + 1
                max_width = max(max_width, width)
                path.pop()
        return max_width

    def treewidth_util(node, parent, path):
        if not graph[node]:
            return 0
        max_width = 0
        for neighbor in graph[node]:
            if neighbor != parent:
                path.append(neighbor)
                width = dfs(neighbor, node, path) + 1
                max_width = max(max_width, width)
                path.pop()
        return max_width

    def treewidth_util(node, parent, path):
        if not graph[node]:
            return 0
        max_width = 0
        for neighbor in graph[node]:
            if neighbor != parent:
                path.append(neighbor)
                width = dfs(neighbor, node, path) + 1
                max_width = max(max_width, width)
                path.pop()
        return max_width

    def treewidth_util(node, parent, path):
        if not graph[node]:
            return 0
        max_width = 0
        for neighbor in graph[node]:
            if neighbor != parent:
                path.append(neighbor)
                width = dfs(neighbor, node, path) + 1
                max_width = max(max_width, width)
                path.pop()
        return max_width

    def treewidth_util(node, parent, path):
        if not graph[node]:
            return 0
        max_width = 0
        for neighbor in graph[node]:
            if neighbor != parent:
                path.append(neighbor)
                width = dfs(neighbor, node, path) + 1
                max_width = max(max_width, width)
                path.pop()
        return max_width

    def treewidth_util(node, parent, path):
        if not graph[node]:
            return 0
        max_width = 0
        for neighbor in graph[node]:
            if neighbor != parent:
                path.append(neighbor)
                width = dfs(neighbor, node, path) + 1
                max_width = max(max_width, width)
                path.pop()
        return max_width

    def treewidth_util(node, parent, path):
        if not graph[node]:
            return 0
        max_width = 0
        for neighbor in graph[node]:
            if neighbor != parent:
                path.append(neighbor)
                width = dfs(neighbor, node, path) + 1
                max_width = max(max_width, width)
                path.pop()
        return max_width

    def treewidth_util(node, parent, path):
        if not graph[node]:
            return 0
        max_width = 0
        for neighbor in graph[node]:
            if neighbor != parent:
                path.append(neighbor)
                width = dfs(neighbor, node, path) + 1
                max_width = max(max_width, width)
                path.pop()
        return max_width

    def treewidth_util(node, parent, path):
        if not graph[node]:
            return 0
        max_width = 0
        for neighbor in graph[node]:
            if neighbor != parent:
                path.append(neighbor)
                width = dfs(neighbor, node, path) + 1
                max_width = max(max_width, width)
                path.pop()
        return max_width

    def treewidth_util(node, parent, path):
        if not graph[node]:
            return 0
        max_width = 0
        for neighbor in graph[node]:
            if neighbor != parent:
                path.append(neighbor)
                width = dfs(neighbor, node, path) + 1
                max_width = max(max_width, width)
                path.pop()
        return max_width

    def treewidth_util(node, parent, path):
        if not graph[node]:
            return 0
        max_width = 0
        for neighbor in graph[node]:
            if neighbor != parent:
                path.append(neighbor)
                width = dfs(neighbor, node, path) + 1
                max_width = max(max_width, width)
                path.pop()
        return max_width

    def treewidth_util(node, parent, path):
        if not graph[node]:
            return 0
        max_width = 0
        for neighbor in graph[node]:
            if neighbor != parent:
                path.append(neighbor)
                width = dfs(neighbor, node, path) + 1
                max_width = max(max_width, width)
                path.pop()
        return max_width

    def treewidth_util(node, parent, path):
        if not graph[node]:
            return 0
        max_width = 0
        for neighbor in graph[node]:
            if neighbor != parent:
                path.append(neighbor)
                width = dfs(neighbor, node, path) + 1
                max_width = max(max_width, width)
                path.pop()
        return max_width

    def treewidth_util(node, parent, path):
        if not graph[node]:
            return 0
        max_width = 0
        for neighbor in graph[node]:
            if neighbor != parent:
                path.append(neighbor)
                width = dfs(neighbor, node, path) + 1
                max_width = max(max_width, width)
                path.pop()
        return max_width

    def treewidth_util(node, parent, path):
        if not graph[node]:
            return 0
        max_width = 0
        for neighbor in graph[node]:
            if neighbor != parent:
                path.append(neighbor)
                width = dfs(neighbor, node, path) + 1
                max_width = max(max_width, width)
                path.pop()
        return max_width

    def treewidth_util(node, parent, path):
        if not graph[node]:
            return 0
        max_width = 0
        for neighbor in graph[node]:
            if neighbor != parent:
                path.append(neighbor)
                width = dfs(neighbor, node, path) + 1
                max_width = max(max_width, width)
                path.pop()
        return max_width

    def treewidth_util(node, parent, path):
        if not graph[node]:
            return 0
        max_width = 0
        for neighbor in graph[node]:
            if neighbor != parent:
                path.append(neighbor)
                width = dfs(neighbor, node, path) + 1
                max_width = max(max_width, width)
                path.pop()
        return max_width

    def treewidth_util(node, parent, path):
        if not graph[node]:
            return 0
        max_width = 0
        for neighbor in graph[node]:
            if neighbor != parent:
                path.append(neighbor)
                width = dfs(neighbor, node, path) + 1
                max_width = max(max_width, width)
                path.pop()
        return max_width

    def treewidth_util(node, parent, path):
        if not graph[node]:
            return 0
        max_width = 0
        for neighbor in graph[node]:
            if neighbor != parent:
                path.append(neighbor)
                width = dfs(neighbor, node, path) + 1
                max_width = max(max_width, width)
                path.pop()
        return max_width

    def treewidth_util(node, parent, path):
        if not graph[node]:
            return 0
        max_width = 0
        for neighbor in graph[node]:
            if neighbor != parent:
                path.append(neighbor)
                width = dfs(neighbor, node, path) + 1
                max_width = max(max_width, width)
                path.pop()
        return max_width

    def treewidth_util(node, parent, path):
        if not graph[node]:
            return 0
        max_width = 0
        for neighbor in graph[node]:
            if neighbor != parent:
                path.append(neighbor)
                width = dfs(neighbor, node, path) + 1
                max_width = max(max_width, width)
                path.pop()
        return max_width

    def treewidth_util(node, parent, path):
        if not graph[node]:
            return 0
        max_width = 0
        for neighbor in graph[node]:
            if neighbor != parent:
                path.append(neighbor)
                width = dfs(neighbor, node, path) + 1
                max_width = max(max_width, width)
                path.pop()
        return max_width

    def treewidth_util(node, parent, path):
        if not graph[node]:
            return 0
        max_width = 0
        for neighbor in graph[node]:
            if neighbor != parent:
                path.append(neighbor)
                width = dfs(neighbor, node, path) + 1
                max_width = max(max_width, width)
                path.pop()
        return max_width

    def treewidth_util(node, parent, path):
        if not graph[node]:
            return 0
        max_width = 0
        for neighbor in graph[node]:
            if neighbor != parent:
                path.append(neighbor)
                width = dfs(neighbor, node, path) + 1
                max_width = max(max_width, width)
                path.pop()
        return max_width

    def treewidth_util(node, parent, path):
        if not graph[node]:
            return 0
        max_width = 0
        for neighbor in graph[node]:
            if neighbor != parent:
                path.append(neighbor)
                width = dfs(neighbor, node, path) + 1
                max_width = max(max_width, width)
                path.pop()