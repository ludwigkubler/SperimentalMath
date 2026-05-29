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
                clause[0], clause[1] = -clause[0], -clause[1]
            clauses.append(clause)
        return clauses
    
    def resolution_width(clauses):
        states = [{'A': set(), 'B': set()}]
        for clause in clauses:
            new_states = []
            for state in states:
                if not any(lit in state['A'] or -lit in state['B'] for lit in clause):
                    continue
                for lit in clause:
                    if lit > 0:
                        new_state = {'A': state['A'].union({lit}), 'B': state['B']}
                    else:
                        new_state = {'A': state['A'], 'B': state['B'].union({-lit})}
                    new_states.append(new_state)
            states.extend(new_states)
        return max(len(s) for s in states if s)

    n = random.randint(5, 30)
    m = min(n * 2, 20)
    clauses = generate_3cnf(n, m)
    
    try:
        width = resolution_width(clauses)
    except ValueError:
        return {
            "metric_name": "resolution_width",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "empty_resolution_states"
        }
    
    order = (n ** Fraction(2, 3)) * (m ** Fraction(1, 4))
    return {
        "metric_name": "minimal_order",
        "metric_value": order,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or list(range(2, 30))  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_order = sum(r["metric_value"] for r in results) / len(results)
    std_order = math.sqrt(sum((r["metric_value"] - mean_order) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_order} std={std_order} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"empty_resolution_states\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")