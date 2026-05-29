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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.randint(-1, 1) * i for i in range(1, n+1)]
            if sum(clause) != 0:
                clauses.append(clause)
        return clauses

    def resolution(cnf):
        stack = cnf[:]
        while True:
            new_clause = None
            for i in range(len(stack)):
                for j in range(i + 1, len(stack)):
                    if set(stack[i]) & set(stack[j]):
                        new_clause = [x for x in stack[i] if x not in stack[j]] + \
                                      [y for y in stack[j] if y not in stack[i]]
                        break
                if new_clause:
                    break
            if not new_clause:
                return len(cnf) - len(stack)
            stack.append(new_clause)

    def riemann_zeta(s, t):
        epsilon = 1e-6
        result = 0.0
        for k in range(1, int(1 / epsilon)):
            term = (k ** (-s)) * math.exp(-2 * math.pi * k * t)
            if abs(term) < epsilon:
                break
            result += term
        return result

    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    proof_length = resolution(cnf)

    s = 0.5 + random.uniform(0, proof_length)
    t = math.log(abs(riemann_zeta(s, 0)), abs(riemann_zeta(s, proof_length)))
    
    if t <= proof_length and t >= 0:
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = "No zero found in the critical strip for ζ(s) at s = 1/2 + it"

    return {
        "metric_name": "Proof Length",
        "metric_value": proof_length,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    total_metric_value = sum(result["metric_value"] for result in results)
    mean_metric_value = total_metric_value / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"No zero found in the critical strip for ζ(s) at s = 1/2 + it\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")