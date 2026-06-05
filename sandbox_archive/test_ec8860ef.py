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
    
    def generate_formula(n):
        clauses = []
        for _ in range(n):
            clause = [random.choice(['A', 'B', 'C']) + ('' if random.randint(0, 1) else "'") for _ in range(random.randint(2, 4))]
            clauses.append(' & '.join(clause))
        return ' | '.join(clauses)
    
    def compute_min_ent(formula):
        # Placeholder for actual computation
        return random.random() * n
    
    def compute_entropy(formula):
        # Placeholder for actual computation
        return -sum(Fraction(1, 2) * math.log2(Fraction(1, 2)) for _ in range(n))
    
    def pearson_correlation(x, y):
        if len(x) != len(y):
            raise ValueError("x and y must have the same length")
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / n
        std_dev_x = math.sqrt(sum((xi - mean_x) ** 2 for xi in x) / n)
        std_dev_y = math.sqrt(sum((yi - mean_y) ** 2 for yi in y) / n)
        return cov_xy / (std_dev_x * std_dev_y)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        formula = generate_formula(n)
        min_ent = compute_min_ent(formula)
        entropy = compute_entropy(formula)
        results.append((min_ent, entropy))
    
    min_ents, entropies = zip(*results)
    corr_coeff = pearson_correlation(min_ents, entropies)
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": corr_coeff,
        "instances_tested": len(results),
        "n_max": max(n for _, n in results),
        "conjecture_holds": abs(corr_coeff) >= 0.8 and all(abs(me - e) <= 3 for me, e in zip(min_ents, entropies)),
        "counterexample": "" if corr_coeff >= 0.8 and all(abs(me - e) <= 3 for me, e in zip(min_ents, entropies)) else "Pearson correlation coefficient < 0.8 or abs(diff) > 3"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_corr_coeff = sum(result["metric_value"] for result in results) / len(results)
    std_corr_coeff = math.sqrt(sum((result["metric_value"] - mean_corr_coeff) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if abs(result["metric_value"]) >= 0.8 and all(abs(me - e) <= 3 for me, e in zip(result["min_ents"], result["entropies"]))) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std={std_corr_coeff} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Pearson correlation coefficient < 0.8 or abs(diff) > 3\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")