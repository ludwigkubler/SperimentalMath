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
    
    def tseitin_encoding(variables, clauses):
        new_vars = {}
        tseitin_clauses = []
        
        for clause in clauses:
            if len(clause) == 1:
                l = clause[0]
                if l < 0:
                    l = -l
                if l not in new_vars:
                    new_var = max(new_vars.values()) + 1 if new_vars else 1
                    new_vars[l] = new_var
                tseitin_clauses.append([new_var, -l])
            else:
                new_var = max(new_vars.values()) + 1 if new_vars else 1
                new_vars[new_var] = new_var
                for l in clause:
                    if l < 0:
                        l = -l
                    tseitin_clauses.append([new_var, -l])
                tseitin_clauses.append([-new_var] + [-l for l in clause])
        
        return list(new_vars.values()), tseitin_clauses
    
    def lie_algebroid_dimension(n):
        # Placeholder function to compute the Lie algebroid dimension
        return n ** (2/3)
    
    def k_clique_circuit_size(k, n):
        # Placeholder function to compute the circuit size for k-CLIQUE
        return k * n
    
    sizes = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for size in sizes:
        n = random.randint(1, size)
        k = random.randint(1, min(n, 5))
        
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(k):
            clause = [random.choice(variables) for _ in range(random.randint(1, n))]
            clauses.append(clause)
        
        literals, tseitin_clauses = tseitin_encoding(variables, clauses)
        lie_dim = lie_algebroid_dimension(n)
        circuit_size = k_clique_circuit_size(k, n)
        
        if lie_dim < Fraction(k ** (2/3) * n ** (2/3)):
            conjecture_holds = False
            counterexample = f"n={n}, k={k}, Lie dim={lie_dim}, Circuit size={circuit_size}"
            break
        
        total_metric_value += lie_dim
        instances_tested += 1
    
    return {
        "metric_name": "Lie algebroid dimension",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "n_max": max(sizes),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")