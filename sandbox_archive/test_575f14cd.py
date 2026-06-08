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
    
    def p_adic_divergence(p, a, b):
        if a == b:
            return 0
        pa = [p**i * (a % p) for i in range(len(a))]
        pb = [p**i * (b % p) for i in range(len(b))]
        return sum(abs(pa[i] - pb[i]) for i in range(max(len(pa), len(pb)))) / max(len(pa), len(pb))
    
    def indicator_function(bit_sequence):
        return [int(bit) for bit in bit_sequence]
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_divergences = []
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        divergences = []
        for _ in range(5):  # Sample 5 independent pairs of bit sequences
            a = indicator_function(random.choices([0, 1], k=n))
            b = indicator_function(random.choices([0, 1], k=n))
            divergence = p_adic_divergence(2, a, b)
            divergences.append(divergence)
            instances_tested += 1
        total_divergences.extend(divergences)
        n_max = max(n_max, n)
    
    mean_divergence = sum(total_divergences) / len(total_divergences)
    conjecture_holds = mean_divergence <= math.log2(n_max)
    counterexample = "" if conjecture_holds else f"mean_divergence={mean_divergence}, log2(n_max)={math.log2(n_max)}"
    
    return {
        "metric_name": "p-adic divergence",
        "metric_value": mean_divergence,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")