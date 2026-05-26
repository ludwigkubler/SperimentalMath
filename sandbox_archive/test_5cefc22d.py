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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def output_complexity(f):
        n = int(math.log2(len(f)))
        count = 0
        for i in range(2**n):
            if f[i] != (i & (i - 1) == 0):  # Check if f(i) is non-zero and not a power of two
                count += 1
        return count
    
    def construct_algebraic_stack(f):
        n = int(math.log2(len(f)))
        F_2_n = [list(range(2)) for _ in range(n)]
        F_2_m = [list(range(2)) for _ in range(len(f))]
        
        # Construct the stack as a list of matrices
        stack = []
        for i in range(2**n):
            matrix = [[random.choice([0, 1]) for _ in range(len(f))] for _ in range(n)]
            stack.append(matrix)
        
        return stack
    
    def rank_of_matrix(matrix):
        m, n = len(matrix), len(matrix[0])
        if m == 0 or n == 0:
            return 0
        
        # Gaussian elimination
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            
            if matrix[i][i] == 0:
                continue
            
            for j in range(i+1, m):
                factor = -matrix[j][i] / matrix[i][i]
                for k in range(n):
                    matrix[j][k] += factor * matrix[i][k]
        
        rank = sum(1 for row in matrix if any(row))
        return rank
    
    def minimal_rank(stack):
        return min(rank_of_matrix(matrix) for matrix in stack)
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    C_f = output_complexity(f)
    stack = construct_algebraic_stack(f)
    min_rank = minimal_rank(stack)
    
    conjecture_holds = min_rank <= 2**C_f
    counterexample = "" if conjecture_holds else "rank_exceeds_bound"
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": min_rank,
        "instances_tested": len(stack),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank_exceeds_bound\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unreachable")