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
    
    # Parameters for k-CNF generation
    n = 10  # Number of variables
    m = 2 * n  # Number of clauses (2 literals per clause)
    k = 3  # Clause length
    
    # Generate a random k-CNF formula φ with n variables and m clauses
    phi = []
    for _ in range(m):
        clause = set(random.sample(range(1, n + 1), k))
        phi.append(clause)
    
    # Convert the k-CNF to a list of literals
    literals = [0] * (n + 1)
    for clause in phi:
        for literal in clause:
            literals[literal] += 1
    
    # Calculate the resolution proof width w(φ)
    def dpll(phi):
        if not phi:
            return 0
        unit_clauses = [c for c in phi if len(c) == 1]
        if not unit_clauses:
            return max(dpll([c - {l} for c in phi if l not in c]) for l in literals if literals[l] > 0)
        literal, _ = unit_clauses[0]
        new_phi = [c - {literal} for c in phi if literal not in c]
        return 1 + dpll(new_phi)
    
    w_phi = dpll(phi)
    
    # Calculate the minimal Hodge index H(φ) (simplified example)
    H_phi = sum(literals[l] ** 2 for l in range(1, n + 1))
    
    # Check the inequality log2(n^(k+1)) ≤ w(φ) + H(φ)
    lhs = math.log2(n ** (k + 1))
    rhs = w_phi + H_phi
    
    conjecture_holds = lhs <= rhs
    counterexample = "" if conjecture_holds else f"lhs={lhs}, rhs={rhs}"
    
    return {
        "metric_name": "resolution_proof_width",
        "metric_value": w_phi,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    # Compute mean/std of metric_value
    total_metric_value = sum(r["metric_value"] for r in results)
    mean_metric_value = total_metric_value / len(results)
    variance = sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results)
    std_metric_value = math.sqrt(variance)
    
    # Compute fraction of seeds where conjecture_holds
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    # Determine the final result
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")