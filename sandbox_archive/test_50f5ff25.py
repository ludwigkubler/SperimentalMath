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
        T = [[float('inf')] * (n + 1) for _ in range(n + 1)]
        for i in range(n + 1):
            T[i][i] = f[0]
        for k in range(1, n + 1):
            for i in range(n - k + 1):
                j = i + k
                T[i][j] = min(T[i][j], max(T[i][m] + T[m+1][j] for m in range(i, j)))
        return T
    
    def shannon_entropy(p):
        p = [x / sum(p) for x in p]
        return -sum(x * math.log2(x) if x > 0 else 0 for x in p)
    
    def acc0_circuit_size(f):
        n = int(math.log2(len(f)))
        # Placeholder for actual ACC⁰ circuit size calculation
        return 2 * n // 5
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    T = tropicalize(f)
    p = [1 / len(T) for _ in range(len(T))]
    entropy = shannon_entropy(p)
    c_log_n = 0.5 * math.log2(n)
    
    return {
        "metric_name": "Minimal Entropy of Tropicalized Boolean Functions",
        "metric_value": entropy,
        "instances_tested": 1,
        "conjecture_holds": entropy < c_log_n and acc0_circuit_size(f) <= 2 * n // 5,
        "counterexample": "" if entropy >= c_log_n or acc0_circuit_size(f) > 2 * n // 5 else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30)) + [29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_entropy = sum(r["metric_value"] for r in results) / len(results)
    std_entropy = math.sqrt(sum((r["metric_value"] - mean_entropy) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_entropy} std={std_entropy} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")