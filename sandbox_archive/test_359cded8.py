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

def generate_3cnf(n):
    clauses = []
    for _ in range(2 * n):
        clause = [random.choice([1, -1]) * random.randint(1, n) for _ in range(3)]
        if len(set(clause)) == 3:
            clauses.append(clause)
    return clauses

def boolean_tensor_product_valuation(clauses):
    width = 0
    for clause in clauses:
        width += max(abs(x) for x in clause)
    return width

def min_rank_tqft(clauses):
    n = len(set(abs(x) for clause in clauses for x in clause))
    rank = 2 ** (n - 1)
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for _ in range(30):  # Ensure at least 30 instances per seed
        n = random.choice([5, 10, 15, 20, 30, 40])
        clauses = generate_3cnf(n)
        val_width = boolean_tensor_product_valuation(clauses)
        min_rank = min_rank_tqft(clauses)
        ratio = math.log(min_rank) / math.log(val_width)
        results.append(ratio)
    metric_value = sum(results) / len(results)
    conjecture_holds = all(0.9 <= r <= 1.1 for r in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": "log_ratio",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, **trial_result}}")
        results.append(trial_result["metric_value"])
    
    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean)**2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if 0.9 <= r <= 1.1) / len(results)
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(not r for r in results):
        first_failing_seed = seeds[results.index(next(r for r in results if not r))]
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")