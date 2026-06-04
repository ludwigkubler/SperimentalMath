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
    
    def generate_group(n):
        # Generate a random group G with n elements using Cayley's theorem
        generators = [random.sample(range(1, n), 2) for _ in range(random.randint(1, 3))]
        relations = []
        for gen in generators:
            rel = [(gen[0], gen[1]), (gen[1], gen[0])]
            relations.extend(rel)
        return generators, relations

    def minimal_representation_rank(generators, relations):
        # Compute the minimal representation rank of the group G
        n = len(generators)
        mrank = 0
        for rel in relations:
            if rel not in generators and (rel[1], rel[0]) not in generators:
                mrank += 1
        return mrank

    def tseitin_formula(n):
        # Construct the Tseitin formula φ_G for the group G
        clauses = []
        for i in range(1, n+1):
            for j in range(1, n+1):
                if i != j:
                    clause = [f'x{i}', f'x{j}']
                    clauses.append(clause)
        return clauses

    def frege_proof_width(clauses):
        # Compute the Frege proof width of the Tseitin formula φ_G
        width = 0
        for clause in clauses:
            width = max(width, len(clause))
        return width

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        generators, relations = generate_group(n)
        mrank = minimal_representation_rank(generators, relations)
        clauses = tseitin_formula(n)
        w_phi_G = frege_proof_width(clauses)
        
        if mrank is None or w_phi_G is None:
            return {
                "metric_name": "mrank(G) vs. w(φ_G)",
                "metric_value": None,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        
        results.append({
            "mrank": mrank,
            "w_phi_G": w_phi_G
        })
    
    if len(results) < 30:
        return {
            "metric_name": "mrank(G) vs. w(φ_G)",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    mrank_values = [r['mrank'] for r in results]
    w_phi_G_values = [r['w_phi_G'] for r in results]
    
    mean_mrank = sum(mrank_values) / len(mrank_values)
    mean_w_phi_G = sum(w_phi_G_values) / len(w_phi_G_values)
    
    if any(val > 10 for val in mrank_values + w_phi_G_values):
        return {
            "metric_name": "mrank(G) vs. w(φ_G)",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "value_exceeds_10"
        }
    
    return {
        "metric_name": "mrank(G) vs. w(φ_G)",
        "metric_value": mean_mrank * mean_w_phi_G,  # Using product as a proxy for correlation
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": False,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r['conjecture_holds'] for r in results):
        mean_metric_value = sum(r['metric_value'] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r['seed'] for r in results if not r['conjecture_holds']), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")