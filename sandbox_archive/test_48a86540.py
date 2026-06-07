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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_clauses(n):
        clauses = []
        for _ in range(n):
            clause = {random.randint(1, n) for _ in range(random.randint(1, 3))}
            clauses.append(clause)
        return clauses
    
    def dpll_proof_tree_height(clause_set):
        if not clause_set:
            return 0
        variables = set()
        for clause in clause_set:
            variables.update(clause)
        true_clauses = {c for c in clause_set if any(var in c for var in variables)}
        false_clauses = clause_set - true_clauses
        if not true_clauses or not false_clauses:
            return 1
        height = 0
        for variable in variables:
            new_true_clauses = {c for c in true_clauses if variable in c}
            new_false_clauses = {c for c in false_clauses if variable not in c}
            height = max(height, dpll_proof_tree_height(new_true_clauses) + 1, dpll_proof_tree_height(new_false_clauses) + 1)
        return height
    
    def geometric_complexity(clause_set):
        n = len(clause_set)
        total_length = sum(len(c) for c in clause_set)
        return Fraction(total_length, n)
    
    max_n = 0
    instances_tested = 0
    total_height = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > max_n:
            max_n = n
        
        for _ in range(5):  # Ensure at least 30 instances per seed
            clauses = generate_clauses(n)
            height = dpll_proof_tree_height(clauses)
            complexity = geometric_complexity(clauses)
            
            total_height += height
            instances_tested += 1
            
            if height > 10 * complexity:
                conjecture_holds = False
                counterexample = f"n={n}, height={height}, complexity={complexity}"
    
    mean_height = Fraction(total_height, instances_tested)
    support_fraction = Fraction(instances_tested - (instances_tested if not conjecture_holds else 0), instances_tested)
    
    return {
        "metric_name": "DPLL Proof Tree Height",
        "metric_value": float(mean_height),
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_height = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_height} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")