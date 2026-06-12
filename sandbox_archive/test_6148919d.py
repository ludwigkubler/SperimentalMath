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
from fractions import Fraction
import math

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_formula(n):
        clauses = []
        for _ in range(random.randint(1, n)):
            clause = [random.choice([True, False]) for _ in range(n)]
            clauses.append(clause)
        return clauses
    
    def clause_tree_depth(clauses):
        if not clauses:
            return 0
        depth = 1 + max([clause_tree_depth([l for l in clauses if l != clause]) for clause in clauses], default=0)
        return depth
    
    def minimal_quandle_rank(clauses):
        n = len(clauses[0])
        quandle = [[False] * n for _ in range(n)]
        for clause in clauses:
            for i in range(n):
                for j in range(i + 1, n):
                    if clause[i] and clause[j]:
                        quandle[i][j] = True
                        quandle[j][i] = True
        rank = 0
        for i in range(n):
            if not any(quandle[i]):
                rank += 1
        return rank
    
    instances_tested = 30
    n_max = 40
    qrank_values = []
    ctdepth_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, 40)
        clauses = generate_formula(n)
        qrank = minimal_quandle_rank(clauses)
        ctdepth = clause_tree_depth(clauses)
        qrank_values.append(qrank)
        ctdepth_values.append(ctdepth)
    
    correlation_coefficient = calculate_correlation(qrank_values, ctdepth_values)
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": "" if correlation_coefficient >= 0.7 else f"Correlation coefficient {correlation_coefficient} < 0.7"
    }

def calculate_correlation(x, y):
    mean_x = sum(x) / len(x)
    mean_y = sum(y) / len(y)
    numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
    denominator = math.sqrt(sum((xi - mean_x) ** 2 for xi in x)) * math.sqrt(sum((yi - mean_y) ** 2 for yi in y))
    return numerator / denominator if denominator != 0 else 0

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")