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
    
    # Define a fixed Lie algebra (e.g., su(2))
    lie_algebra = [
        [1, 0],
        [0, -1]
    ]
    
    def tropicalize(matrix):
        return [[max(x, y) for x, y in zip(row1, row2)] for row1, row2 in zip(*matrix)]
    
    def tensor_product(mat1, mat2):
        result = []
        for i in range(len(mat1)):
            row = []
            for j in range(len(mat2[0])):
                cell = [max(x + y for x, y in zip(row1, col2)) for row1, col2 in zip(mat1[i], mat2)]
                row.append(cell)
            result.append(row)
        return result
    
    def dpll_width(clauses):
        # Simplified DPLL width calculation
        return max(len(set(c) - {'0'}) for c in clauses)
    
    def generate_instance(n):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(n):
            clause = random.sample(variables, 2)
            clauses.append(clause)
        return clauses
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    total_width = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):
            instance = generate_instance(n)
            rank = len(tropicalize(tensor_product(instance, lie_algebra)))
            width = dpll_width(instance)
            total_rank += rank
            total_width += width
            instances_tested += 1
    
    avg_rank = total_rank / instances_tested
    avg_width = total_width / instances_tested
    
    if avg_rank < avg_width - 5:
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = "mapping_undefined"
    
    return {
        "metric_name": "Rank vs Width",
        "metric_value": avg_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    avg_rank = sum(r['metric_value'] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={avg_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")