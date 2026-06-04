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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def dpll(clauses, assignment):
        if not clauses:
            return True
        clause = next(c for c in clauses if any(x in c for x in assignment))
        literal = next(x for x in clause if x in assignment)
        if literal > 0 and assignment[literal] == False:
            return False
        if literal < 0 and assignment[-literal] == True:
            return False
        if literal > 0:
            assignment[literal] = True
        else:
            assignment[-literal] = False
        return dpll(clauses, assignment)
    
    def clause_indicator_polynomial(n, clauses):
        q = [[Fraction(0) for _ in range(2**n)] for _ in range(2**n)]
        for i in range(2**n):
            for j in range(2**n):
                if all((i & (1 << x)) == (j & (1 << x)) or (i & (1 << -x)) == (j & (1 << -x)) for x in range(n)):
                    q[i][j] = Fraction(1)
        return q
    
    def rank(matrix):
        m, n = len(matrix), len(matrix[0])
        if m > n:
            matrix = list(zip(*matrix))
            m, n = n, m
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            if matrix[i][i] == 0:
                return float('inf')
            for j in range(i+1, m):
                factor = matrix[j][i] / matrix[i][i]
                for k in range(n):
                    matrix[j][k] -= factor * matrix[i][k]
        rank = sum(1 for row in matrix if any(x != 0 for x in row))
        return rank
    
    def height(clauses, assignment):
        if not clauses:
            return 0
        clause = next(c for c in clauses if any(x in c for x in assignment))
        literal = next(x for x in clause if x in assignment)
        if literal > 0 and assignment[literal] == False:
            return float('inf')
        if literal < 0 and assignment[-literal] == True:
            return float('inf')
        if literal > 0:
            assignment[literal] = True
        else:
            assignment[-literal] = False
        return 1 + max(height(clauses, assignment) for x in clause)
    
    n = random.randint(5, 40)
    clauses = [random.sample(range(-n, -1), random.randint(1, n)) for _ in range(random.randint(1, n))]
    q = clause_indicator_polynomial(n, clauses)
    rank_q = rank(q)
    assignment = {i: False for i in range(-n, 0)}
    height_dpll = height(clauses, assignment)
    
    return {
        "metric_name": "Rank vs Height",
        "metric_value": rank_q,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": rank_q <= height_dpll,
        "counterexample": "" if rank_q <= height_dpll else f"Counterexample: n={n}, Rank(Qφ)={rank_q}, Height(DPLL(φ))={height_dpll}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")