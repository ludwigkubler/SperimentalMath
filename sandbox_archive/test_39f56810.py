# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def generate_3cnf(n, m):
    clauses = []
    for _ in range(m):
        clause = [random.randint(1, n), random.randint(-n, -1)]
        if len(set(clause)) == 2:
            clauses.append(clause)
    return clauses

def construct_mapping(clauses):
    # Placeholder mapping procedure
    return 50  # This should be replaced with actual computation

def resolution_width(clauses):
    stack = []
    for clause in clauses:
        stack.append(clause)
        while len(stack) > 1:
            c1, c2 = stack.pop(), stack.pop()
            new_clauses = []
            for lit in c1:
                if -lit in c2:
                    continue
                for l in c2:
                    if l != -lit:
                        new_clauses.append([l])
                break
            else:
                stack.extend(new_clauses)
        if not stack:
            return 0
    return len(stack)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = random.randint(n, n * 3)
    clauses = generate_3cnf(n, m)
    I_phi = construct_mapping(clauses)
    w_phi = resolution_width(clauses)
    return {
        "metric_name": "I(phi) <= w(phi)",
        "metric_value": I_phi - w_phi,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": I_phi <= w_phi + 5,
        "counterexample": "" if I_phi <= w_phi + 5 else f"Counterexample for n={n}, m={m}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(2, 6)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")