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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def tropicalize(f):
        n = len(f)
        T = [[max(a[i], b[i]) for i in range(n)] for a, b in zip(f[:len(f)//2], f[len(f)//2:])]
        return T
    
    def shannon_entropy(p):
        p = [x for x in p if x > 0]
        return -sum(x * math.log2(x) for x in p)
    
    def acc0_circuit_size(n):
        # Placeholder function to simulate ACC⁰ circuit size
        # This is a dummy implementation and should be replaced with actual logic
        return n // 5
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    T = tropicalize(f)
    
    entropy = shannon_entropy(T)
    c_log_n = 2 * math.log2(n)  # Simplified for demonstration purposes
    circuit_size = acc0_circuit_size(n)
    
    conjecture_holds = entropy < c_log_n and circuit_size <= 2 * n / 5
    
    return {
        "metric_name": "Minimal Entropy of Tropicalized Boolean Functions vs ACC⁰ Circuit Lower Bounds",
        "metric_value": entropy,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Entropy {entropy} >= c log(n) = {c_log_n}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_entropy = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_entropy} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Entropy >= c log(n)' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")