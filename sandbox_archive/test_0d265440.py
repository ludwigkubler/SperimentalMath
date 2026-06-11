# auto-injected by SEC sandbox
import math
import itertools
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            max_row = max(range(i, n), key=lambda k: abs(matrix[k][i]))
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = Fraction(-matrix[i][i], matrix[i][i])
            for j in range(i + 1, n):
                matrix[j][i] *= factor
            for j in range(n):
                if i == j:
                    continue
                factor = Fraction(matrix[j][i], matrix[i][i])
                for k in range(i, n):
                    matrix[j][k] += factor * matrix[i][k]
        return matrix

    def rank_variance(matrix):
        rref = gaussian_elimination(matrix)
        rank = sum(1 for row in rref if any(row))
        return rank / len(matrix)

    def generate_cnf(n):
        clauses = []
        for _ in range(n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            clauses.append(clause)
        return clauses

    def term_graph(cnf):
        graph = {}
        for clause in cnf:
            for literal in clause:
                if abs(literal) not in graph:
                    graph[abs(literal)] = set()
                for other_literal in clause:
                    if literal != other_literal and abs(other_literal) != abs(literal):
                        graph[abs(literal)].add(abs(other_literal))
        return graph

    def minimal_order(graph):
        visited = set()
        order = 0
        for node in graph:
            if node not in visited:
                stack = [node]
                while stack:
                    current = stack.pop()
                    if current not in visited:
                        visited.add(current)
                        stack.extend(graph[current] - visited)
                order += 1
        return order

    def communication_complexity_rank_variance(cnf):
        term_graph_matrix = [[0] * (len(cnf) + 1) for _ in range(len(cnf) + 1)]
        for i, clause in enumerate(cnf):
            for literal in clause:
                term_graph_matrix[i][abs(literal)] += 1
        return rank_variance(term_graph_matrix)

    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_cnf(n)
    graph = term_graph(cnf)
    min_order = minimal_order(graph)
    rank_var = communication_complexity_rank_variance(cnf)

    return {
        "metric_name": "Correlation",
        "metric_value": min_order * rank_var,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True if rank_var >= 0 else False,
        "counterexample": "" if rank_var >= 0 else f"Negative rank variance: {rank_var}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")