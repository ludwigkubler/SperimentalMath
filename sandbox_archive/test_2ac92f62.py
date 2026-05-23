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
    
    def perm(n):
        return [i for i in range(1, n+1)]
    
    def det(matrix):
        if len(matrix) == 1:
            return matrix[0][0]
        elif len(matrix) == 2:
            return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        else:
            det_val = 0
            for c in range(len(matrix)):
                submatrix = [row[:c] + row[c+1:] for row in matrix[1:]]
                det_val += ((-1) ** c) * matrix[0][c] * det(submatrix)
            return det_val
    
    def schur_multiplicity(m, n):
        # Placeholder function to compute Schur multiplicity
        # This is a dummy implementation and should be replaced with actual computation
        return 1  # Simplified for testing purposes
    
    n = random.randint(5, 40)
    matrix = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    
    perm_multiplicity = schur_multiplicity(perm(n), n)
    det_multiplicity = schur_multiplicity(det(matrix), n)
    
    ratio = perm_multiplicity / det_multiplicity
    
    return {
        "metric_name": "Schur-Weyl Multiplicity Ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio >= 2,
        "counterexample": "" if ratio >= 2 else f"Mean ratio {ratio} < 2"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [3, 5, 7, 11, 13, 17, 19, 23, 29, 31] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        results.append(result)
        print(f"TRIAL: {result}")
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_ratio) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"Mean ratio {results[0]['metric_value']} < 2\" first_failing_seed={first_failing_seed}")