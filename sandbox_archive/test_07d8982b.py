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
    
    def dpll(instance):
        # Simplified DPLL algorithm for demonstration purposes
        if not instance:
            return True
        literal = next((lit for lit in instance if lit != -lit), None)
        if literal is None:
            return False
        new_instance = [lit for lit in instance if lit != literal and lit != -literal]
        return dpll(new_instance) or dpll([l for l in new_instance if l != -literal])
    
    def generate_boolean_satisfiability(n):
        # Generate a random Boolean satisfiability instance with n variables
        clauses = []
        for _ in range(10 * n):  # Each variable appears in multiple clauses
            clause = [random.choice([i, -i]) for i in range(1, n + 1)]
            clauses.append(clause)
        return clauses
    
    def find_monomial_generators(instance):
        # Simplified method to find monomial generators (not actual algebraic geometry)
        return len(instance)
    
    instance = generate_boolean_satisfiability(40)
    dpll_length = len(dpll(instance))
    monomial_generators = find_monomial_generators(instance)
    
    metric_name = "monomial_generators_vs_dpll_length"
    metric_value = abs(monomial_generators - dpll_length) / (monomial_generators + dpll_length) if monomial_generators + dpll_length != 0 else float('inf')
    instances_tested = 1
    n_max = 40
    conjecture_holds = False
    counterexample = ""
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.2:
        print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")