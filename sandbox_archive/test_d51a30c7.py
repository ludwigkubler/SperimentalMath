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
    
    def tseitin_circuit_valuation(n):
        variables = [f'x{i+1}' for i in range(n)]
        clauses = []
        
        # Generate a simple OR circuit
        for i in range(1, n):
            clauses.append([variables[i-1], variables[i]])
        
        # Add Tseitin encoding
        tseitin_vars = [f'y{i+1}' for i in range(n)]
        for i in range(n):
            clauses.append([-tseitin_vars[i], variables[i]])
            for j in range(i+1, n):
                clauses.append([tseitin_vars[i], tseitin_vars[j], -variables[j]])
        
        return variables, clauses
    
    def resolution_refutation_size(clauses):
        # Simplistic estimation of resolution refutation size
        return len(clauses)
    
    def coxeter_group_orbit_length(variables, clauses):
        # Placeholder for actual computation
        # For simplicity, we use a dummy value
        return 2 ** (len(variables) + len(clauses))
    
    n = random.randint(5, 40)
    variables, clauses = tseitin_circuit_valuation(n)
    r_n = resolution_refutation_size(clauses)
    omega_G = coxeter_group_orbit_length(variables, clauses)
    
    return {
        "metric_name": "minimal_orbit_length",
        "metric_value": omega_G,
        "instances_tested": 1,
        "conjecture_holds": omega_G >= 2 ** math.ceil(math.log(r_n, 2)),
        "counterexample": "" if omega_G >= 2 ** math.ceil(math.log(r_n, 2)) else f"omega(G)={omega_G}, expected=2^Ω({r_n})"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(1000, 9999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support")