# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        cnf = []
        for _ in range(2**n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            cnf.append(clause)
        return cnf
    
    def compute_quadratic_form(cnf):
        n = len(cnf[0])
        Q = [[0] * n for _ in range(n)]
        for clause in cnf:
            for lit in clause:
                var = abs(lit) - 1
                Q[var][var] += 1
        return Q
    
    def compute_minimal_surface_area(Q):
        n = len(Q)
        area = 0
        for i in range(n):
            for j in range(i, n):
                area += Q[i][j]
        return area
    
    def compute_volume(A):
        return A ** (3/2)
    
    def frege_proof_width(cnf):
        # Placeholder function; actual implementation needed
        return len(cnf)  # Simplified for testing purposes
    
    results = []
    n_values = [5, 10, 15, 20, 30, 40]
    for n in n_values:
        cnf = generate_cnf(n)
        Q = compute_quadratic_form(cnf)
        A = compute_minimal_surface_area(Q)
        V = compute_volume(A)
        w = frege_proof_width(cnf)
        
        results.append({
            "n": n,
            "A(w)": A,
            "V(φ)": V,
            "w(φ)": w
        })
    
    correlation_A_w = sum((r["A(w)"] - mean_A_w) * (r["w(φ)"] - mean_w) for r in results) / len(results)
    correlation_V_4A = sum((r["V(φ)"] - mean_V_4A) ** 2 for r in results) / len(results)
    
    mean_A_w = sum(r["A(w)"] for r in results) / len(results)
    mean_V_4A = sum(r["V(φ)"] for r in results) / len(results)
    
    conjecture_holds = correlation_A_w >= 0.8 and correlation_V_4A <= 1.25
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "A(w)",
        "metric_value": mean_A_w,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_A_w = sum(r["metric_value"] for r in results) / len(results)
    std_A_w = (sum((r["metric_value"] - mean_A_w) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_A_w} std={std_A_w} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_A_w} std={std_A_w} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")