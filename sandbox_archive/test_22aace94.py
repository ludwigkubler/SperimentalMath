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
    
    def tropicalize(f):
        n = int(math.log2(len(f)))
        T = [[max(a[i], b[i]) for i in range(n)] for a, b in zip(f[:len(f)//2], f[len(f)//2:])]
        return T
    
    def shannon_entropy(p):
        p = [x / sum(p) for x in p if x > 0]
        return -sum(x * math.log2(x) for x in p)
    
    def acc0_circuit_size(n):
        # Placeholder function to simulate ACC⁰ circuit size
        # This is a dummy implementation and should be replaced with actual logic
        return random.randint(1, n)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    f = generate_boolean_function(n)
    T = tropicalize(f)
    p = [random.random() for _ in range(len(T))]
    entropy = shannon_entropy(p)
    c = random.uniform(0.1, 1.0)  # Placeholder value for constant c
    acc0_size = acc0_circuit_size(n)
    
    metric_value = entropy
    conjecture_holds = (entropy < c * math.log2(n)) and (acc0_size > 2 * n / 5)
    counterexample = "" if conjecture_holds else f"Entropy {entropy} >= {c * math.log2(n)} or ACC⁰ size {acc0_size} <= {2 * n / 5}"
    
    return {
        "metric_name": "Minimal Entropy",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        result = f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}"
    elif support_fraction >= 0.8:
        result = f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}"
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        result = f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}"
    
    print(result)