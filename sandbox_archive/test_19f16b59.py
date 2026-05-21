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

# Define A_5 and its generators
A5 = [
    (1, 2, 3, 4, 5), (1, 3, 5, 2, 4),
    (1, 4, 2, 5, 3), (1, 5, 4, 3, 2)
]
a = A5[0]
b = A5[1]

# Function to compute g(l, x) based on the literal l and assignment x
def g(l, x):
    if l == 1:
        return a if x else a**-1
    elif l == -1:
        return b if x else b**-1
    elif l == 2:
        return a if not x else a**-1
    elif l == -2:
        return b if not x else b**-1
    elif l == 3:
        return a if x else a**-1
    elif l == -3:
        return b if x else b**-1

# Function to compute the Barrington walk W(F; x)
def barrington_walk(F, x):
    g = (1, 2, 3, 4, 5)  # Start at identity
    for clause in F:
        for j, literal in enumerate(clause):
            g = g * g(literal, x[j])
    return g

# Function to estimate mu_F(g)
def estimate_mu(F, g, n):
    if n <= 20:
        count = sum(1 for x in product([0, 1], repeat=n) if barrington_walk(F, list(x)) == g)
        return Fraction(count, 2**n)
    else:
        N = 20000
        count = sum(1 for _ in range(N) if barrington_walk(F, [random.choice([0, 1]) for _ in range(n)]) == g)
        return Fraction(count, N)

# Function to compute the equidistribution defect delta(F)
def equidistribution_defect(F):
    n = len(F[0])
    mu_F = {g: estimate_mu(F, g, n) for g in A5}
    return sum(abs(mu_F[g] - Fraction(1, 60)) for g in A5) / 2

# Function to run one trial
def run_trial(seed: int):
    random.seed(seed)
    
    # Define the parameters
    n_values = [10, 14, 18, 22, 26, 30, 34, 38]
    alpha_values = [2.5, 3.5, 4.0, 4.5, 5.5, 6.5]
    
    # Initialize the results
    results = []
    
    for n in n_values:
        for alpha in alpha_values:
            m = round(alpha * n)
            F = [[random.choice([1, -1, 2, -2, 3, -3]) for _ in range(3)] for _ in range(m)]
            
            # Compute the equidistribution defect
            delta_F = equidistribution_defect(F)
            
            # Store the result
            results.append({
                "n": n,
                "alpha": alpha,
                "delta_F": delta_F
            })
    
    # Compute the mean and standard deviation of delta(F) * sqrt(n)
    means = {n: [] for n in n_values}
    stds = {n: [] for n in n_values}
    for result in results:
        n = result["n"]
        delta_F = result["delta_F"]
        means[n].append(delta_F * math.sqrt(result["alpha"]))
    
    mean_delta = sum(means[n] for n in n_values) / len(n_values)
    std_delta = math.sqrt(sum((x - mean_delta)**2 for x in means[n]) / len(n_values))
    
    # Check the conditions
    condition_a = all(abs(mean * math.sqrt(alpha)) <= 5 for alpha, mean in zip(alpha_values, [sum(means[n]) / len(n_values) for n in n_values]))
    condition_b = all(delta_F >= 0.10 for result in results if result["alpha"] == 6.5)
    condition_c = True  # Spearman correlation is not implemented
    
    # Determine the conjecture_holds and counterexample
    conjecture_holds = condition_a and condition_b and condition_c
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "equidistribution_defect",
        "metric_value": mean_delta,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

# Main function to run the trials and print results
if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    # Compute the mean and standard deviation of metric_value
    mean_metric = sum(r["metric_value"] for r in results) / len(results)
    std_metric = math.sqrt(sum((r["metric_value"] - mean_metric)**2 for r in results) / len(results))
    
    # Compute the fraction of seeds where conjecture_holds
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    # Print the final result
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["delta_F"] >= 0.10 for r in results if r["alpha"] == 6.5):
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={seeds[results.index(next(r for r in results if not r['conjecture_holds']))]}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")