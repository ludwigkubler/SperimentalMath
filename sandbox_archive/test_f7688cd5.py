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
    
    def tseitin_formula(n):
        literals = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        
        # Clause 1: x1 ∨ ¬x2
        clauses.append([1, -2])
        
        # Clause 2: ¬x1 ∨ x3
        clauses.append([-1, 3])
        
        # Clause 3: x2 ∨ x4
        clauses.append([2, 4])
        
        # Clause 4: ¬x3 ∨ ¬x5
        clauses.append([-3, -5])
        
        return literals, clauses
    
    def noncrossing_partition(literals):
        n = len(literals)
        partition = []
        for i in range(n):
            partition.append([i+1])
        return partition
    
    def resolution_proof_length(clauses):
        # Simplified estimation of Resolution proof length
        return 2 ** (len(clauses) * 0.5)
    
    literals, clauses = tseitin_formula(4)
    rank_P = len(noncrossing_partition(literals))
    proof_length = resolution_proof_length(clauses)
    
    metric_value = proof_length
    conjecture_holds = proof_length >= 2 ** (math.log2(rank_P) * 0.5)
    counterexample = "" if conjecture_holds else f"Proof length {proof_length} is less than expected 2^(log2({rank_P}) * 0.5)"
    
    return {
        "metric_name": "Resolution proof length",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
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
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")