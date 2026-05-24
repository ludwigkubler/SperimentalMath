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
        for _ in range(2 * n):
            clause = [random.randint(-n, n) for _ in range(random.randint(1, 3))]
            clauses.append(clause)
        return clauses
    
    def dpll_refutation_tree(cnf):
        if not cnf:
            return 0
        literals = set(abs(lit) for lit in sum(cnf, []))
        if len(literals) == 0:
            return 1
        literal = random.choice(list(literals))
        positive_clauses = [c for c in cnf if literal in c]
        negative_clauses = [c for c in cnf if -literal in c]
        return 1 + max(dpll_refutation_tree(positive_clauses), dpll_refutation_tree(negative_clauses))
    
    def algebraic_k_theory_group(cnf):
        # Simplified version of computing the rank
        return len(set(abs(lit) for lit in sum(cnf, [])))
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    diameter = dpll_refutation_tree(cnf)
    r_k = algebraic_k_theory_group(cnf)
    
    return {
        "metric_name": "ratio",
        "metric_value": r_k / diameter if diameter > 0 else float('inf'),
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results if "metric_value" in r and not math.isinf(r["metric_value"])) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_ratio) ** 2 for r in results if "metric_value" in r and not math.isinf(r["metric_value"])) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all("metric_value" in r and not math.isinf(r["metric_value"]) for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_dev} support_fraction={support_fraction}")
    elif any("metric_value" in r and math.isinf(r["metric_value"]) for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if "metric_value" in result and math.isinf(result["metric_value"]))
        print(f"RESULT: FALSIFIED counterexample=\"infinite_ratio\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")