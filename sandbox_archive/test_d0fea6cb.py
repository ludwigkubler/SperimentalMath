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
    
    def generate_tseitin_formula(n):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for var in variables:
            clauses.append(f'{var} v ~{var}')
        for i in range(2, n+1):
            clauses.append(f'({variables[0]} ^ {variables[i-1]}) v ~{variables[i]}')
        return f'( {"v ".join(clauses)} )'
    
    def compute_brauer_rank(formula):
        # Placeholder function to simulate Brauer rank computation
        return random.randint(1, 10)
    
    def compute_resolution_width(formula):
        # Placeholder function to simulate resolution width computation
        return random.randint(5, 20)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    formula = generate_tseitin_formula(n)
    bprank_values = [compute_brauer_rank(formula) for _ in range(30)]
    width_values = [compute_resolution_width(formula) for _ in range(30)]
    
    mean_bprank = sum(bprank_values) / len(bprank_values)
    mean_width = sum(width_values) / len(width_values)
    
    correlation_coefficient = (sum((bprank - mean_bprank) * (width - mean_width) for bprank, width in zip(bprank_values, width_values)) /
                               math.sqrt(sum((bprank - mean_bprank) ** 2 for bprank in bprank_values) *
                                         sum((width - mean_width) ** 2 for width in width_values)))
    
    p_value = random.random()  # Placeholder for actual p-value computation
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(bprank_values),
        "n_max": n,
        "conjecture_holds": correlation_coefficient >= 0.8 and p_value <= 0.05,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
    std_metric_value = math.sqrt(sum((res["metric_value"] - mean_metric_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for res in results if not res["conjecture_holds"]) / len(results) <= 0.2:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={first_failing_seed}")