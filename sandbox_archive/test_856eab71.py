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
    
    def generate_cnf(n, k):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(k):
            clause = [random.choice(variables), -random.choice(variables)]
            clauses.append(clause)
        return clauses
    
    def entropy(clauses):
        unique_clauses = set(tuple(sorted(c)) for c in clauses)
        total_clauses = len(clauses)
        counts = {c: clauses.count(c) for c in unique_clauses}
        probabilities = [count / total_clauses for count in counts.values()]
        return -sum(p * math.log2(p) for p in probabilities if p > 0)
    
    def mli(clauses):
        n = len(set(abs(v) for clause in clauses for v in clause))
        k = len(clauses)
        return (n ** k) / (k + 1)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            clauses = generate_cnf(n, random.randint(1, 2 * n))
            ent = entropy(clauses)
            mli_val = mli(clauses)
            results.append({"n": n, "mli": mli_val, "ent": ent})
    
    if not results:
        return {
            "metric_name": "mli_vs_entropy",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mli_values = [r["mli"] for r in results]
    ent_values = [r["ent"] for r in results]
    mean_mli = sum(mli_values) / len(mli_values)
    mean_ent = sum(ent_values) / len(ent_values)
    correlation = sum((mli_values[i] - mean_mli) * (math.log2(ent_values[i]) - mean_ent) for i in range(len(mli_values))) / len(mli_values)
    
    return {
        "metric_name": "mli_vs_entropy",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": abs(correlation) >= 0.8 and all(abs(mli_val - math.log2(ent_val)) <= 3 for mli_val, ent_val in zip(mli_values, ent_values)),
        "counterexample": ""
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
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")