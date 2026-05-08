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
    
    def generate_ac0_formula(n):
        # Generate a random monotone AC⁰ formula for n variables
        formula = []
        for _ in range(2**n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            formula.append(clause)
        return formula
    
    def compute_communication_matrix(formula, n):
        # Compute the communication matrix for the given formula
        C = [[0] * n for _ in range(n)]
        for clause in formula:
            for x in range(2**n):
                if all((x >> i) & 1 == abs(clause[i]) for i in range(n)):
                    for y in range(2**n):
                        if all((y >> i) & 1 == abs(clause[i]) for i in range(n)):
                            C[x // (2**(n//2))][y // (2**(n//2))] += 1
        return C
    
    def count_monochromatic_rectangles(C, n):
        # Count monochromatic rectangles in the communication matrix
        count = 0
        for i in range(n):
            for j in range(i+1, n):
                for k in range(n):
                    for l in range(k+1, n):
                        if (C[i][k] + C[j][l]) == (n // 2) * 4:
                            count += 1
        return count
    
    n = random.randint(5, 40)
    formula = generate_ac0_formula(n)
    C = compute_communication_matrix(formula, n)
    rectangle_count = count_monochromatic_rectangles(C, n)
    
    metric_name = "monochromatic_rectangle_count"
    metric_value = rectangle_count
    instances_tested = 1
    conjecture_holds = rectangle_count >= n
    counterexample = "" if conjecture_holds else f"Formula size {len(formula)}, n={n}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.2f} std={std_value:.2f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Formula size {len(results[0]['counterexample'])}, n={n}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")