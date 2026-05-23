# auto-injected by SEC sandbox
import math
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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_formula(n):
        return ''.join(random.choice('01') for _ in range(2**n - 1))
    
    def schur_polynomial_representation(formula):
        # Placeholder function to simulate Schur polynomial representation
        return len(formula) % 3
    
    def dpll_search_tree_width(formula):
        # Placeholder function to simulate DPLL search tree width
        return len(formula) // 2
    
    n = random.randint(5, 40)
    formula = generate_boolean_formula(n)
    schur_rank = schur_polynomial_representation(formula)
    dpll_width = dpll_search_tree_width(formula)
    
    return {
        "metric_name": "Schur Rank vs DPLL Width",
        "metric_value": schur_rank,
        "instances_tested": 1,
        "conjecture_holds": schur_rank == dpll_width,
        "counterexample": f"Schur Rank: {schur_rank}, DPLL Width: {dpll_width}" if schur_rank != dpll_width else ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result_type = "SUPPORTED"
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = Fraction(sum(1 for r in results if r["conjecture_holds"]), len(results))
        result_type = "FALSIFIED" if first_failing_seed is not None else "INCONCLUSIVE"
    
    print(f"RESULT: {result_type} mean={mean_value} std=0 support_fraction={support_fraction}")