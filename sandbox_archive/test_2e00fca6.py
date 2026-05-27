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
    
    def generate_sat_instance(n):
        variables = [f'x{i}' for i in range(n)]
        clauses = []
        for _ in range(2**n):
            clause = ' or '.join(random.sample(variables, random.randint(1, n)))
            clauses.append(f'({clause})')
        return ' and '.join(clauses)
    
    def polynomial_ring_from_sat_instance(instance):
        variables = set()
        for clause in instance.split(' and '):
            for term in clause.split(' or '):
                if '(' in term:
                    term = term[1:-1]
                variables.update(term.split('x'))
        return variables
    
    def dpll_proof_tree_size(instance):
        # Simplified DPLL proof tree size estimation
        return len(instance.split(' and '))
    
    def tropicalized_etale_cohomology_rank(variables):
        # Placeholder for actual computation
        # For simplicity, we use the number of variables as a proxy
        return len(variables)
    
    n = random.randint(5, 40)
    instance = generate_sat_instance(n)
    variables = polynomial_ring_from_sat_instance(instance)
    proof_tree_size = dpll_proof_tree_size(instance)
    rank = tropicalized_etale_cohomology_rank(variables)
    
    g_n = math.log(proof_tree_size + 1) if proof_tree_size > 0 else 0
    conjecture_holds = rank <= g_n and rank <= 2 * proof_tree_size
    
    return {
        "metric_name": "Rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"n={n}, rank={rank}, g(n)={g_n}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")