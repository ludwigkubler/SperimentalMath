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

def is_boolean_ring(R):
    for x in R:
        if not (x == 0 or x == 1):
            return False
    return True

def min_rank_K(R):
    if not is_boolean_ring(R):
        return None
    n = len(R)
    rank_A = sum(1 for i in range(n) if R[i] == 1)
    rank_B = sum(1 for j in range(n) if R[j] == 0)
    return min(rank_A, rank_B)

def tseitin_formula(R):
    n = len(R)
    formula = []
    for i in range(n):
        formula.append(f"(x{i} OR x{i+1})")
    formula.append(f"NOT (x{n-1} AND x{n})")
    return " AND ".join(formula)

def resolution_length(formula):
    clauses = formula.split(" AND ")
    resolvents = []
    while True:
        new_resolvents = set()
        for i in range(len(clauses)):
            for j in range(i+1, len(clauses)):
                clause_i = clauses[i].split(" OR ")
                clause_j = clauses[j].split(" OR ")
                for literal_i in clause_i:
                    if "NOT" + literal_i in clause_j:
                        new_resolvent = [l for l in clause_i if l != literal_i] + [l for l in clause_j if l != "NOT" + literal_i]
                        new_resolvents.add(" OR ".join(new_resolvent))
        if not new_resolvents:
            break
        resolvents.update(new_resolvents)
        clauses.extend(new_resolvents)
    return len(resolvents)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    R = [random.choice([0, 1]) for _ in range(n)]
    rank_K = min_rank_K(R)
    if rank_K is None:
        return {
            "metric_name": "Resolution Proof Length",
            "metric_value": float('inf'),
            "instances_tested": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    formula = tseitin_formula(R)
    proof_length = resolution_length(formula)
    return {
        "metric_name": "Resolution Proof Length",
        "metric_value": proof_length,
        "instances_tested": n,
        "conjecture_holds": proof_length >= 2 ** rank_K,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [random.randint(2, 1000003) for _ in range(30)]
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")