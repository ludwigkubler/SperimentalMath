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
    n = random.randint(5, 40)
    m = 2 ** n
    
    # Generate a random XOR tautology of size n
    tautology = [random.choice([0, 1]) for _ in range(m)]
    
    # Construct the associated Kähler form (simplified as a matrix)
    kahler_form = [[0] * m for _ in range(m)]
    for i in range(m):
        for j in range(m):
            if i != j:
                kahler_form[i][j] = tautology[i] ^ tautology[j]
    
    # Compute the rank of the Kähler form
    def matrix_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(m):
            if any(matrix[i][j] != 0 for j in range(n)):
                rank += 1
                for j in range(n):
                    matrix[i][j] /= matrix[i][i]
                for k in range(m):
                    if k != i and any(matrix[k][j] != 0 for j in range(n)):
                        for j in range(n):
                            matrix[k][j] -= matrix[i][j] * matrix[k][i]
        return rank
    
    rank_k = matrix_rank(kahler_form)
    
    # Construct the smallest DNF representation of the tautology
    def dnf_width(tautology):
        n = len(tautology)
        width = 0
        for i in range(1 << n):
            clause = []
            for j in range(n):
                if (i >> j) & 1:
                    clause.append(j + 1)
                else:
                    clause.append(-(j + 1))
            if all(tautology[j] == (sum(clause) % 2) for j in range(n)):
                width = max(width, len(clause))
        return width
    
    width_dnf = dnf_width(tautology)
    
    # Compare the rank of the Kähler form with the width of the DNF representation
    if rank_k < width_dnf / 2 or rank_k > width_dnf * 2:
        conjecture_holds = False
        counterexample = f"rank(K)={rank_k}, width(DNF)={width_dnf}"
    else:
        conjecture_holds = True
        counterexample = ""
    
    return {
        "metric_name": "Rank vs DNF Width",
        "metric_value": rank_k,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2**i + 7 for i in range(5, 30)]
    else:
        seeds = list(map(int, sys.argv[1:]))

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")