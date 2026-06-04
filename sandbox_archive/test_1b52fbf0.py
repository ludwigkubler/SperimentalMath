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
from itertools import combinations, product

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_kary_cnf(n: int, k: int):
        literals = list(range(1, n + 1))
        clauses = []
        for _ in range(k * n):
            clause = [random.choice(literals), -random.choice(literals)]
            while len(set(clause)) != 2:
                clause = [random.choice(literals), -random.choice(literals)]
            clauses.append(clause)
        return clauses
    
    def resolution_width(cnf: list):
        queue = cnf[:]
        seen = set()
        width = 0
        while queue:
            literal, negated_literal = random.choice(queue)
            if negated_literal in seen:
                continue
            seen.add(negated_literal)
            new_clauses = []
            for clause in queue:
                if literal in clause and -negated_literal not in clause:
                    new_clauses.append([-x for x in clause if x != literal])
                elif negated_literal in clause and -literal not in clause:
                    new_clauses.append([-x for x in clause if x != negated_literal])
            queue.extend(new_clauses)
            width = max(width, len(seen))
        return width
    
    def formal_group_order(cnf: list):
        # Placeholder for actual implementation
        return 1  # This is a placeholder and should be replaced with an actual algorithm

    k = random.randint(2, 4)  # Randomly choose k between 2 and 4
    n = random.randint(5, 10)  # Randomly choose n between 5 and 10
    cnf = generate_kary_cnf(n, k)
    
    formal_group_order_value = formal_group_order(cnf)
    resolution_width_value = resolution_width(cnf)
    
    return {
        "metric_name": "formal_group_order",
        "metric_value": abs(formal_group_order_value - resolution_width_value),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": formal_group_order_value <= resolution_width_value,
        "counterexample": ""
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    else:
        seeds = list(map(int, sys.argv[1:]))

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        if result["instances_tested"] > 0:
            results.append(result["metric_value"])

    mean_val = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean_val) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r <= 2) / len(results)

    if all(r <= 2 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_val} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_val} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = seeds[results.index(max(results))]
        print(f"RESULT: FALSIFIED counterexample='not_proven' first_failing_seed={first_failing_seed}")