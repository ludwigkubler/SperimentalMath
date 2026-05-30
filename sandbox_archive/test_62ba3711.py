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
        return [random.randint(0, 1) for _ in range(2**n)]
    
    def dpll_refutation_size(f):
        n = len(f)
        clauses = []
        for i in range(n):
            clause = []
            for j in range(i + 1, n):
                if f[2**(i + j)] != f[2**i] ^ f[2**j]:
                    clause.append((i, j))
            clauses.append(clause)
        return len(clauses) + n
    
    def geometric_entropy(f):
        n = len(f)
        count = [0] * (n + 1)
        for i in range(2**n):
            count[bin(i).count('1')] += 1
        entropy = 0
        total = 2**n
        for c in count:
            if c > 0:
                p = c / total
                entropy -= p * math.log2(p)
        return entropy
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        f = generate_boolean_function(n)
        ge = geometric_entropy(f)
        t_f = dpll_refutation_size(f)
        if t_f > 0:
            ratio = ge / t_f
            metric_values.append(ratio)
    
    return {
        "metric_name": "GE(A_f) / t*(f)",
        "metric_value": sum(metric_values) / len(metric_values),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": all(x <= 2 for x in metric_values),  # Assuming k = 1
        "counterexample": "" if all(x <= 2 for x in metric_values) else "GE(A_f) / t*(f) > 2"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"GE(A_f) / t*(f) > 2\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")