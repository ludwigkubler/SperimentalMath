# auto-injected by SEC sandbox
import itertools
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            max_row = i
            for k in range(i+1, n):
                if abs(matrix[k][i]) > abs(matrix[max_row][i]):
                    max_row = k
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = matrix[i][i]
            for j in range(n + 1):
                matrix[i][j] /= factor
            for k in range(n):
                if k != i:
                    factor = matrix[k][i]
                    for j in range(n + 1):
                        matrix[k][j] -= factor * matrix[i][j]
        return matrix

    def is_independent_set(graph, vertex, independent_set):
        for v in independent_set:
            if graph[v][vertex]:
                return False
        return True

    def find_maximal_independent_set(graph):
        n = len(graph)
        max_size = 0
        max_set = []
        for i in range(1 << n):
            independent_set = [j for j in range(n) if (i & (1 << j))]
            if all(is_independent_set(graph, v, independent_set) for v in independent_set):
                if len(independent_set) > max_size:
                    max_size = len(independent_set)
                    max_set = independent_set
        return max_set

    def tseitin_formula(graph):
        n = len(graph)
        variables = list(range(1, 2 * n + 1))
        clauses = []
        for v in range(n):
            clauses.append([variables[2 * v - 1], variables[2 * v]])
            for u in range(v + 1, n):
                if graph[v][u]:
                    clauses.append([-variables[2 * v - 1], -variables[2 * u - 1]])
                    clauses.append([-variables[2 * v], variables[2 * u - 1]])
                    clauses.append([variables[2 * v], -variables[2 * u]])
        return variables, clauses

    def resolution_width(clauses):
        queue = [c for c in clauses if len(c) == 1]
        learned_clauses = []
        while queue:
            clause = queue.pop()
            literal = clause[0]
            opposite_literal = -literal
            new_clauses = []
            for c in learned_clauses:
                if opposite_literal in c:
                    continue
                if literal in c:
                    new_clauses.append([x for x in c if x != literal])
                else:
                    new_clauses.append(c + [opposite_literal])
            queue.extend(new_clauses)
            learned_clauses.extend(new_clauses)
        return max(len(c) for c in learned_clauses)

    def monoidal_category_size(graph):
        n = len(graph)
        independent_set = find_maximal_independent_set(graph)
        size = 2 ** len(independent_set)
        return size

    def generate_d_regular_graph(n, d):
        graph = [[0] * n for _ in range(n)]
        degree_count = [0] * n
        for _ in range(d * n // 2):
            while True:
                u = random.randint(0, n - 1)
                v = random.randint(0, n - 1)
                if u != v and not graph[u][v]:
                    graph[u][v] = 1
                    graph[v][u] = 1
                    degree_count[u] += 1
                    degree_count[v] += 1
                    break
        return graph

    def dpll(clauses):
        def solve(variables, assignment):
            if not clauses:
                return True
            literal = next(l for l in variables if l not in assignment and -l not in assignment)
            for value in [True, False]:
                new_assignment = assignment.copy()
                new_assignment[literal] = value
                if all(not any(clause[i] == 1 for i in range(len(clause))) for clause in clauses):
                    if solve(variables, new_assignment):
                        return True
            return False

        variables = list(range(1, 2 * len(clauses) + 1))
        return solve(variables, {})

    def resolution_width(clauses):
        queue = [c for c in clauses if len(c) == 1]
        learned_clauses = []
        while queue:
            clause = queue.pop()
            literal = clause[0]
            opposite_literal = -literal
            new_clauses = []
            for c in learned_clauses:
                if opposite_literal in c:
                    continue
                if literal in c:
                    new_clauses.append([x for x in c if x != literal])
                else:
                    new_clauses.append(c + [opposite_literal])
            queue.extend(new_clauses)
            learned_clauses.extend(new_clauses)
        return max(len(c) for c in learned_clauses)

    def monoidal_category_size(graph):
        n = len(graph)
        independent_set = find_maximal_independent_set(graph)
        size = 2 ** len(independent_set)
        return size

    def generate_d_regular_graph(n, d):
        graph = [[0] * n for _ in range(n)]
        degree_count = [0] * n
        for _ in range(d * n // 2):
            while True:
                u = random.randint(0, n - 1)
                v = random.randint(0, n - 1)
                if u != v and not graph[u][v]:
                    graph[u][v] = 1
                    graph[v][u] = 1
                    degree_count[u] += 1
                    degree_count[v] += 1
                    break
        return graph

    def dpll(clauses):
        def solve(variables, assignment):
            if not clauses:
                return True
            literal = next(l for l in variables if l not in assignment and -l not in assignment)
            for value in [True, False]:
                new_assignment = assignment.copy()
                new_assignment[literal] = value
                if all(not any(clause[i] == 1 for i in range(len(clause))) for clause in clauses):
                    if solve(variables, new_assignment):
                        return True
            return False

        variables = list(range(1, 2 * len(clauses) + 1))
        return solve(variables, {})

    def resolution_width(clauses):
        queue = [c for c in clauses if len(c) == 1]
        learned_clauses = []
        while queue:
            clause = queue.pop()
            literal = clause[0]
            opposite_literal = -literal
            new_clauses = []
            for c in learned_clauses:
                if opposite_literal in c:
                    continue
                if literal in c:
                    new_clauses.append([x for x in c if x != literal])
                else:
                    new_clauses.append(c + [opposite_literal])
            queue.extend(new_clauses)
            learned_clauses.extend(new_clauses)
        return max(len(c) for c in learned_clauses)

    def monoidal_category_size(graph):
        n = len(graph)
        independent_set = find_maximal_independent_set(graph)
        size = 2 ** len(independent_set)
        return size

    def generate_d_regular_graph(n, d):
        graph = [[0] * n for _ in range(n)]
        degree_count = [0] * n
        for _ in range(d * n // 2):
            while True:
                u = random.randint(0, n - 1)
                v = random.randint(0, n - 1)
                if u != v and not graph[u][v]:
                    graph[u][v] = 1
                    graph[v][u] = 1
                    degree_count[u] += 1
                    degree_count[v] += 1
                    break
        return graph

    def dpll(clauses):
        def solve(variables, assignment):
            if not clauses:
                return True
            literal = next(l for l in variables if l not in assignment and -l not in assignment)
            for value in [True, False]:
                new_assignment = assignment.copy()
                new_assignment[literal] = value
                if all(not any(clause[i] == 1 for i in range(len(clause))) for clause in clauses):
                    if solve(variables, new_assignment):
                        return True
            return False

        variables = list(range(1, 2 * len(clauses) + 1))
        return solve(variables, {})

    def resolution_width(clauses):
        queue = [c for c in clauses if len(c) == 1]
        learned_clauses = []
        while queue:
            clause = queue.pop()
            literal = clause[0]
            opposite_literal = -literal
            new_clauses = []
            for c in learned_clauses:
                if opposite_literal in c:
                    continue
                if literal in c:
                    new_clauses.append([x for x in c if x != literal])
                else:
                    new_clauses.append(c + [opposite_literal])
            queue.extend(new_clauses)
            learned_clauses.extend(new_clauses)
        return max(len(c) for c in learned_clauses)

    def monoidal_category_size(graph):
        n = len(graph)
        independent_set = find_maximal_independent_set(graph)
        size = 2 ** len(independent_set)
        return size

    def generate_d_regular_graph(n, d):
        graph = [[0] * n for _ in range(n)]
        degree_count = [0] * n
        for _ in range(d * n // 2):
            while True:
                u = random.randint(0, n - 1)
                v = random.randint(0, n - 1)
                if u != v and not graph[u][v]:
                    graph[u][v] = 1
                    graph[v][u] = 1
                    degree_count[u] += 1
                    degree_count[v] += 1
                    break
        return graph

    def dpll(clauses):
        def solve(variables, assignment):
            if not clauses:
                return True
            literal = next(l for l in variables if l not in assignment and -l not in assignment)
            for value in [True, False]:
                new_assignment = assignment.copy()
                new_assignment[literal] = value
                if all(not any(clause[i] == 1 for i in range(len(clause))) for clause in clauses):
                    if solve(variables, new_assignment):
                        return True
            return False

        variables = list(range(1, 2 * len(clauses) + 1))
        return solve(variables, {})

    def resolution_width(clauses):
        queue = [c for c in clauses if len(c) == 1]
        learned_clauses = []
        while queue:
            clause = queue.pop()
            literal = clause[0]
            opposite_literal = -literal
            new_clauses = []
            for c in learned_clauses:
                if opposite_literal in c:
                    continue
                if literal in c:
                    new_clauses.append([x for x in c if x != literal])
                else:
                    new_clauses.append(c + [opposite_literal])
            queue.extend(new_clauses)
            learned_clauses.extend(new_clauses)
        return max(len(c) for c in learned_clauses)

    def monoidal_category_size(graph):
        n = len(graph)
        independent_set = find_maximal_independent_set(graph)
        size = 2 ** len(independent_set)
        return size

    def generate_d_regular_graph(n, d):
        graph = [[0] * n for _ in range(n)]
        degree_count = [0] * n
        for _ in range(d * n // 2):
            while True:
                u = random.randint(0, n - 1)
                v = random.randint(0, n - 1)
                if u != v and not graph[u][v]:
                    graph[u][v] = 1
                    graph[v][u] = 1
                    degree_count[u] += 1
                    degree_count[v] += 1
                    break
        return graph

    def dpll(clauses):
        def solve(variables, assignment):
            if not clauses:
                return True
            literal = next(l for l in variables if l not in assignment and -l not in assignment)
            for value in [True, False]:
                new_assignment = assignment.copy()
                new_assignment[literal] = value
                if all(not any(clause[i] == 1 for i in range(len(clause))) for clause in clauses):
                    if solve(variables, new_assignment):
                        return True
            return False

        variables = list(range(1, 2 * len(clauses) + 1))
        return solve(variables, {})

    def resolution_width(clauses):
        queue = [c for c in clauses if len(c) == 1]
        learned_clauses = []
        while queue:
            clause = queue.pop()
            literal = clause[0]
            opposite_literal = -literal
            new_clauses = []
            for c in learned_clauses:
                if opposite_literal in c:
                    continue
                if literal in c:
                    new_clauses.append([x for x in c if x != literal])
                else:
                    new_clauses.append(c + [opposite_literal])
            queue.extend(new_clauses)
            learned_clauses.extend(new_clauses)
        return max(len(c) for c in learned_clauses)

    def monoidal_category_size(graph):
        n = len(graph)
        independent_set = find_maximal_independent_set(graph)
        size = 2 ** len(independent_set)
        return size

    def generate_d_regular_graph(n, d):
        graph = [[0] * n for _ in range(n)]
        degree_count = [0] * n
        for _ in range(d * n // 2):
            while True:
                u = random.randint(0, n - 1)
                v = random.randint(0, n - 1)
                if u != v and not graph[u][v]:
                    graph[u][v] = 1
                    graph[v][u] = 1
                    degree_count[u] += 1
                    degree_count[v] += 1
                    break
        return graph

    def dpll(clauses):
        def solve(variables, assignment):
            if not clauses:
                return True
            literal = next(l for l in variables if l not in assignment and -l not in assignment)
            for value in [True, False]:
                new_assignment = assignment.copy()
                new_assignment[literal] = value
                if all(not any(clause[i] == 1 for i in range(len(clause))) for clause in clauses):
                    if solve(variables, new_assignment):
                        return True
            return False

        variables = list(range(1, 2 * len(clauses) + 1))
        return solve(variables, {})

    def resolution_width(clauses):
        queue = [c for c in clauses if len(c) == 1]
        learned_clauses = []
        while queue:
            clause = queue.pop()
            literal = clause[0]
            opposite_literal = -literal
            new_clauses = []
            for c in learned_clauses:
                if opposite_literal in c:
                    continue
                if literal in c:
                    new_clauses.append([x for x in c if x != literal])
                else:
                    new_clauses.append(c + [opposite_literal])
            queue.extend(new_clauses)
            learned_clauses.extend(new_clauses)
        return max(len(c) for c in learned_clauses)

    def monoidal_category_size(graph):
        n = len(graph)
        independent_set = find_maximal_independent_set(graph)
        size = 2 ** len(independent_set)
        return size

    def generate_d_regular_graph(n, d):
        graph = [[0] * n for _ in range(n)]
        degree_count = [0] * n
        for _ in range(d * n // 2):
            while True:
                u = random.randint(0, n - 1)
                v = random.randint(0, n - 1)
                if u != v and not graph[u][v]:
                    graph[u][v] = 1
                    graph[v][u] = 1
                    degree_count[u] += 1
                    degree_count[v] += 1
                    break
        return graph

    def dpll(clauses):
        def solve(variables, assignment):
            if not clauses:
                return True
            literal = next(l for l in variables if l not in assignment and -l not in assignment)
            for value in [True, False]:
                new_assignment = assignment.copy()
                new_assignment[literal] = value
                if all(not any(clause[i] == 1 for i in range(len(clause))) for clause in clauses):
                    if solve(variables, new_assignment):
                        return True
            return False

        variables = list(range(1, 2 * len(clauses) + 1))
        return solve(variables, {})

    def resolution_width(clauses):
        queue = [c for c in clauses if len(c) == 1]
        learned_clauses = []
        while queue:
            clause = queue.pop()
            literal = clause[0]
            opposite_literal = -literal
            new_clauses = []
            for c in learned_clauses:
                if opposite_literal in c:
                    continue
                if literal in c:
                    new_clauses.append([x for x in c if x != literal])
                else:
                    new_clauses.append(c + [opposite_literal])
            queue.extend(new_clauses)
            learned_clauses.extend(new_clauses)
        return max(len(c) for c in learned_clauses)

    def monoidal_category_size(graph):
        n = len(graph)
        independent_set = find_maximal_independent_set(graph)
        size = 2 ** len(independent_set)
        return size

    def generate_d_regular_graph(n, d):
        graph = [[0] * n for _ in range(n)]
        degree_count = [0] * n
        for _ in range(d * n // 2):
            while True:
                u = random.randint(0, n - 1)
                v = random.randint(0, n - 1)
                if u != v and not graph[u][v]:
                    graph[u][v] = 1
                    graph[v][u] = 1
                    degree_count[u] += 1
                    degree_count[v] += 1
                    break
        return graph

    def dpll(clauses):
        def solve(variables, assignment):
            if not clauses:
                return True
            literal = next(l for l in variables if l not in assignment and -l not in assignment)
            for value in [True, False]:
                new_assignment = assignment.copy()
                new_assignment[literal] = value
                if all(not any(clause[i] == 1 for i in range(len(clause))) for clause in clauses):
                    if solve(variables, new_assignment):
                        return True
            return False
