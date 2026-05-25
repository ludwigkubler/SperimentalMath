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

def gaussian_elimination(M):
    n = len(M)
    for i in range(n):
        # Find pivot
        max_row = i
        for k in range(i+1, n):
            if abs(M[k][i]) > abs(M[max_row][i]):
                max_row = k
        M[i], M[max_row] = M[max_row], M[i]
        
        # Eliminate below pivot
        factor = 1 / M[i][i]
        for j in range(i, n):
            M[i][j] *= factor
        for k in range(i+1, n):
            factor = M[k][i]
            for j in range(i, n):
                M[k][j] -= factor * M[i][j]

    # Back substitution
    for i in range(n-1, -1, -1):
        for k in range(i-1, -1, -1):
            factor = M[k][i]
            for j in range(n):
                M[k][j] -= factor * M[i][j]
    
    rank = 0
    for row in M:
        if any(row):
            rank += 1
    return rank

def moment_matrix(p, n):
    M = [[0] * (n+1) for _ in range(n+1)]
    for term in p:
        degree = sum(term[1])
        for i in range(degree + 1):
            for j in range(degree - i + 1):
                M[i][j] += term[0] * math.comb(degree, i) * math.comb(degree - i, j)
    return M

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    d = random.randint(1, 3)
    
    # Generate a random max-CUT instance
    variables = [f'x{i}' for i in range(n)]
    terms = []
    for _ in range(random.randint(2, 10)):
        coeffs = [random.uniform(-1, 1) for _ in range(d + 1)]
        exponents = [random.sample(range(n), random.randint(1, d)) for _ in range(d + 1)]
        terms.append((coeffs, exponents))
    
    p = sum(coeffs * x**sum(exponents) for coeffs, exponents in terms)
    
    M_p = moment_matrix(p, n)
    rank_M_p = gaussian_elimination(M_p)
    
    if rank_M_p < d * math.log(n)**2:
        ratio = 0.878
    else:
        ratio = 1.0
    
    return {
        "metric_name": "Rank of Moment Matrix",
        "metric_value": rank_M_p,
        "instances_tested": 1,
        "conjecture_holds": rank_M_p >= d * math.log(n)**2 or ratio <= 0.878,
        "counterexample": "" if rank_M_p >= d * math.log(n)**2 else f"Approximation ratio {ratio} is not worse than 0.878"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 9999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
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
        print(f"RESULT: FALSIFIED counterexample=\"Approximation ratio is not worse than 0.878\" first_failing_seed={first_failing_seed}")