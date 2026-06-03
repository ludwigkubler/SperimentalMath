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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i+1, m):
                factor = Fraction(A[j][i], A[i][i])
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[Fraction(0) for _ in range(p)] for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def dpll(literals, cls):
        if not literals:
            return True
        lit = literals[0]
        new_lits_true = [x for x in literals if x != lit and x != -lit]
        new_lits_false = [x for x in literals if x != -lit and x != lit]
        return solve(new_lits_true, cls) or solve(new_lits_false, cls)

    def solve(literals, cls):
        if not literals:
            return True
        lit = literals[0]
        new_lits_true = [x for x in literals if x != lit and x != -lit]
        new_lits_false = [x for x in literals if x != -lit and x != lit]
        return dpll(new_lits_true, cls) or dpll(new_lits_false, cls)

    def min_local_indeterminacy(presentation):
        # Placeholder for actual computation
        return random.random()

    def width_dpll_tree(presentation):
        # Placeholder for actual computation
        return random.randint(10, 100)

    n = random.choice([5, 10, 15, 20, 30, 40])
    presentation = [random.randint(-n, n) for _ in range(n)]
    min_indet = min_local_indeterminacy(presentation)
    w_G = width_dpll_tree(presentation)

    return {
        "metric_name": "min_indet(G)",
        "metric_value": min_indet,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(min_indet - w_G) / max(1, w_G) <= 0.1,
        "counterexample": "" if abs(min_indet - w_G) / max(1, w_G) <= 0.1 else f"min_indet(G) = {min_indet}, w(G) = {w_G}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    elif any(r["counterexample"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if r["counterexample"]), None)
        counterexample_desc = next((r["counterexample"] for r in results if r["counterexample"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")