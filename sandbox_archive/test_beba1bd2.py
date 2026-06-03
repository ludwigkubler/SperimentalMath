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
    
    def generate_tseitin_formula(n):
        # Generate a Tseitin formula with n variables
        literals = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for literal in literals:
            clauses.append([literal])
        for i in range(1, n+1):
            clauses.append([f'~x{i}', f'x{i}'])
        return clauses
    
    def frege_proof_depth(clauses):
        # Compute the Frege proof depth
        if not clauses:
            return 0
        max_depth = 0
        for clause in clauses:
            if len(clause) == 1:
                continue
            sub_clauses = [c for c in clauses if c != clause]
            depth = 1 + max(frege_proof_depth(sub_clauses), frege_proof_depth([~c for c in clause]))
            max_depth = max(max_depth, depth)
        return max_depth
    
    def longest_arithmetic_hierarchy_sequence(n):
        # Compute the length of the longest sequence of jumps in the arithmetic hierarchy
        if n == 1:
            return 0
        return 2 * (n - 1)
    
    n = random.randint(5, 40)
    formula = generate_tseitin_formula(n)
    f_pi = frege_proof_depth(formula)
    L_pi = longest_arithmetic_hierarchy_sequence(n)
    
    return {
        "metric_name": "Frege Proof Depth",
        "metric_value": f_pi,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": f_pi <= L_pi,
        "counterexample": "" if f_pi <= L_pi else f"Counterexample: n={n}, f(π)={f_pi}, L(π)={L_pi}"
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample_desc = next(result["counterexample"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")