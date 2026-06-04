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
    
    def generate_group(n):
        # Generate a random group G with n elements
        # This is a placeholder implementation and should be replaced with actual group generation logic
        return {i: (i + 1) % n for i in range(n)}
    
    def mrank(G):
        # Placeholder function to compute the minimal representation rank of a group
        # This is a placeholder implementation and should be replaced with actual computation logic
        return len(G)
    
    def Tseitin_formula(G):
        # Placeholder function to construct the Tseitin formula φ_G for a given group G
        # This is a placeholder implementation and should be replaced with actual construction logic
        clauses = []
        for x in G:
            clause = [x]
            for y in G:
                if x != y:
                    clause.append(-y)
            clauses.append(clause)
        return clauses
    
    def Frege_proof_width(clauses):
        # Placeholder function to compute the Frege proof width of a Tseitin formula
        # This is a placeholder implementation and should be replaced with actual computation logic
        return len(clauses)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    G = generate_group(n)
    mrank_G = mrank(G)
    φ_G = Tseitin_formula(G)
    w_φ_G = Frege_proof_width(φ_G)
    
    if mrank_G > 10 or w_φ_G > 10:
        return {
            "metric_name": "mrank(G) vs. w(φ_G)",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    return {
        "metric_name": "mrank(G) vs. w(φ_G)",
        "metric_value": mrank_G * w_φ_G,  # Placeholder metric
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r['conjecture_holds'] for r in results):
        mean_value = sum(r['metric_value'] for r in results) / len(results)
        std_value = math.sqrt(sum((r['metric_value'] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r['seed'] for r in results if r['counterexample'] == "mapping_undefined"), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")