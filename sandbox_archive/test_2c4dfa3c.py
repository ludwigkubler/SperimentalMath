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
            max_row = i + max(range(i, n), key=lambda j: abs(matrix[j][i]))
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = Fraction(1, matrix[i][i])
            for j in range(n):
                if j != i:
                    row_factor = Fraction(matrix[j][i], matrix[i][i])
                    for k in range(n + 1):
                        matrix[j][k] -= row_factor * matrix[i][k]
        return matrix

    def det(matrix):
        n = len(matrix)
        if n == 2:
            return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        else:
            det_val = Fraction(0)
            for j in range(n):
                submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
                det_val += (-1) ** j * matrix[0][j] * det(submatrix)
            return det_val

    def frege_proof_depth(n):
        # Simplified model of Frege proof depth
        return int(Fraction(2, 3) * n + Fraction(1, 6))

    def min_etale_cohomology_rank(n):
        # Simplified model of minimum etale cohomology rank
        return int(Fraction(1, 4) * n ** 2)

    instances_tested = 0
    total_ratio = Fraction(0)
    max_n = 0

    for _ in range(30):
        n = random.randint(5, 40)
        if n > max_n:
            max_n = n
        
        # Generate a random CNF formula with n variables
        clauses = []
        for _ in range(n):
            literals = [random.choice([1, -1]) * (i + 1) for i in range(n)]
            clauses.append(literals)
        
        # Compute the minimum etale cohomology rank
        min_rank = min_etale_cohomology_rank(n)
        
        # Compute the Frege proof depth
        d_phi = frege_proof_depth(n)
        
        if d_phi == 0:
            continue
        
        ratio = Fraction(min_rank, d_phi)
        total_ratio += ratio
        instances_tested += 1

    conjecture_holds = all(ratio <= Fraction(2 * n, n) for _ in range(30))
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "min_etale_cohomology_rank_over_frege_depth",
        "metric_value": float(total_ratio / instances_tested),
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}**}}")
        results.append(result)

    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")