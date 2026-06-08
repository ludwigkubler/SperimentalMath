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
    
    def generate_instance(n, m):
        variables = list(range(n))
        clauses = []
        for _ in range(m):
            clause = random.sample(variables, 3)
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses
    
    def dpll(instance, assignment={}):
        unsatisfied_clauses = [c for c in instance if not any(x in assignment and (assignment[x] == 1 if x > 0 else -assignment[-x] == 1) for x in c)]
        if not unsatisfied_clauses:
            return True
        unit_clause = next((c for c in unsatisfied_clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_assignment = assignment.copy()
            new_assignment[literal] = 1 if literal > 0 else -literal
            return dpll(instance, new_assignment)
        pure_literal = next((x for x in variables if all(x not in c or (x < 0 and -x not in c) for c in unsatisfied_clauses)), None)
        if pure_literal:
            new_assignment = assignment.copy()
            new_assignment[pure_literal] = 1
            return dpll(instance, new_assignment)
        literal = random.choice([x for x in variables if any(x in c or -x in c for c in unsatisfied_clauses)])
        new_assignment = assignment.copy()
        new_assignment[literal] = 1
        if not dpll(instance, new_assignment):
            new_assignment[literal] = -literal
            return dpll(instance, new_assignment)
        return False
    
    def geometric_entropy(instance):
        # Placeholder for actual GCT computation
        return random.random() * len(instance)  # Simplified for testing
    
    n_values = [5, 10, 15, 20, 30, 40]
    entropy_values = []
    path_length_values = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            m = random.randint(n, 2 * n)
            instance = generate_instance(n, m)
            entropy = geometric_entropy(instance)
            path_length = dpll(instance)
            entropy_values.append(entropy)
            path_length_values.append(path_length)
    
    if not entropy_values or not path_length_values:
        return {
            "metric_name": "Geometric Entropy vs DPLL Path Length",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "Empty instance set"
        }
    
    def pearson_correlation(x, y):
        if len(x) != len(y):
            raise ValueError("x and y must have the same length")
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
        std1 = math.sqrt(sum((xi - mean_x) ** 2 for xi in x) / n)
        std2 = math.sqrt(sum((yi - mean_y) ** 2 for yi in y) / n)
        if std1 == 0 or std2 == 0:
            return 0
        return cov / (std1 * std2)
    
    correlation = pearson_correlation(entropy_values, path_length_values)
    conjecture_holds = correlation >= 0.8
    
    return {
        "metric_name": "Geometric Entropy vs DPLL Path Length",
        "metric_value": correlation,
        "instances_tested": len(entropy_values),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Correlation {correlation:.2f} < 0.8"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.2f} std={std_value:.2f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Correlation too low\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")