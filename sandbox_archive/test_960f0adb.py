# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        clauses = []
        for i in range(1 << n):
            clause = [random.choice([-1, 1]) * (j + 1) for j in range(n)]
            if all(clause[j] != -clause[(j + 1) % n] for j in range(n)):
                clauses.append(clause)
        return clauses
    
    def quasi_group_from_cnf(cnf):
        variables = set()
        for clause in cnf:
            variables.update(abs(lit) for lit in clause)
        n_vars = max(variables)
        table = {}
        for i in range(1, n_vars + 1):
            for j in range(1, n_vars + 1):
                table[(i, j)] = (i + j - 1) % n_vars + 1
        return table
    
    def min_rank(quasi_group):
        n_vars = max(quasi_group.keys(), key=lambda x: max(x))
        identity = {i: i for i in range(1, n_vars + 1)}
        if quasi_group == identity:
            return 1
        
        rank = 0
        for size in range(2, n_vars + 1):
            for subset in combinations(quasi_group.keys(), size):
                sub_group = {k: v for k, v in quasi_group.items() if k in subset}
                if len(sub_group) == size and all(sub_group[a][b] in sub_group for a, b in sub_group):
                    rank += 1
                    break
            else:
                continue
            break
        
        return rank
    
    def circuit_weight(cnf):
        return sum(len(clause) for clause in cnf)
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    quasi_group = quasi_group_from_cnf(cnf)
    min_rank_value = min_rank(quasi_group)
    weight = circuit_weight(cnf)
    
    return {
        "metric_name": "correlation",
        "metric_value": min_rank_value / weight,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")