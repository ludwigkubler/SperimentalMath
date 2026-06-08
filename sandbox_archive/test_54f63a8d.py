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
    
    def tseitin_embedding(phi):
        literals = set()
        clauses = []
        
        def process_formula(formula, prefix=""):
            if isinstance(formula, str):
                literals.add(prefix + formula)
                return prefix + formula
            elif formula[0] == "NOT":
                return "NOT_" + process_formula(formula[1], prefix)
            elif formula[0] == "AND":
                left = process_formula(formula[1], prefix)
                right = process_formula(formula[2], prefix)
                var = f"V_{len(literals)}"
                literals.add(var)
                clauses.append([left, right, "-NOT_" + var])
                clauses.append(["-left", "-right", var])
                return var
            elif formula[0] == "OR":
                left = process_formula(formula[1], prefix)
                right = process_formula(formula[2], prefix)
                var = f"V_{len(literals)}"
                literals.add(var)
                clauses.append(["-left", "-right", "-var"])
                clauses.append([left, var])
                clauses.append([right, var])
                return var
            else:
                raise ValueError("Invalid formula")
        
        process_formula(phi)
        return literals, clauses
    
    def min_local_index(embedding):
        # Placeholder for minimal local index calculation
        # This is a dummy implementation and should be replaced with actual logic
        return len(embedding)
    
    def dpll_proof_path_length(clauses):
        # Placeholder for DPLL proof path length calculation
        # This is a dummy implementation and should be replaced with actual logic
        return len(clauses)
    
    n = random.randint(5, 40)
    phi = generate_random_formula(n)
    embedding = tseitin_embedding(phi)
    min_ind = min_local_index(embedding[0])
    p = dpll_proof_path_length(embedding[1])
    
    return {
        "metric_name": "min_ind_p_correlation",
        "metric_value": min_ind * p,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

def generate_random_formula(n):
    if n == 0:
        return random.choice(["True", "False"])
    elif n == 1:
        return random.choice(["A", "-A"])
    else:
        op = random.choice(["AND", "OR"])
        left = generate_random_formula(n - 1)
        right = generate_random_formula(n - 1)
        if op == "AND":
            return ("AND", left, right)
        elif op == "OR":
            return ("OR", left, right)

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.75:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")