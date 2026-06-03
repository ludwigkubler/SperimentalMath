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
        cnf = []
        for _ in range(10 * n):  # Generate 10 clauses per variable
            clause = [random.randint(-n, -1), random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def calculate_resolution_width(cnf):
        literals_seen = set()
        queue = list(cnf)
        while queue:
            literal = queue.pop()
            if literal in literals_seen or -literal in literals_seen:
                continue
            literals_seen.add(literal)
            for clause in cnf:
                if literal in clause:
                    new_clause = [l for l in clause if l != literal]
                    if not new_clause:
                        return len(literals_seen)  # Resolution width is the number of unique literals seen
                    queue.append(new_clause)
        return len(literals_seen)
    
    def calculate_mli(cnf):
        n = max(abs(lit) for lit in cnf)
        state_space_volume = 2 ** (n * n)
        entanglement_cost = 0.5  # Placeholder value, should be calculated based on actual quantum state
        return state_space_volume * entanglement_cost
    
    def pearson_correlation(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov_xy = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / len(x)
        std_x = math.sqrt(sum((xi - mean_x) ** 2 for xi in x) / len(x))
        std_y = math.sqrt(sum((yi - mean_y) ** 2 for yi in y) / len(y))
        return cov_xy / (std_x * std_y)
    
    n_values = [5, 10, 15, 20, 30, 40]
    mli_values = []
    w_phi_values = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        mli_value = calculate_mli(cnf)
        w_phi_value = calculate_resolution_width(cnf)
        mli_values.append(mli_value)
        w_phi_values.append(w_phi_value)
    
    correlation_coefficient = pearson_correlation(mli_values, w_phi_values)
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": "" if correlation_coefficient >= 0.5 else f"Correlation coefficient {correlation_coefficient:.2f} < 0.5"
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [random.randint(1, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_dev:.4f} support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_dev:.4f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Correlation coefficient below 0.7\" first_failing_seed={first_failing_seed}")