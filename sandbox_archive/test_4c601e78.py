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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(c == 0 for c in clause):
                continue
            clauses.append(clause)
        return clauses
    
    def resolution_width(clauses):
        queue = list(clauses)
        seen = set()
        while queue:
            literal, rest = queue.pop(0)
            seen.add(literal)
            new_clauses = []
            for clause in rest:
                if -literal in clause:
                    new_clause = [l for l in clause if l != -literal]
                    if not new_clause:
                        return len(queue) + 1
                    new_clauses.append(new_clause)
                else:
                    new_clauses.append(clause)
            queue.extend(new_clauses)
        return float('inf')
    
    def hopf_algebra_rank(cnf):
        # Simplified rank calculation for demonstration purposes
        return sum(len(set(abs(l) for l in clause)) for clause in cnf)
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    min_rank = hopf_algebra_rank(cnf)
    w_phi = resolution_width(cnf)
    
    if w_phi == float('inf'):
        return {
            "metric_name": "min_rank_to_w_ratio",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "resolution_width_infinite"
        }
    
    ratio = min_rank / w_phi
    return {
        "metric_name": "min_rank_to_w_ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": 0.5 <= ratio <= 2 and abs(ratio - 1) <= 1,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_ratio = math.sqrt(sum((r["metric_value"] - mean_ratio)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if 0.5 <= r["metric_value"] <= 2 and abs(r["metric_value"] - 1) <= 1) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"min_rank_to_w_ratio_out_of_bounds\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")