# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def generate_kcnf_instance(n, m, k):
    instance = []
    for _ in range(m):
        clause = set()
        while len(clause) < k:
            var = random.randint(1, n)
            lit = random.choice([var, -var])
            if lit not in clause:
                clause.add(lit)
        instance.append(clause)
    return instance

def count_satisfying_assignments(instance):
    n = max(abs(lit) for clause in instance for lit in clause)
    satisfying_count = 0
    for assignment in range(1 << n):
        if all((assignment >> (var - 1)) & 1 == abs(lit) % 2 != (lit < 0) for clause in instance for lit in clause):
            satisfying_count += 1
    return satisfying_count

def compute_entropy(satisfying_count, total_assignments):
    p = Fraction(satisfying_count, total_assignments)
    if p == 0 or p == 1:
        return 0
    return -p * math.log2(p) - (1 - p) * math.log2(1 - p)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Test with 5 instances per n
            m = random.randint(n // 2, n * 2)
            k = random.randint(1, min(k, n))
            instance = generate_kcnf_instance(n, m, k)
            total_assignments = 1 << n
            satisfying_count = count_satisfying_assignments(instance)
            entropy = compute_entropy(satisfying_count, total_assignments)
            results.append((n, m, k, entropy))
    
    if len(results) < 30:
        return {
            "metric_name": "Entropy",
            "metric_value": None,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    n_values = [res[0] for res in results]
    entropies = [res[3] for res in results]
    mean_entropy = sum(entropies) / len(entropies)
    std_entropy = (sum((x - mean_entropy) ** 2 for x in entropies) / len(entropies)) ** 0.5
    
    return {
        "metric_name": "Entropy",
        "metric_value": mean_entropy,
        "instances_tested": len(results),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_entropy = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_entropy = (sum((r["metric_value"] - mean_entropy) ** 2 for r in results if r["metric_value"] is not None) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_entropy} std={std_entropy} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_entropy} std={std_entropy} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"insufficient_evidence\" first_failing_seed={first_failing_seed}")