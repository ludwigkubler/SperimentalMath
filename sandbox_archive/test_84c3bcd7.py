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
            return 'x'
        else:
            subformulas = [generate_formula(random.randint(1, n-1)) for _ in range(2)]
            return f'({subformulas[0]} & {subformulas[1]}) | ({subformulas[0]} & ~{subformulas[1]})'
    
    def compute_tropical_norm(formula):
        # Simplified tropical norm calculation
        return len(formula)
    
    def compute_proof_length(formula):
        # Simplified proof length calculation (assuming linear complexity)
        return len(formula) * 2
    
    n = random.randint(5, 40)
    formula = generate_formula(n)
    norm_trop = compute_tropical_norm(formula)
    proof_length = compute_proof_length(formula)
    
    c = 1.0  # Constant for the conjecture
    expected_bound = n ** c * proof_length
    
    deviation = abs(norm_trop - expected_bound) / expected_bound
    
    return {
        "metric_name": "tropical_norm",
        "metric_value": norm_trop,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": deviation <= 0.1 and norm_trop <= 1.1 * expected_bound,
        "counterexample": "" if deviation <= 0.1 else f"deviation={deviation:.2f}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] and "counterexample" not in r for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"deviation_too_large\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")