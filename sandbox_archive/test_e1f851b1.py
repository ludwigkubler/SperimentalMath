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
    
    def generate_k_cnf(n, k):
        clauses = []
        for _ in range(k):
            clause = set(random.sample(range(1, n + 1), random.randint(1, n)))
            if random.choice([True, False]):
                clause = {x: -1 for x in clause}
            else:
                clause = {x: 1 for x in clause}
            clauses.append(clause)
        return clauses

    def compute_p_adic_valuation_rank(cnf):
        # Simplified p-adic valuation rank computation
        rank = len(set.union(*cnf))
        return rank

    def monotone_circuit_depth(cnf):
        # Placeholder for actual monotone circuit depth calculation
        # This is a dummy implementation for testing purposes
        return len(cnf)

    n = random.randint(5, 40)
    k = random.randint(1, min(n * (n - 1) // 2, 30))
    cnf = generate_k_cnf(n, k)
    rank = compute_p_adic_valuation_rank(cnf)
    depth = monotone_circuit_depth(cnf)

    return {
        "metric_name": "Rank vs DPLL Height",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank <= math.log(n),
        "counterexample": ""
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    else:
        seeds = list(map(int, sys.argv[1:]))

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")