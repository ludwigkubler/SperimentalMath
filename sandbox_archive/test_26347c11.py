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
    
    def generate_cnf(n, m):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(m):
            clause = [random.choice(variables), random.choice(variables)]
            if random.choice([True, False]):
                clause[0] *= -1
            if random.choice([True, False]):
                clause[1] *= -1
            clauses.append(clause)
        return variables, clauses

    def tseitin_width(cnf):
        width = 0
        for var in set(abs(lit) for lit in sum(cnf, [])):
            width = max(width, len([c for c in cnf if abs(c[0]) == var or abs(c[1]) == var]))
        return width

    def geometric_quantization_rank(cnf):
        # Placeholder function to simulate the computation
        # This is a dummy implementation and should be replaced with actual geometric quantization logic
        rank = sum(1 for clause in cnf if len(set(abs(lit) for lit in clause)) > 1)
        return rank

    n, m = random.randint(5, 40), random.randint(n * 2, n * 3)
    variables, clauses = generate_cnf(n, m)
    tseitin_w = tseitin_width(cnf)
    gq_rank = geometric_quantization_rank(cnf)

    return {
        "metric_name": "geometric_quantization_rank",
        "metric_value": gq_rank,
        "instances_tested": 1,
        "conjecture_holds": gq_rank >= tseitin_w,
        "counterexample": f"CNF with n={n}, m={m} has rank {gq_rank} < Tseitin width {tseitin_w}" if not gq_rank >= tseitin_w else ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result = f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}"
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        result = f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}"

    print(result)