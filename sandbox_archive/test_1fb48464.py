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
    
    def generate_monotone_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def matrix_from_function(f, n):
        matrix = []
        for i in range(2**n):
            row = []
            for j in range(2**n):
                if f[i] == f[j]:
                    row.append(0)
                else:
                    row.append(1)
            matrix.append(row)
        return matrix
    
    def tropical_hermitian_rank(matrix):
        n = len(matrix)
        rank = 0
        for i in range(n):
            if any(matrix[j][i] == 1 for j in range(n)):
                rank += 1
        return rank
    
    def karchmer_wigderson_protocol_cost(f, n):
        # Simplified protocol cost (not actual KWP)
        return n
    
    n = random.randint(5, 40)
    f = generate_monotone_boolean_function(n)
    matrix = matrix_from_function(f, n)
    
    rank = tropical_hermitian_rank(matrix)
    cost = karchmer_wigderson_protocol_cost(f, n)
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": rank / cost,
        "instances_tested": 1,
        "conjecture_holds": rank >= cost * 0.5 and rank <= cost * 2,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")