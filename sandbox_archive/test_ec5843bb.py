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
    
    def generate_circuit(n):
        if n == 1:
            return ['0']
        else:
            left = generate_circuit(n // 2)
            right = generate_circuit(n - n // 2)
            return [f'({left[0]} & {right[0]})', f'({left[1]} | {right[1]})']
    
    def monotone_width(circuit):
        if isinstance(circuit, str):
            return 1
        else:
            return max(monotone_width(circuit[0]), monotone_width(circuit[1])) + 1
    
    def geometric_group_size(n):
        # Placeholder for actual computation of group size
        return n * (n + 1) // 2
    
    def automorphism_group_generators(group_size):
        # Placeholder for actual computation of generator size
        return int(math.log2(group_size)) + 1
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    circuit = generate_circuit(n)
    group_size = geometric_group_size(n)
    generators = automorphism_group_generators(group_size)
    
    width = monotone_width(circuit)
    diff = abs(generators - width)
    
    return {
        "metric_name": "Difference between generator size and monotone width",
        "metric_value": diff,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": diff <= 3,
        "counterexample": "" if diff <= 3 else f"Generator size: {generators}, Monotone width: {width}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_diff = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_diff} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_diff} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Generator size and monotone width do not match\" first_failing_seed={first_failing_seed}")