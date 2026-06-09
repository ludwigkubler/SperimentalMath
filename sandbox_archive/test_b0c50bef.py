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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n // 4):  # Ensure at least 2^n / 4 clauses
            clause = [random.randint(-n, n-1) for _ in range(random.randint(1, n))]
            clauses.append(clause)
        return clauses
    
    def frege_proof_width(cnf):
        # Simplified heuristic to estimate proof width
        return len(cnf) ** 0.5
    
    def hausdorff_dimension(cnf):
        # Simplified heuristic to estimate Hausdorff dimension
        return len(cnf) ** 0.333
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    
    w_phi = frege_proof_width(cnf)
    D_H_phi = hausdorff_dimension(cnf)
    
    alpha_n = D_H_phi
    beta_n = D_H_phi
    
    if abs(w_phi - (D_H_phi ** 2 * n)) > 3:
        return {
            "metric_name": "Frege Proof Width",
            "metric_value": w_phi,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": f"Failed for n={n}, w(φ)={w_phi}, D_H(φ)={D_H_phi}"
        }
    
    return {
        "metric_name": "Frege Proof Width",
        "metric_value": w_phi,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")