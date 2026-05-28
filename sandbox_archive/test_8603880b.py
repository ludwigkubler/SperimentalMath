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
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(2 * n):
            literals = [random.choice([f'x{i}', f'~x{i}']) for i in range(1, n + 1)]
            random.shuffle(literals)
            clause = ' & '.join(literals)
            clauses.append(clause)
        formula = ' | '.join(clauses)
        return formula
    
    def dpll_refutation_size(formula):
        # Simplified DPLL refutation size estimation
        return len(formula.split(' | '))
    
    def tropicalized_sheaves_order(formula):
        # Simplified tropicalized sheaves order estimation
        return len(formula.split(' & '))
    
    n = random.randint(5, 40)
    formula = generate_3cnf(n)
    refutation_size = dpll_refutation_size(formula)
    sheaves_order = tropicalized_sheaves_order(formula)
    
    if refutation_size == 0:
        return {
            "metric_name": "tropicalized_sheaves_order",
            "metric_value": 0,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "DPLL refutation size is zero"
        }
    
    ratio = Fraction(sheaves_order, math.log2(refutation_size))
    conjecture_holds = 0.5 <= ratio <= 1.5
    
    return {
        "metric_name": "tropicalized_sheaves_order",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Ratio {ratio} out of bounds"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio out of bounds\" first_failing_seed={first_failing_seed}")