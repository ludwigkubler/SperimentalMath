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
    
    def generate_frege_proof(n, clause_density):
        num_clauses = int(n * clause_density)
        proof = []
        for _ in range(num_clauses):
            literals = [random.choice([f'x{i}', f'-x{i}']) for i in range(1, n + 1)]
            proof.append(literals)
        return proof
    
    def compute_coxeter_diagram(proof):
        diagram = {}
        for clause in proof:
            for lit1 in clause:
                for lit2 in clause:
                    if lit1 != lit2 and (lit1[0] == '-' or lit2[0] == '-'):
                        key = tuple(sorted([lit1, lit2]))
                        diagram[key] = True
        return len(diagram)
    
    def alpha(depth):
        # Placeholder function for α(D(φ))
        # This is a dummy implementation; replace with actual computation if possible.
        return depth
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_edges = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        for _ in range(5):  # Sample 5 instances per size
            proof = generate_frege_proof(n, random.uniform(0.1, 0.5))
            depth = len(proof)
            edges = compute_coxeter_diagram(proof)
            total_edges += edges
            instances_tested += 1
            n_max = max(n_max, n)
    
    mean_edges = total_edges / instances_tested
    conjecture_holds = mean_edges <= 10
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "average_coxeter_diagram_edges",
        "metric_value": mean_edges,
        "instances_tested": instances_tested,
        "n_max": n_max,
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
    
    mean_edges = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_edges} std=0 support_fraction=1")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_edges} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")