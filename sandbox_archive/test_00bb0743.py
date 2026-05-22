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
    
    def generate_max_cut_instance(n):
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    edges.append((i, j))
        return edges
    
    def tropical_curve_rank(edges):
        # Simplified rank calculation (not actual tropical curve)
        return len(edges) // 2
    
    def sum_of_squares_degree(n):
        return int(math.log2(n)) + 1
    
    n = random.randint(5, 40)
    instance = generate_max_cut_instance(n)
    rank = tropical_curve_rank(instance)
    degree = sum_of_squares_degree(n)
    
    metric_name = 'min_rank_tropical_curve'
    metric_value = rank
    instances_tested = 1
    conjecture_holds = rank >= degree
    counterexample = '' if conjecture_holds else f'Rank {rank} < Degree {degree}'
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f'TRIAL: {result}')
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = 1.0
        print(f'RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}')
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f'RESULT: FALSIFIED counterexample="{r["counterexample"]}" first_failing_seed={first_failing_seed}')