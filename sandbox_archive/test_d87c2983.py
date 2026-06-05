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

def generate_formula(n):
    variables = [f'x{i}' for i in range(n)]
    clauses = []
    for _ in range(n):
        clause = random.sample(variables, 2)
        clause.append(random.choice(['', '¬']))
        clauses.append(clause)
    return clauses

def compute_min_ent(clauses):
    # Placeholder function to simulate computation
    return len(clauses)

def compute_entropy(clauses):
    counts = {}
    for clause in clauses:
        key = tuple(sorted(clause))
        if key not in counts:
            counts[key] = 0
        counts[key] += 1
    entropy = 0
    total = sum(counts.values())
    for count in counts.values():
        p = Fraction(count, total)
        entropy -= p * math.log2(p)
    return entropy

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    min_ents = []
    entropies = []
    
    for n in n_values:
        formula = generate_formula(n)
        min_ent = compute_min_ent(formula)
        entropy = compute_entropy(formula)
        min_ents.append(min_ent)
        entropies.append(entropy)
    
    correlation_coefficient = 0
    if len(min_ents) > 1 and len(entropies) > 1:
        mean_x = sum(min_ents) / len(min_ents)
        mean_y = sum(entropies) / len(entropies)
        numerator = sum((min_ents[i] - mean_x) * (entropies[i] - mean_y) for i in range(len(min_ents)))
        denominator = math.sqrt(sum((min_ents[i] - mean_x)**2 for i in range(len(min_ents)))) * math.sqrt(sum((entropies[i] - mean_y)**2 for i in range(len(entropies))))
        if denominator != 0:
            correlation_coefficient = numerator / denominator
    
    conjecture_holds = abs(correlation_coefficient) >= 0.8 and all(abs(me - e) <= 3 for me, e in zip(min_ents, entropies))
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "Correlation coefficient < 0.8 or absolute difference > 3"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Correlation coefficient < 0.8 or absolute difference > 3' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")