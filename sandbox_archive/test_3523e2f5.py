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
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            # Find the pivot
            max_row = i
            for r in range(i + 1, rows):
                if abs(matrix[r][i]) > abs(matrix[max_row][i]):
                    max_row = r
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            
            # Eliminate below the pivot
            for r in range(i + 1, rows):
                factor = Fraction(matrix[r][i], matrix[i][i])
                for c in range(cols):
                    matrix[r][c] -= factor * matrix[i][c]
        
        rank = sum(1 for row in matrix if any(row))
        return rank
    
    def construct_tropical_graph(n, s):
        inputs = [(i // 2, i % 2) for i in range(n)]
        outputs = [random.randint(-100, 100) for _ in range(n)]
        
        E = []
        for i in range(s):
            if len(inputs) < 2:
                break
            a, b = random.sample(inputs, 2)
            inputs.remove(a)
            inputs.remove(b)
            E.append((a, b))
        
        return E
    
    n = 10
    s = 5
    G = construct_tropical_graph(n, s)
    
    rank = gaussian_elimination(G)
    
    metric_value = rank / (s * math.log(n))
    instances_tested = 1
    conjecture_holds = rank <= s * math.log(n)
    counterexample = "" if conjecture_holds else "rank too high"
    
    return {
        "metric_name": "Rank of Tropical Graph",
        "metric_value": metric_value,
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
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank too high\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")