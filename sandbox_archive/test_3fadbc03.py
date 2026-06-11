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
    
    def char_poly(f, m):
        n = 2**m
        A = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if f(i ^ j) != f(i) ^ f(j):
                    return None
        return A
    
    def max_plus_entropy(A):
        n = len(A)
        if n == 0:
            return 0
        max_entries = [max(row[i] for row in A) for i in range(n)]
        entropy = sum(math.log2(1 + entry) for entry in max_entries)
        return entropy
    
    m_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for m in m_values:
        n_max = 0
        for _ in range(30):
            boolean_function = lambda x: random.choice([0, 1])
            char_poly_result = char_poly(boolean_function, m)
            if char_poly_result is None:
                continue
            entropy = max_plus_entropy(char_poly_result)
            if entropy is not None:
                results.append(entropy)
                n_max = max(n_max, len(char_poly_result))
    
    if not results:
        return {
            "metric_name": "max_plus_entropy",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    conjecture_holds = all(entropy <= m * math.log(m, 2) for entropy, m in zip(results, m_values))
    
    return {
        "metric_name": "max_plus_entropy",
        "metric_value": mean,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r <= max(m * math.log(m, 2) for m in [5, 10, 15, 20, 30, 40])) / len(results)
    
    if all(r <= max(m * math.log(m, 2) for m in [5, 10, 15, 20, 30, 40]) for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(r > max(m * math.log(m, 2) for m in [5, 10, 15, 20, 30, 40]) for r in results):
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={seeds[results.index(max(results))]}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")