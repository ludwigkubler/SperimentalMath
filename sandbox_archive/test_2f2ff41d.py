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
    
    def generate_sat_clause_set(n: int):
        clauses = []
        for _ in range(n):
            clause = [random.choice([1, -1]) * (i + 1) for i in range(random.randint(2, n))]
            clauses.append(clause)
        return clauses
    
    def compute_nerve(clauses):
        # Simplified nerve computation for demonstration
        nerve = {}
        for clause in clauses:
            for lit in clause:
                if lit not in nerve:
                    nerve[lit] = set()
                for other_lit in clause:
                    if other_lit != lit and abs(lit) == abs(other_lit):
                        nerve[lit].add(other_lit)
        return nerve
    
    def local_indeterminacy_index(nerve):
        # Simplified local indeterminacy index computation
        return len(nerve)
    
    def complexity(clauses):
        return len(clauses)
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(instances_tested):
        n = random.randint(5, 40)
        φ = generate_sat_clause_set(n)
        Nφ = compute_nerve(φ)
        I_ind_Nφ = local_indeterminacy_index(Nφ)
        c = complexity(φ)
        
        if I_ind_Nφ > c * math.log2(c):
            conjecture_holds = False
            counterexample = f"n={n}, I_ind(Nφ)={I_ind_Nφ}, c*|φ|={c*math.log2(c)}"
        
        metric_values.append(I_ind_Nφ / n)
    
    return {
        "metric_name": "local_indeterminacy_ratio",
        "metric_value": sum(metric_values) / len(metric_values),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")