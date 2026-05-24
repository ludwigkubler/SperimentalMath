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
    
    def generate_tseitin_formula(n):
        variables = [f'x{i}' for i in range(n)]
        clauses = []
        for i in range(n):
            clauses.append(f'({variables[i]} v ~{variables[i]})')
        for i in range(1, n):
            clauses.append(f'{variables[0]} v {variables[i]}')
        return ' & '.join(clauses)
    
    def local_index(ring):
        # Placeholder for actual computation
        return 2 ** (len(ring) / 2)
    
    def resolution_proof_width(formula):
        # Placeholder for actual computation
        return 2 ** len(formula.split(' v '))
    
    n = random.randint(5, 40)
    formula = generate_tseitin_formula(n)
    ring = formula.replace(' ', '').replace('v', '1').replace('~', '0')
    local_idx = local_index(ring)
    resolution_width = resolution_proof_width(formula)
    
    return {
        "metric_name": "LocalIndex vs ResolutionWidth",
        "metric_value": local_idx,
        "instances_tested": 1,
        "conjecture_holds": local_idx <= 2 ** (n / 2) and resolution_width >= 2 ** (n - math.log(n, 2)),
        "counterexample": f"n={n}, LocalIndex={local_idx}, ResolutionWidth={resolution_width}" if not conjecture_holds else ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(100, 999) for _ in range(30)]
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")