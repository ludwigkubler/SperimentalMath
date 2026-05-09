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
    
    def p_adic_valuation(n, p):
        if n == 0:
            return -math.inf
        valuation = 0
        while n % p == 0:
            n //= p
            valuation += 1
        return valuation
    
    def count_solutions(phi):
        n = len(phi)
        count = 0
        for i in range(2**n):
            if all((i >> j) & 1 or not any(lit % 3 == 0 for lit in clause) for j, clause in enumerate(phi)):
                count += 1
        return count
    
    def dpll_tree_size(phi, assignment=[]):
        if len(assignment) == n:
            if all(any((assignment[j] >> i) & 1 or not any(lit % 3 == 0 for lit in clause) for j, clause in enumerate(phi)) for i in range(n)):
                return 1
            else:
                return 0
        count = 0
        for val in [0, 1]:
            assignment.append(val)
            count += dpll_tree_size(phi, assignment)
            assignment.pop()
        return count
    
    n = random.randint(5, 20)
    phi = [[random.choice([-3*i-1, -3*i+1, 3*i-1, 3*i+1]) for _ in range(random.randint(3, 5))] for _ in range(n)]
    
    solutions_mod_p = count_solutions(phi) % 3
    valuation = p_adic_valuation(solutions_mod_p, 3)
    tree_size = dpll_tree_size(phi)
    
    metric_name = "p-adic Valuation vs DPLL Tree Size"
    metric_value = (valuation, math.log2(tree_size))
    instances_tested = 1
    conjecture_holds = abs(valuation - math.log2(tree_size)) < 0.5
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_valuation = sum(val for val, _ in [r["metric_value"] for r in results]) / len(results)
    mean_tree_size = sum(size for _, size in [r["metric_value"] for r in results]) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean_valuation={mean_valuation} mean_tree_size={mean_tree_size} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")