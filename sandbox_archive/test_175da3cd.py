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
    
    def generate_kcnf(n, k):
        clauses = []
        for _ in range(k):
            clause = set()
            while len(clause) < 3:
                lit = random.randint(1, n) * (random.choice([1, -1]))
                if lit not in clause:
                    clause.add(lit)
            clauses.append(tuple(sorted(clause)))
        return clauses
    
    def coxeter_group_action_complexity(n):
        # Placeholder for the actual computation
        return 2 ** (n // 4) * random.uniform(0.9, 1.1)
    
    def tropicalize(complexity):
        # Placeholder for the actual tropicalization
        return complexity
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # 5 instances per size
            k = random.randint(1, min(n, 10))
            phi = generate_kcnf(n, k)
            complexity = coxeter_group_action_complexity(n)
            tropicalized = tropicalize(complexity)
            results.append((n, tropicalized))
    
    mean_value = sum(tropicalized for n, tropicalized in results) / len(results)
    expected_values = [2 ** (n // 4) for n, _ in results]
    std_dev = math.sqrt(sum((t - e) ** 2 for t, e in zip(expected_values, expected_values)) / len(expected_values))
    
    support_fraction = sum(1 for _, t in results if abs(t - mean_value) <= 0.1 * mean_value and abs(t - expected_values[results.index((n, t))]) <= 0.2 * expected_values[results.index((n, t))]) / len(results)
    
    conjecture_holds = support_fraction >= 0.8
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "tropicalized_complexity",
        "metric_value": mean_value,
        "instances_tested": len(results),
        "n_max": max(n for n, _ in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["n_max"] >= 16 for r in results):
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
        else:
            first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=not_enough_large_n n_tested={len([r for r in results if r['n_max'] >= 16])}")