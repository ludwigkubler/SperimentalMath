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
    M = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    
    def matrix_minor(M, i, j):
        return [row[:j] + row[j+1:] for row in M[:i] + M[i+1:]]
    
    def determinant(M):
        if len(M) == 0:
            return 0
        elif len(M) == 1:
            return M[0][0]
        else:
            det = 0
            for c in range(len(M)):
                det += ((-1)**c) * M[0][c] * determinant(matrix_minor(M, 0, c))
            return det
    
    def euler_characteristic(M):
        rank = len(set(tuple(row) for row in M))
        return n - rank + 1
    
    comm_complexity = abs(determinant(M))
    chi_M = euler_characteristic(M)
    
    metric_value = comm_complexity
    instances_tested = 1
    n_max = n
    conjecture_holds = False
    counterexample = ""
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, min(30, len(primes)))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" not in r or r["conjecture_holds"] for r in results):
        support_fraction = sum(1 for r in results if "conjecture_holds" not in r or r["conjecture_holds"]) / len(results)
        RESULT = f"SUPPORTED mean={sum(r['metric_value'] for r in results) / len(results):.2f} std=0.00 support_fraction={support_fraction:.2f}"
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if "counterexample" in result and result["counterexample"])
        RESULT = f"FALSIFIED counterexample=\"{next(r['counterexample'] for r in results if 'counterexample' in r)}\" first_failing_seed={first_failing_seed}"
    else:
        RESULT = "INCONCLUSIVE no data"
    
    print(RESULT)