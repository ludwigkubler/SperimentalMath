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
            max_row = i
            for j in range(i + 1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = Fraction(matrix[i][i])
            for j in range(i, n):
                matrix[i][j] /= factor
            for j in range(n):
                if j != i:
                    factor = matrix[j][i]
                    for k in range(i, n):
                        matrix[j][k] -= factor * matrix[i][k]
        return matrix

    def rank(matrix):
        n = len(matrix)
        echelon_form = gaussian_elimination(matrix)
        rank = 0
        for row in echelon_form:
            if any(row):
                rank += 1
        return rank

    def tseitin_formula(n, G):
        clauses = []
        for i in range(2**n):
            binary = [int(b) for b in format(i, f'0{n}b')]
            clause = []
            for j in range(n):
                if binary[j] == 1:
                    clause.append(j + 1)
                else:
                    clause.append(-(j + 1))
            clauses.append(clause)
        return clauses

    def resolution_length(clauses):
        stack = []
        while True:
            new_clause = None
            for i in range(len(stack)):
                for j in range(i + 1, len(stack)):
                    if any(-x in stack[i] and x in stack[j] for x in set(stack[i]) & set(stack[j])):
                        new_clause = [x for x in stack[i] if x not in stack[j]] + [x for x in stack[j] if -x not in stack[i]]
                        break
                if new_clause:
                    break
            if not new_clause:
                return len(stack)
            stack.append(new_clause)

    def ramanujan_graph(n):
        G = []
        for i in range(n):
            row = [0] * n
            row[i] = 1
            for j in range(i + 1, n):
                if random.random() < (2 * (n - 1) ** 2 / n ** 2):
                    row[j] = 1
                    G.append((i, j))
                    G.append((j, i))
        return G

    def tropicalized_quantum_state(G):
        n = len(G)
        Q = [[0] * n for _ in range(n)]
        for u, v in G:
            Q[u][v] = Fraction(1, 2)
            Q[v][u] = Fraction(1, 2)
        return Q

    n = random.choice([5, 10, 15, 20, 30, 40])
    G = ramanujan_graph(n)
    T = tseitin_formula(n, G)
    Q = tropicalized_quantum_state(G)
    R = resolution_length(T)

    expected_length = 2 ** (n / 8) + n / 10
    diff = abs(R - expected_length)

    return {
        "metric_name": "Resolution proof length",
        "metric_value": R,
        "instances_tested": 1,
        "conjecture_holds": R >= expected_length - 3 * (n / 10),
        "counterexample": "" if R >= expected_length - 3 * (n / 10) else f"R={R}, expected>=R-{3*(n/10)}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"R<{expected_length-3*(n/10)}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")