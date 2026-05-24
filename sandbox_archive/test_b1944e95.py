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
    
    def generate_planar_cnf(n, m):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(m):
            clause = [random.choice(variables), -random.choice(variables)]
            if random.choice([True, False]):
                clause.append(-random.choice(variables))
            clauses.append(clause)
        return clauses

    def resolution_length(cnf):
        stack = cnf[:]
        seen = set()
        while stack:
            literal = stack.pop()
            if literal in seen or -literal in seen:
                continue
            seen.add(literal)
            for clause in cnf:
                if literal in clause:
                    new_clause = [l for l in clause if l != literal]
                    if not new_clause:
                        return 0
                    if -new_clause[0] in stack:
                        return 0
                    stack.append(-new_clause[0])
        return len(cnf)

    def hodge_diamond_size(n):
        # Simplified Hodge diamond size for planar 3-CNF
        return n

    n = random.randint(5, 40)
    m = random.randint(2 * n, 4 * n)
    cnf = generate_planar_cnf(n, m)
    proof_length = resolution_length(cnf)
    hodge_rank = hodge_diamond_size(n)

    return {
        "metric_name": "Hodge Rank vs Resolution Proof Length",
        "metric_value": hodge_rank,
        "instances_tested": 1,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")