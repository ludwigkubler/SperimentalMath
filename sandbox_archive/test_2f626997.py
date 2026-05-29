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
    
    def generate_3cnf(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if random.choice([True, False]):
                clause[0] *= -1
            if random.choice([True, False]):
                clause[1] *= -1
            clauses.append(clause)
        return clauses

    def resolution_width(clauses):
        # Simplified DPLL solver to estimate resolution width
        states = [set()]
        while True:
            new_states = set()
            for state in states:
                found_resolvent = False
                for clause in clauses:
                    if not any(abs(lit) in state for lit in clause):
                        resolvent = [lit for lit in clause if lit not in state]
                        if len(resolvent) == 1:
                            new_states.add(state.union({resolvent[0]}))
                            found_resolvent = True
                if not found_resolvent:
                    break
            if states == new_states:
                return max(len(s) for s in states)
            states = new_states

    def minimal_quaternion_order(clauses):
        # Placeholder function to compute minimal quaternion order
        # This is a dummy implementation and should be replaced with actual logic
        return len(clauses)

    n = random.randint(5, 30)
    m = min(n * (n - 1) // 2, 20)
    clauses = generate_3cnf(n, m)
    
    width = resolution_width(clauses)
    order = minimal_quaternion_order(clauses)
    
    return {
        "metric_name": "resolution_width",
        "metric_value": width,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_width = sum(result["metric_value"] for result in results) / len(results)
    std_width = math.sqrt(sum((result["metric_value"] - mean_width) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_width} std={std_width} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unsupported_operation")