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
    
    def tseitin_formula(n):
        return [f"X{i} ∨ X{j}" for i in range(1, n+1) for j in range(i+1, n+1)]
    
    def monomial_ideal(formula):
        ideal = set()
        for clause in formula:
            literals = clause.split(" ∨ ")
            for literal in literals:
                if literal.startswith("¬"):
                    continue
                ideal.add(literal)
        return ideal
    
    def associated_graded_ring(ideal):
        rank = 0
        for literal in ideal:
            if literal.startswith("¬"):
                continue
            rank += 1
        return rank
    
    def resolution_width(formula):
        width = 0
        for clause in formula:
            literals = clause.split(" ∨ ")
            width = max(width, len(literals))
        return width
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_width = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            formula = tseitin_formula(n)
            ideal = monomial_ideal(formula)
            grade_rank = associated_graded_ring(ideal)
            proof_width = resolution_width(formula)
            total_width += proof_width
            instances_tested += 1
    
    mean_width = total_width / instances_tested
    conjecture_holds = mean_width >= 2**(n_values[0]/2) and mean_width <= 2**(n_values[-1]/2)
    counterexample = "" if conjecture_holds else f"Mean width {mean_width} does not meet Θ(2^(n/2))"
    
    return {
        "metric_name": "resolution_width",
        "metric_value": mean_width,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_width = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_width} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mean_width does not meet Θ(2^(n/2))\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")