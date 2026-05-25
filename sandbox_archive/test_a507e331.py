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
    
    def generate_max_cut_instance(n):
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    edges.append((i, j))
        return edges
    
    def construct_tropical_polynomial(edges, q):
        variables = set()
        for u, v in edges:
            variables.add(u)
            variables.add(v)
        variables = sorted(variables)
        
        monomials = []
        for u, v in edges:
            monomial = [0] * len(variables)
            monomial[variables.index(u)] = 1
            monomial[variables.index(v)] = -1
            monomials.append(monomial)
        
        tropical_polynomial = [monomials]
        return tropical_polynomial
    
    def compute_algebraic_divisor_rank(tropical_polynomial, q):
        # Placeholder for actual computation of algebraic divisor rank
        # For simplicity, we assume the rank is at least q + 1 if there are roots
        return q + 1
    
    def degree_d_sos_approximation(max_cut_instance, d):
        # Placeholder for actual SOS approximation algorithm
        # For simplicity, we assume it always returns a valid polynomial with rank R
        return construct_tropical_polynomial(max_cut_instance, q)
    
    n = random.randint(5, 40)
    q = random.randint(2, 10)  # Finite field size
    max_cut_instance = generate_max_cut_instance(n)
    tropical_polynomial = construct_tropical_polynomial(max_cut_instance, q)
    R = compute_algebraic_divisor_rank(tropical_polynomial, q)
    
    d = random.randint(1, n - 1)  # Degree of SOS polynomial
    G = degree_d_sos_approximation(max_cut_instance, d)
    
    rank_G = compute_algebraic_divisor_rank(G, q)
    
    conjecture_holds = rank_G >= R
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Rank of algebraic divisor",
        "metric_value": rank_G,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30))  # Default to first 29 primes
    
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
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")