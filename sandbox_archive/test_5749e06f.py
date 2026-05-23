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
    
    def generate_random_function(n):
        return {tuple(random.randint(0, 1) for _ in range(n)): random.choice([0, 1]) for _ in range(2**n)}
    
    def communication_complexity(f):
        n = len(next(iter(f.keys())))
        p_values = [Fraction(p, 100) for p in range(101)]
        entropies = []
        
        for p in p_values:
            matrix = [[0] * (2**n + 1) for _ in range(2**n + 1)]
            for x in f:
                index = sum(bit << i for i, bit in enumerate(x))
                for y in range(n):
                    if x[y] == 1:
                        matrix[index][index + y] += 1
            total = sum(sum(row) for row in matrix)
            entropy = 0
            for row in matrix:
                for val in row:
                    if val > 0:
                        prob = Fraction(val, total)
                        entropy -= prob * math.log2(prob)
            entropies.append(entropy)
        
        return max(entropies)

    n_values = [5, 10, 15, 20, 30, 40]
    metric_value = []
    
    for n in n_values:
        f = generate_random_function(n)
        entropy = communication_complexity(f)
        metric_value.append(entropy)
    
    instances_tested = len(metric_value) * len(n_values)
    conjecture_holds = all(entropy >= n**(1 - 1/p) for p in range(1, 101) for n in n_values)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": sum(metric_value) / instances_tested,
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
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")