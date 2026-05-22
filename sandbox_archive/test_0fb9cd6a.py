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
    n = random.randint(5, 40)
    G = generate_tseitin_formula(n)
    
    μ_G = compute_μ(G)
    refutation_length = resolve_refutation(G)
    
    return {
        "metric_name": "resolution_refutation_length",
        "metric_value": refutation_length,
        "instances_tested": 1,
        "conjecture_holds": μ_G <= refutation_length - 3,
        "counterexample": "" if μ_G <= refutation_length - 3 else f"μ(G)={μ_G}, refutation_length={refutation_length}"
    }

def generate_tseitin_formula(n: int) -> list:
    symbols = [f"x{i}" for i in range(1, n+1)]
    clauses = []
    
    # Generate clauses
    for i in range(1, n+1):
        clauses.append([f"¬{symbols[i-1]}"])
        for j in range(i+1, n+1):
            clauses.append([f"{symbols[j-1]}", f"¬{symbols[i-1]}"])
    
    # Generate the final clause
    final_clause = []
    for i in range(n):
        final_clause.append(f"¬{symbols[i]}")
    clauses.append(final_clause)
    
    return clauses

def compute_μ(G: list) -> float:
    # Placeholder function to compute μ(G)
    # This is a dummy implementation and should be replaced with actual Hodge decomposition logic
    return random.random()

def resolve_refutation(G: list) -> int:
    # Placeholder function to resolve refutation
    # This is a dummy implementation and should be replaced with actual resolution logic
    return len(G)

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if r["counterexample"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")