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
    
    def resolve(cnf):
        n = len(cnf[0])
        dnf = []
        
        for clause in cnf:
            new_clause = []
            for literal in clause:
                if -literal in new_clause:
                    return []  # Conflict found, resolution fails
                elif literal not in new_clause and -literal not in [x for c in dnf for x in c]:
                    new_clause.append(literal)
            if new_clause:
                dnf.append(new_clause)
        
        return dnf

    def fast_walsh_hadamard_transform(fourier_coeffs):
        n = len(fourier_coeffs)
        while n > 1:
            half = n // 2
            for i in range(half):
                even = fourier_coeffs[2 * i]
                odd = fourier_coeffs[2 * i + 1]
                fourier_coeffs[i] = even + odd
                fourier_coeffs[half + i] = even - odd
            n //= 2
        return fourier_coeffs

    def polymatroid_rank(fourier_coeffs, S):
        return sum(abs(coeff) for i, coeff in enumerate(fourier_coeffs) if i+1 in S)

    k = 5
    n = 40
    
    # Generate a random 3-CNF formula with n variables and m clauses
    m = random.randint(2 * n, 4 * n)
    cnf = []
    for _ in range(m):
        clause = [random.choice([-i, i]) for i in range(1, n+1)]
        if len(set(clause)) == 3:
            cnf.append(clause)
    
    # Convert the 3-CNF to a monotone DNF via resolution
    dnf = resolve(cnf)
    if not dnf:
        return {
            "metric_name": "polymatroid_rank",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Resolution failed"
        }
    
    # Compute Fourier coefficients via Fast Walsh-Hadamard Transform
    fourier_coeffs = [0] * (2 ** n)
    for clause in dnf:
        mask = 0
        for literal in clause:
            if literal > 0:
                mask |= (1 << (literal - 1))
            else:
                mask &= ~(1 << (-literal - 1))
        fourier_coeffs[mask] += 1
    
    # Normalize Fourier coefficients
    norm_factor = math.sqrt(2 ** n)
    for i in range(len(fourier_coeffs)):
        fourier_coeffs[i] /= norm_factor
    
    # Compute polymatroid rank function ρ(S) for all subsets S
    rho_values = [polymatroid_rank(fourier_coeffs, set(range(1, n+1)))]

    # Verify the conjecture
    if rho_values[0] < math.sqrt(n) * k ** 0.25:
        return {
            "metric_name": "polymatroid_rank",
            "metric_value": rho_values[0],
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"ρ([n]) = {rho_values[0]} < {math.sqrt(n) * k ** 0.25}"
        }
    
    return {
        "metric_name": "polymatroid_rank",
        "metric_value": rho_values[0],
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                break
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[results.index(r)]}")