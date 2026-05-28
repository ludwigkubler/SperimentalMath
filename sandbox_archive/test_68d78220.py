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
    
    def generate_xor_function(n):
        return [random.randint(0, 1) for _ in range(n)]
    
    def generate_tropical_curve(n, f):
        curve = []
        for i in range(2**n):
            binary_rep = format(i, '0{}b'.format(n))
            input_vector = list(map(int, binary_rep))
            curve.append(f(input_vector))
        return curve
    
    def communication_complexity(curve):
        n = len(curve)
        total_bits = sum(curve)
        return total_bits / n
    
    def minimal_rank_tropical_curve(curve):
        n = len(curve)
        matrix = []
        for i in range(n):
            row = [curve[j] ^ curve[i] for j in range(n)]
            matrix.append(row)
        
        rank = 0
        for i in range(n):
            if all(matrix[j][i] == 0 for j in range(i, n)):
                continue
            pivot_row = i
            for j in range(i+1, n):
                if abs(matrix[j][i]) > abs(matrix[pivot_row][i]):
                    pivot_row = j
            matrix[i], matrix[pivot_row] = matrix[pivot_row], matrix[i]
            rank += 1
            for j in range(n):
                if i != j:
                    factor = Fraction(matrix[j][i], matrix[i][i])
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[i][k]
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    communication_complexities = []
    ranks = []
    
    for n in n_values:
        f = generate_xor_function(n)
        curve = generate_tropical_curve(n, f)
        comm_comp = communication_complexity(curve)
        rank_val = minimal_rank_tropical_curve(curve)
        
        communication_complexities.append(comm_comp)
        ranks.append(rank_val)
    
    mean_comm_comp = sum(communication_complexities) / len(communication_complexities)
    mean_rank = sum(ranks) / len(ranks)
    diff_mean = abs(mean_comm_comp - mean_rank)
    
    correlation_bound = 0.8
    acceptance_threshold = 3
    
    conjecture_holds = (diff_mean <= acceptance_threshold and 
                        all(corr >= correlation_bound for corr in [comm_comp / rank_val for comm_comp, rank_val in zip(communication_complexities, ranks)]))
    
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Communication Complexity vs Minimal Rank",
        "metric_value": mean_comm_comp,
        "instances_tested": len(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000003) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)
    
    mean_comm_comp = sum(r["metric_value"] for r in results) / len(results)
    std_comm_comp = math.sqrt(sum((r["metric_value"] - mean_comm_comp)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_comm_comp} std={std_comm_comp} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_comm_comp} std={std_comm_comp} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")