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
        total_weight = sum(G[i][j] for i in range(n) for j in range(i+1, n))
        min_balls = float('inf')
        for k in range(1, n + 1):
            balls = [sum(G[i][j] for j in range(i+1, n)) for i in range(k)]
            if sum(balls) >= total_weight:
                min_balls = k
                break
        return math.log2(min_balls)
    
    def compute_resolution_width(f):
        # Simplified DPLL solver to estimate resolution width
        clauses = []
        for i in range(len(f)):
            clause = [i + 1 if f[i] == 0 else -(i + 1)]
            clauses.append(clause)
        
        def dpll(model, clauses):
            if not clauses:
                return True
            unit_clause = next((c for c in clauses if len(c) == 1), None)
            if unit_clause:
                literal = unit_clause[0]
                model[abs(literal)] = literal > 0
                new_clauses = [c for c in clauses if literal not in c and -literal not in c]
                return dpll(model, new_clauses)
            pure_literal = next((l for l in range(1, len(f) + 1) if (l not in model and -l not in model)), None)
            if pure_literal:
                model[pure_literal] = True
                new_clauses = [c for c in clauses if pure_literal not in c and -pure_literal not in c]
                return dpll(model, new_clauses)
            literal = random.choice([1, 2])
            model[literal] = True
            new_clauses = [c for c in clauses if literal not in c and -literal not in c]
            if dpll(model, new_clauses):
                return True
            del model[literal]
            model[-literal] = True
            new_clauses = [c for c in clauses if literal not in c and -literal not in c]
            return dpll(model, new_clauses)
        
        width = 0
        while not dpll({}, clauses):
            width += 1
        return width
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        G = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        Hmin_Gf = compute_geometric_entropy(G)
        w_f = compute_resolution_width(f)
        results.append((n, Hmin_Gf, w_f))
    
    if not results:
        return {
            "metric_name": "resolution_width",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    Hmin_values = [H for _, H, _ in results]
    w_f_values = [w for _, _, w in results]
    
    mean_Hmin = sum(Hmin_values) / len(Hmin_values)
    mean_w_f = sum(w_f_values) / len(w_f_values)
    std_Hmin = math.sqrt(sum((H - mean_Hmin)**2 for H in Hmin_values) / len(Hmin_values))
    std_w_f = math.sqrt(sum((w - mean_w_f)**2 for w in w_f_values) / len(w_f_values))
    
    correlation_coefficient = sum((Hmin_values[i] - mean_Hmin) * (w_f_values[i] - mean_w_f) for i in range(len(results))) / (len(results) * std_Hmin * std_w_f)
    
    return {
        "metric_name": "resolution_width",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": 0.2 <= correlation_coefficient <= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [random.randint(1, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(r["metric_value"] < 0.2 for r in results):
        first_failing_seed = next((r["seed"] for r in results if r["metric_value"] < 0.2), None)
        print(f"RESULT: FALSIFIED counterexample=\"low_correlation\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support")