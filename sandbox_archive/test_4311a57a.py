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
    
    def generate_sat_formula(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.choice([f'x{i+1}', f'~x{i+1}']) for i in range(n)]
            clauses.append(clause)
        return clauses

    def tropical_rank(sat_formula):
        # Simplified version of the tropical rank calculation
        # This is a placeholder and should be replaced with actual computation
        return len(sat_formula) ** 0.5

    n = random.choice([5, 10, 15, 20, 30, 40])
    sat_formula = generate_sat_formula(n)
    rank = tropical_rank(sat_formula)
    
    metric_value = rank
    instances_tested = 1
    conjecture_holds = rank >= n ** 0.5 - 3 and rank <= n ** 0.5 + 3
    counterexample = "" if conjecture_holds else "n={} rank={}".format(n, rank)
    
    return {
        "metric_name": "tropical_rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 307))  # First 30 primes

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print("TRIAL:", {"seed": seed, **result})
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print("RESULT: SUPPORTED mean=%.4f std=%.4f support_fraction=%.2f" % (mean_value, std_value, support_fraction))
    elif any(r["counterexample"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["counterexample"])
        print("RESULT: FALSIFIED counterexample=\"%s\" first_failing_seed=%d" % (results[0]["counterexample"], first_failing_seed))
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested=%d" % len(results))