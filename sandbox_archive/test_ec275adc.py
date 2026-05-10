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

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        # Find pivot
        max_row = i + max(range(i, rows), key=lambda r: abs(matrix[r][i]))
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate below
        for j in range(i+1, rows):
            factor = matrix[j][i] / matrix[i][i]
            for k in range(cols):
                matrix[j][k] -= factor * matrix[i][k]
    
    rank = sum(1 for row in matrix if any(row))
    return rank

def bdd_width(truth_table):
    n = len(truth_table)
    variables = list(range(n))
    width = 0
    
    while variables:
        new_variables = []
        for var in variables:
            if all(truth_table[i][var] == truth_table[i][var+1] for i in range(len(truth_table)//2)):
                continue
            new_variables.append(var)
        variables = new_variables
        width += 1
    
    return width

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 10
    M_f = [[random.choice([0, 1]) for _ in range(2**n)] for _ in range(n)]
    
    rank = gaussian_elimination(M_f)
    width = bdd_width(M_f)
    
    return {
        "metric_name": "width_vs_rank",
        "metric_value": width,
        "instances_tested": 1,
        "conjecture_holds": width >= rank,
        "counterexample": "" if width >= rank else f"Width {width} < Rank {rank}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]  # Default to first 30 primes
    
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")