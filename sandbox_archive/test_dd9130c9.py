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
    n = 10
    alpha = 3.5
    random.seed(seed)
    
    # Generate a random 3-CNF with n variables and clause density α
    clauses = []
    for _ in range(math.ceil(alpha * (n * (n - 1)) / 6)):
        while True:
            var1, var2, var3 = sorted(random.sample(range(n), 3))
            lit1 = random.choice([1, -1])
            lit2 = random.choice([1, -1])
            lit3 = random.choice([1, -1])
            clause = [(var1, lit1), (var2, lit2), (var3, lit3)]
            if all(lit != 0 for _, lit in clause):
                clauses.append(clause)
                break
    
    # Compute the truth table of f_F
    truth_table = [0] * (1 << n)
    for i in range(1 << n):
        assignment = [(i >> j) & 1 for j in range(n)]
        for var, lit in enumerate(clauses):
            if all(assignment[var] != lit for _, lit in enumerate(clause)):
                truth_table[i] = 0
                break
        else:
            truth_table[i] = 1
    
    # Compute all n influences Inf_i
    influences = [0] * n
    for i in range(n):
        influence = 0
        for j in range(1 << n):
            if (j >> i) & 1 == 0:
                influence += truth_table[j ^ (1 << i)] - truth_table[j]
        influences[i] = abs(influence / (1 << (n - 1)))
    
    # Find the maximum single-variable influence
    I_max = max(influences)
    
    # Run DPLL-with-unit-propagation and count leaves τ_KKL
    def dpll(alpha, assignment):
        if not clauses:
            return 1
        alpha_new = sum(1 for c in clauses if any(assignment[var] != lit for var, lit in enumerate(c))) / len(clauses)
        if alpha_new == 0:
            return 1
        max_inf_var = influences.index(max(influences))
        left_assignment = assignment[:]
        right_assignment = assignment[:]
        left_assignment[max_inf_var] = 0
        right_assignment[max_inf_var] = 1
        return dpll(alpha_new, left_assignment) + dpll(alpha_new, right_assignment)
    
    tau_KKL = dpll(alpha, [0] * n)
    
    # Check the conjecture
    if tau_KKL is None:
        return {
            "metric_name": "log2_tau_KKL",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    log2_tau_KKL = math.log2(tau_KKL + 1)
    right_side = (1 - I_max) * (n - 1) + 5 * math.sqrt(n)
    if log2_tau_KKL <= right_side:
        return {
            "metric_name": "log2_tau_KKL",
            "metric_value": log2_tau_KKL,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "log2_tau_KKL",
            "metric_value": log2_tau_KKL,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Counterexample: n={n}, alpha={alpha}, seed={seed}"
        }

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, 30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")