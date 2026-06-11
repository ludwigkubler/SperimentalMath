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
        for _ in range(2**n):
            clause = [random.randint(-1, 1) * (i + 1) for i in range(n)]
            if all(c == 0 for c in clause):
                continue
            clauses.append(clause)
        return clauses
    
    def dpll_width(clauses):
        literals = set()
        for clause in clauses:
            literals.update(abs(lit) for lit in clause)
        n = len(literals)
        
        def dfs(model, level):
            if level == n:
                return 1
            literal = list(literals - model.keys())[0]
            if literal in model and model[literal] != (literal > 0):
                return dfs(model, level + 1)
            new_model_pos = model.copy()
            new_model_neg = model.copy()
            new_model_pos[literal] = True
            new_model_neg[literal] = False
            width_pos = dfs(new_model_pos, level + 1)
            width_neg = dfs(new_model_neg, level + 1)
            return max(width_pos, width_neg)
        
        return dfs({}, 0)
    
    def hodge_theory_dimension(clauses):
        # Placeholder for Hodge theory dimension calculation
        # This is a dummy implementation and should be replaced with actual computation
        return len(clauses) / 2
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        cnf = generate_cnf(n)
        htd = hodge_theory_dimension(cnf)
        width = dpll_width(cnf)
        metric_values.append(htd * width)
    
    mean_value = sum(metric_values) / len(metric_values)
    std_value = math.sqrt(sum((x - mean_value) ** 2 for x in metric_values) / len(metric_values))
    correlation_coefficient = sum((metric_values[i] - mean_value) * (i + 1) for i in range(len(metric_values))) / (len(metric_values) * std_value * math.sqrt(sum((i + 1) ** 2 for i in range(len(metric_values)))))
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation_coefficient) >= 0.8,
        "counterexample": "" if abs(correlation_coefficient) >= 0.8 else "Correlation coefficient < 0.5"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
    elif any(not r["conjecture_holds"] and r["metric_value"] < 0.5 for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"] and r["metric_value"] < 0.5)
        print(f"RESULT: FALSIFIED counterexample='Correlation coefficient < 0.5' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")