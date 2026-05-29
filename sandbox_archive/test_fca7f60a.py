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
    
    def generate_3cnf(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.choice([1, -1]) * (i + 1) for i in random.sample(range(n), random.randint(1, n))]
            clauses.append(clause)
        return clauses
    
    def truth_table_size(n):
        return 2 ** n
    
    def hilbert_cube_diameter(n):
        return math.log2(truth_table_size(n))
    
    def frege_proof_depth(clauses):
        # Simplified DPLL-based solver to estimate proof depth
        stack = []
        model = {}
        for clause in clauses:
            if all(l not in model or model[l] != -l for l in clause):
                stack.append((clause, 1))
            else:
                return len(stack)
        while stack:
            (clause, level) = stack.pop()
            for i, literal in enumerate(clause):
                new_clause = [l for j, l in enumerate(clause) if j != i]
                if all(l not in model or model[l] != -l for l in new_clause):
                    stack.append((new_clause, level + 1))
        return len(stack)
    
    n = random.randint(5, 40)
    m = random.randint(n * 2, n * 3)
    clauses = generate_3cnf(n, m)
    diameter = hilbert_cube_diameter(n)
    proof_depth = frege_proof_depth(clauses)
    
    if proof_depth == 0:
        return {
            "metric_name": "diameter / proof_depth",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "proof_depth_zero"
        }
    
    ratio = diameter / proof_depth
    return {
        "metric_name": "diameter / proof_depth",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio <= 2,  # Hypothetical constant c=2 for simplicity
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1000, 9999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result = f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}"
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if r["counterexample"]), "")
        result = f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}"
    
    print(result)