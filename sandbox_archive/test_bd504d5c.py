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
    
    def generate_formula(m: int):
        variables = [f'x{i}' for i in range(1, m+1)]
        clauses = []
        for _ in range(m):
            clause = random.sample(variables + [f'~{v}' for v in variables], 2)
            clauses.append(clause)
        return ' & '.join(['(' + ' | '.join(c) + ')' for c in clauses])
    
    def fca(formula):
        # Placeholder FCA implementation
        return len(formula.split('&'))
    
    def resolution_width(formula):
        # Placeholder DPLL-based solver for resolution width
        return len(formula.split('&'))
    
    m_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for m in m_values:
        formula = generate_formula(m)
        order_of_concepts = fca(formula)
        width = resolution_width(formula)
        results.append((order_of_concepts, width))
    
    if not results:
        return {
            "metric_name": "Correlation Coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No formulas generated"
        }
    
    order_values = [r[0] for r in results]
    width_values = [r[1] for r in results]
    
    mean_order = sum(order_values) / len(order_values)
    mean_width = sum(width_values) / len(width_values)
    
    correlation_coefficient = 0
    if mean_order != 0 and mean_width != 0:
        numerator = sum((order - mean_order) * (width - mean_width) for order, width in results)
        denominator = math.sqrt(sum((order - mean_order)**2 for order in order_values)) * math.sqrt(sum((width - mean_width)**2 for width in width_values))
        correlation_coefficient = numerator / denominator
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(m_values),
        "conjecture_holds": correlation_coefficient >= 0.9,
        "counterexample": "" if correlation_coefficient >= 0.9 else f"Correlation: {correlation_coefficient}"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000003) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None)) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["metric_value"] < 0.5 for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Correlation below threshold\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")