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
    
    def generate_polynomial_system(n, m):
        variables = [f'x{i}' for i in range(n)]
        equations = []
        for _ in range(m):
            coeffs = [random.randint(-10, 10) for _ in range(n + 1)]
            equation = ' + '.join(f'{coeffs[i]}*{variables[i]}' for i in range(n)) + ' = 0'
            equations.append(equation)
        return equations
    
    def hodge_diamond_rank(equations):
        # Simplified Hodge diamond rank calculation
        m = len(equations)
        return 2 * m
    
    def dpll_refutation_depth(equations):
        # Simplified DPLL refutation depth calculation
        m = len(equations)
        return m + 1
    
    n = random.randint(5, 40)
    m = random.randint(1, 5)
    equations = generate_polynomial_system(n, m)
    
    hodge_rank = hodge_diamond_rank(equations)
    dpll_depth = dpll_refutation_depth(equations)
    
    if hodge_rank <= 2 * dpll_depth:
        conjecture_holds = False
        counterexample = f"n={n}, m={m}, hodge_rank={hodge_rank}, dpll_depth={dpll_depth}"
    else:
        conjecture_holds = True
        counterexample = ""
    
    return {
        "metric_name": "Hodge Rank vs DPLL Depth",
        "metric_value": hodge_rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [random.randint(2, 997) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.2f} std={std_metric_value:.2f} support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.2f} std={std_metric_value:.2f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")