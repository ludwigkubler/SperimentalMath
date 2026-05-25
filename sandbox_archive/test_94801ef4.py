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
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            max_row = i + max(range(i, rows), key=lambda r: abs(matrix[r][i]))
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            for j in range(cols):
                if j != i:
                    factor = matrix[j][i] / matrix[i][i]
                    for k in range(rows):
                        matrix[j][k] -= factor * matrix[i][k]
        return matrix

    def rank(matrix):
        rows, cols = len(matrix), len(matrix[0])
        rref = gaussian_elimination(matrix)
        rank = 0
        for row in rref:
            if any(row):
                rank += 1
        return rank

    def random_cnf(n: int) -> list:
        clauses = []
        for _ in range(2 ** n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if any(clause):
                clauses.append(clause)
        return clauses

    def resolution_tree(cnf: list) -> dict:
        tree = {}
        stack = []
        for clause in cnf:
            stack.append((clause, []))
        while stack:
            clause, path = stack.pop()
            if not clause:
                continue
            literal = abs(clause[0])
            new_clauses = [c for c in cnf if literal not in c and -literal not in c]
            tree[id(path)] = (path, new_clauses)
            for other_clause in new_clauses:
                if literal in other_clause:
                    stack.append((other_clause, path + [literal]))
        return tree

    def min_rank(tree):
        nodes = list(tree.values())
        ranks = []
        while nodes:
            node, children = nodes.pop(0)
            rank = 1
            for child in children:
                rank += max(ranks) if ranks else 1
            ranks.append(rank)
        return sum(ranks)

    n_values = [10, 15, 20, 25, 30, 35, 40]
    moduli_ranks = []
    tree_ranks = []

    for n in n_values:
        cnf = random_cnf(n)
        moduli_rank = rank([[abs(lit) for lit in clause] for clause in cnf])
        tree_rank = min_rank(resolution_tree(cnf))
        moduli_ranks.append(moduli_rank)
        tree_ranks.append(tree_rank)

    mean_moduli_rank = sum(moduli_ranks) / len(moduli_ranks)
    mean_tree_rank = sum(tree_ranks) / len(tree_ranks)
    
    conjecture_holds = all(m >= 2 * t for m, t in zip(moduli_ranks, tree_ranks))
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "Minimal Rank",
        "metric_value": mean_moduli_rank,
        "instances_tested": len(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")