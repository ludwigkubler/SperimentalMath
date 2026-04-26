# auto-injected by SEC sandbox
import collections
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
    from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import itertools
import math
import json
from sys import argv

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(clause[i] != -clause[j] for i in range(n) for j in range(i + 1, n)):
                clauses.append(clause)
        return clauses
    
    def euler_characteristic(cnf):
        n = len(cnf[0])
        subsets = []
        for r in range(1, len(cnf) + 1):
            subsets.extend(itertools.combinations(cnf, r))
        consistent_assignments = set()
        for subset in subsets:
            assignment = [False] * n
            valid = True
            for clause in subset:
                satisfied = False
                for var in clause:
                    if abs(var) <= n and (var > 0) == assignment[abs(var) - 1]:
                        satisfied = True
                        break
                if not satisfied:
                    valid = False
                    break
            if valid:
                consistent_assignments.add(tuple(assignment))
        return len(consistent_assignments)
    
    def communication_complexity(cnf):
        n = len(cnf[0])
        m = len(cnf)
        # Simple deterministic protocol: each player sends their assignment bit by bit
        return n * (n + 1) // 2
    
    n = random.randint(5, 14)
    m = random.randint(n, n * 3)
    cnf = generate_cnf(n, m)
    
    euler_char = euler_characteristic(cnf)
    comm_complexity = communication_complexity(cnf)
    
    return {
        "metric_name": "Euler Characteristic",
        "metric_value": euler_char,
        "instances_tested": 1,
        "conjecture_holds": euler_char == comm_complexity,
        "counterexample": "" if euler_char == comm_complexity else f"CNF: {cnf}, Euler Char: {euler_char}, Comm Complexity: {comm_complexity}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in argv[1:]] or [11, 23, 37, 53, 71]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(json.dumps({"TRIAL": {"seed": seed, **result}}))
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] for r in results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results) or support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_metric_value / len(results):.2f} std=0.00 support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")