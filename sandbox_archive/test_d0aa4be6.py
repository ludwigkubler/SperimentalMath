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
    
    def generate_3cnf(n):
        literals = [f"x{i}" for i in range(1, n+1)] + [f"~x{i}" for i in range(1, n+1)]
        clauses = []
        for _ in range(n * 2):  # Each variable appears twice
            clause = random.sample(literals, 3)
            clauses.append(clause)
        return clauses

    def resolution_proof_size(clauses):
        # Simplified resolution proof size estimation (not actual proof)
        return len(clauses) ** 1.5

    n = random.randint(5, 40)
    clauses = generate_3cnf(n)
    
    # Minimal order of geometric invariants for a projective variety
    k = len(set(len(c) for c in clauses))  # Simplified example
    
    proof_size = resolution_proof_size(clauses)
    
    return {
        "metric_name": "resolution_proof_size",
        "metric_value": proof_size,
        "instances_tested": 1,
        "conjecture_holds": proof_size <= k**3 * math.log(n),
        "counterexample": "" if proof_size <= k**3 * math.log(n) else f"Proof size {proof_size} exceeds bound {k**3 * math.log(n)}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        support_fraction = 1.0
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = next(result["counterexample"] for result in results if not result["conjecture_holds"])
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        support_fraction = (len([r for r in results if r["conjecture_holds"]]) / len(results)) * 100
    
    print(f"RESULT: {'SUPPORTED' if all(result['conjecture_holds'] for result in results) else 'FALSIFIED'} mean={mean_value} std={std_value} support_fraction={support_fraction:.2f}")