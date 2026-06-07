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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_geometric_entropy(G):
        n = len(G)
        if n == 0:
            return 0
        total_edges = sum(sum(row) for row in G)
        max_edges = n * (n - 1) // 2
        return math.log(total_edges / max_edges, 2)
    
    def compute_resolution_width(f):
        # Simplified DPLL solver to estimate resolution width
        clauses = []
        for i in range(len(f)):
            clause = [i + 1 if f[i] == 0 else -i - 1]
            clauses.append(clause)
        
        def dpll(model, clauses):
            if not clauses:
                return True
            unit_clause = next((c for c in clauses if len(c) == 1), None)
            if unit_clause:
                literal = unit_clause[0]
                model[literal] = literal > 0
                new_clauses = [c for c in clauses if literal not in c and -literal not in c]
                return dpll(model, new_clauses)
            
            literal = next((i + 1 for i in range(len(f)) if i + 1 not in model), None)
            model[literal] = True
            if dpll(model, clauses):
                return True
            del model[literal]
            model[-literal] = False
            return dpll(model, clauses)
        
        max_width = 0
        for literal in range(1, len(f) + 1):
            model = {literal: None}
            if dpll(model, clauses):
                width = sum(1 for k, v in model.items() if v is not None)
                max_width = max(max_width, width)
        return max_width
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        G = [[f[i] ^ f[j] for j in range(n)] for i in range(n)]
        Hmin = compute_geometric_entropy(G)
        w_f = compute_resolution_width(f)
        results.append({"n": n, "Hmin": Hmin, "w_f": w_f})
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    Hmin_values = [r["Hmin"] for r in results]
    w_f_values = [r["w_f"] for r in results]
    
    def correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = math.sqrt(sum((x[i] - mean_x)**2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y)**2 for i in range(n)) / n)
        return cov / (std_x * std_y) if std_x * std_y != 0 else 0
    
    corr_coeff = correlation(Hmin_values, w_f_values)
    
    return {
        "metric_name": "correlation",
        "metric_value": corr_coeff,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": 0.2 < corr_coeff < 0.8,
        "counterexample": "" if 0.2 < corr_coeff < 0.8 else f"correlation={corr_coeff}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_corr = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result = f"SUPPORTED mean={mean_corr} std=0 support_fraction={support_fraction}"
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        result = f"FALSIFIED counterexample=\"correlation out of bounds\" first_failing_seed={first_failing_seed}"
    else:
        result = "INCONCLUSIVE"
    
    print(result)