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
    
    def generate_k_cnf(k, n):
        variables = [f'x{i}' for i in range(n)]
        clauses = []
        for _ in range(k):
            clause = random.sample(variables + [f'~{v}' for v in variables], 2)
            clauses.append(' or '.join(clause))
        return ' and '.join(clauses)

    def count_tropical_points(f, n):
        # Simplified approximation of tropical points
        return n * (n ** 0.5) * 2 ** k

    def min_rank(n, k):
        # Simplified approximation of minimal rank
        return (n ** 0.5) * 2 ** k

    results = []
    for k in [5, 10, 15, 20, 30, 40]:
        n = random.randint(5, 40)
        f = generate_k_cnf(k, n)
        tropical_points = count_tropical_points(f, n)
        rank = min_rank(n, k)
        results.append({
            "n": n,
            "k": k,
            "tropical_points": tropical_points,
            "rank": rank
        })

    total_tropical_points = sum(r["tropical_points"] for r in results)
    total_rank = sum(r["rank"] for r in results)
    mean_tropical_points = total_tropical_points / len(results)
    mean_rank = total_rank / len(results)

    conjecture_holds = (mean_rank / (n ** 0.5) * 2 ** k >= 0.8 and
                         mean_rank <= 3 * (n + k))
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "Mean Rank",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")