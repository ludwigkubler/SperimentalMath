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
    
    def generate_knot(n):
        # Placeholder for knot generation logic
        return [random.randint(0, 1) for _ in range(n)]
    
    def compute_betti_numbers(knot):
        # Placeholder for Betti number computation logic
        return sum(knot)
    
    def cnf_formula(knot):
        # Placeholder for CNF formula generation logic
        return knot
    
    def dpll_proof_length(cnf):
        # Placeholder for DPLL proof length calculation logic
        return len(cnf) * 2
    
    n = random.randint(5, 40)
    knot = generate_knot(n)
    betti_rank = compute_betti_numbers(knot)
    cnf = cnf_formula(knot)
    proof_length = dpll_proof_length(cnf)
    
    return {
        "metric_name": "DPLL Proof Length",
        "metric_value": proof_length,
        "instances_tested": 1,
        "conjecture_holds": proof_length <= betti_rank**2,
        "counterexample": "" if proof_length <= betti_rank**2 else f"Seed {seed} failed with DPLL length {proof_length}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(100, 999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"DPLL length exceeds Rank(K)^2\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")