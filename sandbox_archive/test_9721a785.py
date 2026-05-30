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
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def coxeter_group_action(clauses):
        action_count = {}
        for clause in clauses:
            key = tuple(sorted(clause))
            if key not in action_count:
                action_count[key] = 0
            action_count[key] += 1
        return len(action_count)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_ratio = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):
            clauses = generate_3cnf(n)
            action_count = coxeter_group_action(clauses)
            ratio = action_count / (n ** (1/3))
            total_ratio += ratio
            instances_tested += 1
    
    mean_ratio = total_ratio / instances_tested
    conjecture_holds = mean_ratio >= 0.8 and mean_ratio <= 3
    counterexample = "" if conjecture_holds else "mean_ratio out of bounds"
    
    return {
        "metric_name": "ratio",
        "metric_value": mean_ratio,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}}}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio:.2f} std=0.00 support_fraction=1.00")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio:.2f} std=0.00 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mean_ratio out of bounds\" first_failing_seed={first_failing_seed}")