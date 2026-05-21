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
    
    def walsh_hadamard_transform(f):
        n = len(f)
        if n == 1:
            return f
        even_part = walsh_hadamard_transform([f[i] for i in range(0, n, 2)])
        odd_part = walsh_hadamard_transform([f[i] for i in range(1, n, 2)])
        result = [0] * n
        for k in range(n // 2):
            result[k] = even_part[k] + odd_part[k]
            result[k + n // 2] = even_part[k] - odd_part[k]
        return result
    
    def norm_l1(f):
        return sum(abs(x) for x in f)
    
    def generate_bp(n, w):
        layers = []
        for _ in range(w):
            layer = {}
            for i in range(2 * n):
                if i not in layer:
                    layer[i] = random.choice([0, 1])
            layers.append(layer)
        return layers
    
    def simulate_bp(bp, input_):
        current_state = 0
        for bit in input_:
            current_state = bp[current_state][bit]
        return current_state
    
    n_values = [6, 8, 10, 12, 14]
    w_values = [2, 3, 4]
    instances_tested = 0
    total_norm_l1 = 0
    support_count = 0
    
    for n in n_values:
        for w in w_values:
            size = 2 * n * w + 2
            for _ in range(30):
                bp = generate_bp(n, w)
                truth_table = [simulate_bp(bp, input_) for input_ in range(1 << n)]
                f_hat = walsh_hadamard_transform(truth_table)
                norm_l1_value = norm_l1(f_hat)
                instances_tested += 1
                total_norm_l1 += norm_l1_value
                if norm_l1_value <= (size + 1) ** 3:
                    support_count += 1
    
    conjecture_holds = support_count >= 28 * len(n_values) * len(w_values)
    mean_norm_l1 = total_norm_l1 / instances_tested
    std_norm_l1 = math.sqrt(sum((norm_l1_value - mean_norm_l1) ** 2 for norm_l1_value in f_hat) / instances_tested)
    
    return {
        "metric_name": "Fourier L1 Norm",
        "metric_value": mean_norm_l1,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_norm_l1 = sum(r["metric_value"] for r in results) / len(results)
    std_norm_l1 = math.sqrt(sum((r["metric_value"] - mean_norm_l1) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_norm_l1} std={std_norm_l1} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")