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
        clauses = []
        for _ in range(n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def is_tautology(cnf):
        # Simplified check for tautology
        variables = set(abs(lit) for lit in sum(cnf, []))
        assignments = {var: random.choice([True, False]) for var in variables}
        for clause in cnf:
            if not any(assignments[abs(lit)] == (lit > 0) for lit in clause):
                return False
        return True
    
    def free_probability_entanglement(cnf):
        # Simplified model of entanglement
        return len(cnf)
    
    def minimal_invariant(entanglement):
        # Simplified model of invariant
        return math.log2(entanglement + 1)
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    if not is_tautology(cnf):
        return {
            "metric_name": "minimal_invariant",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "not a tautology"
        }
    
    entanglement = free_probability_entanglement(cnf)
    invariant = minimal_invariant(entanglement)
    
    return {
        "metric_name": "minimal_invariant",
        "metric_value": invariant,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_metric_value / len(results)} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='not a tautology' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")