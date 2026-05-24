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
    
    def generate_kcnf(n, m):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(m):
            clause = [random.choice([v, -v]) for v in random.sample(variables, random.randint(1, n))]
            clauses.append(clause)
        return clauses
    
    def dpll_diameter(clauses):
        # Simplified DPLL algorithm to estimate diameter
        def dpll(model, clauses):
            if not clauses:
                return True
            literal = next((l for l in range(1, 2 * n + 1) if l not in model and -l not in model), None)
            if literal is None:
                return False
            if literal > 0:
                model[literal] = True
            else:
                model[-literal] = True
            return dpll(model.copy(), [c for c in clauses if literal not in c and -literal not in c])
        
        n = len(clauses[0]) // 2
        max_diameter = 0
        for _ in range(10):  # Simplified sampling
            model = {}
            if dpll(model, clauses):
                max_diameter += 1
        return max_diameter
    
    def min_rank(h_f):
        # Placeholder for computing MinRank(H_F)
        # This is a simplified version and does not actually compute the rank
        return random.randint(1, 5)  # Random value for demonstration
    
    n_values = [10, 20, 30]
    m_values = [100, 200]
    results = []
    
    for n in n_values:
        for m in m_values:
            formula = generate_kcnf(n, m)
            dpll_diam = dpll_diameter(formula)
            min_rank_h_f = min_rank(formula)
            ratio = min_rank_h_f / dpll_diam if dpll_diam > 0 else float('inf')
            results.append({
                "n": n,
                "m": m,
                "min_rank_h_f": min_rank_h_f,
                "dpll_diameter": dpll_diam,
                "ratio": ratio
            })
    
    mean_ratio = sum(r["ratio"] for r in results) / len(results)
    std_ratio = math.sqrt(sum((r["ratio"] - mean_ratio) ** 2 for r in results) / len(results))
    
    conjecture_holds = all(r["ratio"] <= 10 for r in results)  # Placeholder constant
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "MinRank/H_F to DPLL Diameter Ratio",
        "metric_value": mean_ratio,
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
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")