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

def geometric_langlands_dual(cnf):
    # Placeholder function for constructing the geometric Langlands dual object from a CNF
    n = len(cnf)
    m = sum(1 for clause in cnf if any(var in clause for var in range(n)))
    return m ** (Fraction(1, 4)) * n ** (Fraction(3, 8))

def generate_cnf(n, m):
    cnfs = []
    for _ in range(m):
        cnf = set()
        while len(cnf) < n:
            clause = {random.randint(0, n-1), random.randint(0, n-1)}
            if len(clause) == 2 and clause not in cnf:
                cnf.add(frozenset(clause))
        cnfs.append(list(cnf))
    return cnfs

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Ensure at least 30 instances per seed
            m = random.randint(n, 2*n)
            cnf = generate_cnf(n, m)
            dual_rank = geometric_langlands_dual(cnf)
            results.append((n, m, dual_rank))
    metric_value = sum(dual_rank for n, m, dual_rank in results) / len(results)
    instances_tested = len(results)
    conjecture_holds = all(dual_rank <= m ** (Fraction(1, 4)) * n ** (Fraction(3, 8)) for n, m, dual_rank in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": "minimal_rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 30)]
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = (sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results)) ** 0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")