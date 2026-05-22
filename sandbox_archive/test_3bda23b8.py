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
    
    def generate_tseitin_formula(n):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for i in range(n):
            clauses.append(f'{variables[i]}')
            clauses.append(f'-{variables[i]}')
        for i in range(n):
            for j in range(i+1, n):
                clauses.append(f'{-variables[i]} {variables[j]} -{variables[j]}')
                clauses.append(f'{variables[i]} {-variables[j]} {variables[j]}')
        return ' '.join(clauses)
    
    def resolution_proof_length(formula):
        # Simplified version of resolution proof length calculation
        # This is a placeholder and should be replaced with actual logic
        return len(formula.split())
    
    n = random.randint(5, 40)
    formula = generate_tseitin_formula(n)
    rank = n * math.log(n)  # Placeholder for minimal rank of geometric quantization
    proof_length = resolution_proof_length(formula)
    
    return {
        "metric_name": "Resolution Proof Length",
        "metric_value": proof_length,
        "instances_tested": 1,
        "conjecture_holds": proof_length <= rank,
        "counterexample": "" if proof_length <= rank else f"Proof length {proof_length} exceeds expected rank {rank}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Proof length exceeds expected rank\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")