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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def frege_proof_depth(cnf):
        # Simplified Frege proof depth simulation
        return len(cnf) * 2
    
    def hodge_theoretic_index(cnf):
        # Placeholder for Hodge-theoretic index calculation
        # For simplicity, we use the number of clauses as a proxy
        return len(cnf)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        cnf = generate_cnf(n)
        h_index = hodge_theoretic_index(cnf)
        d_depth = frege_proof_depth(cnf)
        results.append({"n": n, "h_index": h_index, "d_depth": d_depth})
    
    if not results:
        return {
            "metric_name": "Hodge-theoretic Index vs Frege Proof Depth",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    h_values = [r["h_index"] for r in results]
    d_values = [r["d_depth"] for r in results]
    
    mean_h = sum(h_values) / len(h_values)
    mean_d = sum(d_values) / len(d_values)
    std_h = math.sqrt(sum((x - mean_h) ** 2 for x in h_values) / len(h_values))
    std_d = math.sqrt(sum((x - mean_d) ** 2 for x in d_values) / len(d_values))
    
    correlation = sum((h_values[i] - mean_h) * (d_values[i] - mean_d) for i in range(len(h_values))) / (len(h_values) * std_h * std_d)
    
    c = 1.0
    k = 5
    
    conjecture_holds = all(h >= d for h, d in zip(h_values, d_values)) and all(h <= c * d ** 2 for h, d in zip(h_values, d_values) if d >= k)
    
    return {
        "metric_name": "Hodge-theoretic Index vs Frege Proof Depth",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no seeds tested")