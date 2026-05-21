# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations

def generate_random_3cnf(n: int, m: int) -> list:
    variables = set(range(1, n + 1))
    clauses = []
    for _ in range(m):
        clause = [random.choice([var, -var]) for var in random.sample(variables, 3)]
        clauses.append(clause)
    return clauses

def poset_dimension(clauses: list, n: int) -> int:
    poset = {i: set() for i in range(1, n + 1)}
    for clause in clauses:
        for var in clause:
            if -var not in poset[-var]:
                poset[-var].add(var)
    return max(len(poset[var]) for var in poset)

def karchmer_wigderson_communication_complexity(clauses: list, n: int) -> int:
    # Simplified simulation of KW communication complexity
    # This is a placeholder and should be replaced with actual protocol simulation
    return len(clauses)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = random.randint(3 * n, 6 * n)
    clauses = generate_random_3cnf(n, m)
    
    pos_dim = poset_dimension(clauses, n)
    comm_complexity = karchmer_wigderson_communication_complexity(clauses, n)
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": comm_complexity,
        "instances_tested": 1,
        "conjecture_holds": pos_dim == comm_complexity,
        "counterexample": "" if pos_dim == comm_complexity else f"Graph with n={n}, A={clauses}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")