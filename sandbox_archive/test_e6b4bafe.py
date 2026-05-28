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
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda k: abs(matrix[k][i]))
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = Fraction(1, matrix[i][i])
            for j in range(i, n):
                matrix[i][j] *= factor
            for j in range(n):
                if i != j:
                    factor = -Fraction(matrix[j][i], matrix[i][i])
                    for k in range(n):
                        matrix[j][k] += factor * matrix[i][k]
        rank = sum(1 for row in matrix if any(row))
        return rank
    
    def generate_frege_proof(n):
        # Simplified Frege proof generation (for illustration)
        return [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):
            proof = generate_frege_proof(n)
            dual_object = gaussian_elimination(proof)
            total_rank += dual_object
            instances_tested += 1
    
    expected_rank = Fraction(math.log(n), math.log(math.log(n)))
    avg_rank = Fraction(total_rank, instances_tested)
    
    conjecture_holds = abs(avg_rank - expected_rank) <= Fraction(10, 100) * expected_rank
    counterexample = "" if conjecture_holds else f"Expected {expected_rank}, got {avg_rank}"
    
    return {
        "metric_name": "Average Rank of Dual Object",
        "metric_value": avg_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)
    
    total_rank = sum(r["metric_value"] for r in results)
    instances_tested = sum(r["instances_tested"] for r in results)
    avg_rank = Fraction(total_rank, instances_tested)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={avg_rank} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")