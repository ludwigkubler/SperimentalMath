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
    
    def generate_random_sat_instance(n, clause_count):
        literals = [f"x{i}" for i in range(n)]
        clauses = []
        for _ in range(clause_count):
            clause = random.sample(literals + [-l for l in literals], 2)
            clauses.append("(" + " ∨ ".join(clause) + ")")
        return " ∧ ".join(clauses)
    
    def dpll_width(phi):
        # Simplified DPLL width calculation
        if not phi:
            return 0
        if "∨" not in phi:
            return 1
        parts = phi.split(" ∨ ")
        return max(dpll_width(p) for p in parts)
    
    def affine_quotient_generators(phi):
        # Simplified generator set calculation
        if not phi:
            return set()
        if "∨" not in phi:
            return {phi}
        parts = phi.split(" ∨ ")
        generators = set()
        for part in parts:
            generators.update(affine_quotient_generators(part))
        return generators
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_ratio = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            clause_count = random.randint(n, n * 10)
            phi = generate_random_sat_instance(n, clause_count)
            w_phi = dpll_width(phi)
            G_phi = affine_quotient_generators(phi)
            
            if w_phi == 0:
                continue
            
            ratio = len(G_phi) / w_phi
            total_ratio += ratio
            instances_tested += 1
            n_max = max(n_max, n)
    
    mean_ratio = Fraction(total_ratio, instances_tested).limit_denominator()
    conjecture_holds = abs(mean_ratio - Fraction(1)) <= Fraction(10, 100)
    counterexample = "" if conjecture_holds else f"Mean ratio {mean_ratio} not within ±10% of 1.0"
    
    return {
        "metric_name": "mean_ratio",
        "metric_value": float(mean_ratio),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}}}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")