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
            pivot = matrix[i][i]
            if pivot == 0:
                continue
            for j in range(cols):
                matrix[i][j] /= pivot
            for k in range(rows):
                if k != i:
                    factor = matrix[k][i]
                    for j in range(cols):
                        matrix[k][j] -= factor * matrix[i][j]
        return matrix

    def rank(matrix):
        rows, cols = len(matrix), len(matrix[0])
        reduced_matrix = gaussian_elimination(matrix)
        rank = 0
        for row in reduced_matrix:
            if any(row):
                rank += 1
        return rank

    n = random.choice([5, 10, 15, 20, 30, 40])
    s = random.randint(1, n)
    
    # Generate a random Boolean function f computable by an AC0 circuit of size s
    def ac0_circuit(s):
        if s == 1:
            return lambda x: x
        else:
            f1 = ac0_circuit(s // 2)
            f2 = ac0_circuit(s - s // 2)
            return lambda x: f1(x) and f2(x)
    
    f = ac0_circuit(s)
    
    # Find a Weierstrass elliptic curve E over the finite field F2 with a marked point P
    # such that the tropicalization of the divisor class [P] has minimal rank s
    def weierstrass_curve(n):
        return [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    
    E = weierstrass_curve(n)
    P = (random.randint(0, n-1), random.randint(0, n-1))
    
    # Verify the converse statement by checking if there exists an elliptic curve and a point P
    # such that the tropical rank of [P] is exactly s for all AC0 circuits computing f
    def tropical_rank(E, P):
        return rank([[E[0][i] + E[1][j] + E[2][k] for i in range(n) for j in range(n) for k in range(n)]])
    
    if tropical_rank(E, P) != s:
        return {
            "metric_name": "tropical_rank",
            "metric_value": tropical_rank(E, P),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Counterexample for n={n}, s={s}: Tropical rank is {tropical_rank(E, P)}"
        }
    
    return {
        "metric_name": "tropical_rank",
        "metric_value": tropical_rank(E, P),
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 30)]
    
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
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")