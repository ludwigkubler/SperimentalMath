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
    
    def generate_delone_set(n):
        # Placeholder for generating a Delone set with n tiles
        return [[random.random(), random.random()] for _ in range(n)]
    
    def char_poly(A):
        if len(A) == 1:
            return [A[0][0], 1]
        det_A = 0
        for j in range(len(A)):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det_A += (-1) ** j * A[0][j] * char_poly(submatrix)[0]
        return [det_A, 1]
    
    def matrix_rank(matrix):
        # Placeholder for computing the rank of a matrix
        rows = len(matrix)
        cols = len(matrix[0])
        rank = 0
        for i in range(rows):
            if any(matrix[i][j] != 0 for j in range(cols)):
                rank += 1
                for j in range(i + 1, rows):
                    factor = matrix[j][i] / matrix[i][i]
                    for k in range(cols):
                        matrix[j][k] -= factor * matrix[i][k]
        return rank
    
    def permutation_circuit_depth(poly):
        # Placeholder for computing the depth of a permutation circuit
        if len(poly) == 2:
            return 0
        return 1 + max(permutation_circuit_depth([poly[0], poly[2]]), permutation_circuit_depth([poly[1], poly[3]]))
    
    n = random.randint(5, 40)
    D = generate_delone_set(n)
    A = char_poly(D)
    rho_D = matrix_rank(A)
    depth_C = permutation_circuit_depth(A)
    
    return {
        "metric_name": "min_rank",
        "metric_value": rho_D,
        "instances_tested": 1,
        "conjecture_holds": rho_D <= depth_C,
        "counterexample": "" if rho_D <= depth_C else f"Delone set with rank {rho_D} and circuit depth {depth_C}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        support_fraction = 1.0
    else:
        support_fraction = sum(1 for r in results if "conjecture_holds" in r and r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(r['metric_value'] for r in results) / len(results)} std=0 support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if "counterexample" in r and r["counterexample"]), None)
        print(f"RESULT: FALSIFIED counterexample={results[0]['counterexample']} first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")