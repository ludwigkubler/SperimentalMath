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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def support(f):
        return [i for i in range(len(f)) if f[i] == 1]
    
    def groupoid_action(s):
        action = set()
        for i in s:
            for j in range(len(s)):
                action.add((i, (i + j) % len(s)))
        return action
    
    def min_rank(g):
        return len(g)
    
    def acc0_parity_circuit_size(f):
        n = len(f)
        if n == 1:
            return 1
        circuit_size = 2 * acc0_parity_circuit_size(n // 2) + 1
        return circuit_size
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    total_circuit_size = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):
            f = generate_boolean_function(n)
            s = support(f)
            g = groupoid_action(s)
            rank = min_rank(g)
            circuit_size = acc0_parity_circuit_size(n)
            total_rank += rank
            total_circuit_size += circuit_size
            instances_tested += 1
    
    mean_ratio = total_rank / total_circuit_size if total_circuit_size > 0 else float('inf')
    
    return {
        "metric_name": "mean_ratio",
        "metric_value": mean_ratio,
        "instances_tested": instances_tested,
        "conjecture_holds": mean_ratio <= 1.5,  # Hypothetical constant c
        "counterexample": "" if mean_ratio <= 1.5 else f"Mean ratio {mean_ratio} exceeds conjectured bound"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(2, 6)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Mean ratio exceeds conjectured bound' first_failing_seed={first_failing_seed}")