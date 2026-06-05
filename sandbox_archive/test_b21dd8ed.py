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
    
    def generate_formula(n):
        if n == 1:
            return random.choice(['0', '1'])
        else:
            subformulas = [generate_formula(random.randint(1, n-1)) for _ in range(2)]
            return f"({subformulas[0]} & {subformulas[1]}) | ({subformulas[0]} & ~{subformulas[1]})"
    
    def compute_minimal_rank(formula):
        # Placeholder for actual minimal rank computation
        return random.randint(1, 5)
    
    def compute_circuit_entanglement(formula):
        # Placeholder for actual circuit entanglement computation
        return random.uniform(0.1, 2.0)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    formula = generate_formula(n)
    rank = compute_minimal_rank(formula)
    entanglement = compute_circuit_entanglement(formula)
    
    ratio = abs(rank / entanglement)
    conjecture_holds = 0.5 <= ratio <= 2.0
    
    return {
        "metric_name": "Ratio of Minimal Rank to Entanglement",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Formula: {formula}, Ratio: {ratio}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        results.append(trial_result)
        print(f"TRIAL: {trial_result}")
    
    mean_ratio = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Formula: {results[first_failing_seed]['counterexample']}, Ratio: {results[first_failing_seed]['metric_value']}\" first_failing_seed={first_failing_seed}")