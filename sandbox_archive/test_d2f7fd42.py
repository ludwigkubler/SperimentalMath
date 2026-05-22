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
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            max_row = i + A[i:].index(max(abs(row[i]) for row in A[i:]))
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i + 1, n):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A
    
    def det(A):
        n = len(A)
        if n == 1:
            return A[0][0]
        elif n == 2:
            return A[0][0] * A[1][1] - A[0][1] * A[1][0]
        else:
            det_val = 0
            for c in range(n):
                submatrix = [row[:c] + row[c+1:] for row in A[1:]]
                sign = (-1) ** (c % 2)
                det_val += sign * A[0][c] * det(submatrix)
            return det_val
    
    def geometric_entropy(A):
        n = len(A)
        rank = sum(1 for row in gaussian_elimination(A) if any(row[i] != 0 for i in range(n)))
        return rank * math.log2(n)
    
    def dpll_width(G, assignment=[]):
        if not G:
            return 0
        var = next((i for i in range(len(G)) if all(not clause[i] for clause in G)), None)
        if var is None:
            return 1
        return max(dpll_width([clause for clause in G if clause[var]], assignment + [True]), dpll_width([clause for clause in G if not clause[var]], assignment + [False]))
    
    def generate_cnf(n, m):
        variables = list(range(n))
        clauses = []
        for _ in range(m):
            clause = random.sample(variables, random.randint(1, n))
            clauses.append(clause)
        return clauses
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    m = random.randint(n, 2 * n)
    cnf = generate_cnf(n, m)
    
    G = []
    for clause in cnf:
        row = [0] * n
        for var in clause:
            if var < 0:
                row[-var - 1] = -1
            else:
                row[var - 1] = 1
        G.append(row)
    
    H_G = geometric_entropy(G)
    W_G = dpll_width(G)
    
    return {
        "metric_name": "geometric_entropy",
        "metric_value": H_G,
        "instances_tested": 1,
        "conjecture_holds": H_G <= 0.5 * n * math.log2(m) and W_G <= 3 * math.sqrt(H_G),
        "counterexample": "" if H_G <= 0.5 * n * math.log2(m) and W_G <= 3 * math.sqrt(H_G) else f"H(G)={H_G}, W(G)={W_G}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000003) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_H_G = sum(r["metric_value"] for r in results) / len(results)
    std_H_G = math.sqrt(sum((r["metric_value"] - mean_H_G) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_H_G} std={std_H_G} support_fraction={support_fraction}")
    elif support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_H_G} std={std_H_G} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")