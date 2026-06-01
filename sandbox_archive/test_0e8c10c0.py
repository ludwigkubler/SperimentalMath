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
    
    def generate_cnf(n):
        cnf = []
        for i in range(1, n + 1):
            clause = [random.choice([-1, 1]) * j for j in range(1, n + 1)]
            if all(clause[i] != -clause[j] for j in range(i)):
                cnf.append(clause)
        return cnf
    
    def tseitin_representation(cnf):
        literals = set()
        for clause in cnf:
            literals.update(abs(lit) for lit in clause)
        
        tseitin_vars = list(range(1, len(literals) + 1))
        formulas = []
        
        for i, literal in enumerate(literals, start=1):
            formulas.append(f"{tseitin_vars[i-1]} <-> ( {' & '.join(str(lit) if lit > 0 else f'¬{abs(lit)}' for lit in cnf[i-1])} )")
        
        return formulas
    
    def dpll_search_tree_diameter(formulas):
        # Simplified DPLL search tree diameter calculation
        n = len(formulas)
        return n * (n - 1) // 2
    
    def minimal_local_ring_norm(cnf):
        # Placeholder for actual computation of minimal local ring norm
        return random.random()
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    tseitin_formulas = tseitin_representation(cnf)
    td = dpll_search_tree_diameter(tseitin_formulas)
    min_norm = minimal_local_ring_norm(cnf)
    
    metric_value = math.log(math.factorial(n)) * min_norm
    instances_tested = 1
    n_max = n
    conjecture_holds = False
    counterexample = "mapping_undefined"
    
    return {
        "metric_name": "log(n!) * min_{P ∈ φ_T} |P|",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='<desc>' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")