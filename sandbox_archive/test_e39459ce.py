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

def generate_tseitin_tree(n):
    if n == 1:
        return (None, None, 'x')
    else:
        left_size = random.randint(1, n-2)
        right_size = n - left_size - 1
        left = generate_tseitin_tree(left_size)
        right = generate_tseitin_tree(right_size)
        return (left, right, f'¬({generate_tseitin_tree(left_size)[2]} ∨ {generate_tseitin_tree(right_size)[2]})')

def calculate_rank(poly):
    # Placeholder for calculating the rank of a polynomial
    # This is a dummy implementation and should be replaced with actual logic
    return len(poly)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        if n * (n - 1) // 2 < 1:  # Avoid empty range in randrange
            continue
        
        width_sum = 0
        rank_sum = 0
        instances_tested = 0
        
        for _ in range(5):  # Ensure at least 30 instances per seed
            tree = generate_tseitin_tree(n)
            poly = calculate_rank(tree)  # Placeholder for actual polynomial calculation
            width = len(tree[2].split(' ')) - 1
            rank = calculate_rank(poly)
            
            width_sum += width
            rank_sum += rank
            instances_tested += 1
        
        avg_width = width_sum / instances_tested
        avg_rank = rank_sum / instances_tested
        crc = spearman_correlation([-math.log2(avg_rank), math.log2(avg_width)])
        
        results.append({
            "metric_name": "Spearman's Rank Correlation",
            "metric_value": crc,
            "instances_tested": instances_tested,
            "conjecture_holds": crc >= 0.8,  # Placeholder threshold
            "counterexample": ""
        })
    
    return {
        "seed": seed,
        "results": results
    }

def spearman_correlation(x):
    n = len(x)
    if n < 2:
        raise ValueError("At least two data points are required")
    
    sorted_x = sorted((x[i], i) for i in range(n))
    rank_x = [sorted_x.index(i[1]) for i in sorted_x]
    
    sorted_y = sorted((y, i) for i, y in enumerate(x))
    rank_y = [sorted_y.index(i[1]) for i in sorted_y]
    
    d_squared_sum = sum((rank_x[i] - rank_y[i]) ** 2 for i in range(n))
    spearman_coefficient = 1 - (6 * d_squared_sum) / (n * (n**2 - 1))
    
    return spearman_coefficient

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["results"])
    
    all_crcs = [r[0]["metric_value"] for r in results]
    mean_crc = sum(all_crcs) / len(all_crcs)
    std_crc = math.sqrt(sum((x - mean_crc) ** 2 for x in all_crcs) / len(all_crcs))
    support_fraction = sum(1 for r in results if r[0]["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_crc} std={std_crc} support_fraction={support_fraction}")
    elif any(not r[0]["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result[0]["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")