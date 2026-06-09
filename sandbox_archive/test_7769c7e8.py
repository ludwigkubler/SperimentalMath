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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i+1, n):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(n):
                A[j][k] -= factor * A[i][k]

def rank(cnf):
    num_vars = len(cnf[0])
    A = [[Fraction(0) for _ in range(num_vars)] for _ in range(num_vars)]
    for clause in cnf:
        for literal in clause:
            var_index = abs(literal) - 1
            if literal > 0:
                A[var_index][var_index] += Fraction(1)
            else:
                A[var_index][var_index] -= Fraction(1)
    gaussian_elimination(A)
    rank = sum(1 for row in A if any(coeff != Fraction(0) for coeff in row))
    return rank

def dpll(cnf, assignment={}):
    if not cnf:
        return True
    clause = next(clause for clause in cnf if any(lit in assignment or -lit in assignment for lit in clause))
    literal = next(lit for lit in clause if lit not in assignment and -lit not in assignment)
    new_cnf = [c for c in cnf if literal not in c and -literal not in c]
    return dpll(new_cnf, assignment | {literal: True}) or dpll(new_cnf, assignment | {-literal: True})

def circuit_complexity(cnf):
    return len(cnf)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    m = 2 * n
    cnf = [[random.randint(1, n) for _ in range(random.randint(1, 3))] for _ in range(m)]
    r = rank(cnf)
    c = circuit_complexity(cnf)
    return {
        "metric_name": "rank_circuit_difference",
        "metric_value": abs(r - c),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(r - c) <= Fraction(0.1 * n, n),
        "counterexample": "" if abs(r - c) <= Fraction(0.1 * n, n) else f"CNF with rank {r} and circuit complexity {c}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 37))  # Default to first 30 primes if no seeds provided
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)

    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=empty_results")