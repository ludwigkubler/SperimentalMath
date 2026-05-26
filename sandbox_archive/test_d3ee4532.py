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
    
    def generate_bp(n):
        size = 2 ** n
        bp = [[random.randint(0, 1) for _ in range(size)] for _ in range(size)]
        return bp
    
    def entropy(p):
        p = [x / sum(p) for x in p if x > 0]
        return -sum(x * math.log2(x) for x in p)
    
    def free_entropy(bp):
        n = len(bp)
        size = len(bp[0])
        entropies = []
        for i in range(size):
            row_entropies = [entropy(row[i::size]) for row in bp]
            entropies.append(sum(row_entropies) / n)
        return sum(entropies) / n
    
    def log2_size(bp):
        size = len(bp[0])
        return math.log2(size)
    
    O_n = lambda n: 1.5 * n  # Simplified O(n) term for demonstration purposes
    
    max_diff = -float('inf')
    instances_tested = 0
    support_count = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Test each size 5 times to gather enough data
            bp = generate_bp(n)
            F_P = free_entropy(bp)
            log2_size_value = log2_size(bp)
            O_n_value = O_n(n)
            diff = abs(F_P - (log2_size_value + O_n_value))
            
            if diff > max_diff:
                max_diff = diff
                counterexample = f"n={n}, F(P)={F_P}, log2(size)= {log2_size_value}, O(n)={O_n_value}"
            else:
                counterexample = ""
            
            instances_tested += 1
            if diff <= 3:
                support_count += 1
    
    conjecture_holds = support_count / instances_tested >= 0.9 and max_diff <= 10
    
    return {
        "metric_name": "free_entropy",
        "metric_value": max_diff,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, **result}}")
        results.append(result)
    
    mean_value = sum(r['metric_value'] for r in results) / len(results)
    std_value = math.sqrt(sum((r['metric_value'] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in results) and max_diff <= 10:
        first_failing_seed = next(i for i, r in enumerate(results) if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={seeds[first_failing_seed]}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence_or_budget_exceeded n_tested=30")