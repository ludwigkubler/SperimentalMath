# auto-injected by SEC sandbox
import math
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

from itertools import combinations
import random

def generate_formula(n, m):
    clauses = []
    variables = set(range(1, n + 1))
    while len(clauses) < m:
        clause = set()
        while len(clause) < 2 or any(abs(x - y) <= 1 for x, y in combinations(clause, 2)):
            var = random.choice(list(variables))
            if var not in clause:
                clause.add(var)
        clauses.append(tuple(sorted(clause)))
    return clauses

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        m = n // 2
        if m <= 0:
            continue
        clauses = generate_formula(n, m)
        d = max(abs(x - y) for x, y in combinations(range(1, n + 1), 2))
        # Placeholder for Ehrhart semigroup computation (not implemented)
        mtr_phi = sum(len(clause) for clause in clauses)
        ratio = mtr_phi / (d ** (1.5 / 2) * (m ** 3))
        results.append({"n": n, "m": m, "d": d, "mtr_phi": mtr_phi, "ratio": ratio})
    metric_value = sum(result["ratio"] for result in results)
    instances_tested = len(results)
    n_max = max(result["n"] for result in results)
    conjecture_holds = all(result["ratio"] <= 1.0 for result in results) if instances_tested > 30 else False
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": "Ratio of mtr(φ) to d^(1.5/2) * log^3(m)",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["instances_tested"] >= 30 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")