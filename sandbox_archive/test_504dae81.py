# auto-injected by SEC sandbox
import math
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction
from itertools import combinations

def calculate_groupoid_morphisms(f):
    n = len(f)
    m_n = 0
    for i in range(n):
        for j in range(i + 1, n):
            if f[i] == f[j]:
                m_n += 1
    return m_n

def calculate_communication_complexity_rank(f):
    n = len(f)
    rank = 0
    for subset in combinations(range(n), n // 2):
        subsum = sum(f[i] for i in subset)
        if subsum == n // 2:
            rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    metric_name = "Variance Ratio of Communication Complexity Rank"
    instances_tested = 0
    total_variance = 0
    n_max = 5
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        
        for _ in range(5):  # Ensure at least 30 instances per seed
            f = [random.randint(0, 1) for _ in range(n)]
            m_n = calculate_groupoid_morphisms(f)
            rank = calculate_communication_complexity_rank(f)
            
            if m_n == 0:
                continue
            
            instances_tested += 1
            total_variance += (rank - n / 2) ** 2
    
    variance_ratio = Fraction(total_variance, instances_tested * n_max) if instances_tested > 0 else Fraction(0, 1)
    
    conjecture_holds = m_n <= variance_ratio <= m_n
    counterexample = "" if conjecture_holds else f"Variance Ratio: {variance_ratio}, Expected: [m(n), m(n)]"
    
    return {
        "metric_name": metric_name,
        "metric_value": float(variance_ratio),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")