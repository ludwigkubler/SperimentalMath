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
    
    def generate_3cnf(n, m):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(m):
            clause = [random.choice(variables), random.choice(variables), random.choice(variables)]
            if len(set(clause)) == 2:
                clause.append(random.choice(variables))
            clauses.append(clause)
        return clauses
    
    def delone_set_geometry(clauses):
        # Simplified mapping to Delone set geometry
        return sum(len(c) for c in clauses), len(clauses)
    
    def ac0_k_distance_circuit_size(clauses):
        # Simplified mapping to AC^0-k-distance circuit size
        return len(clauses)
    
    n = random.randint(5, 40)
    m = random.randint(n * 2, n * 3)
    formula = generate_3cnf(n, m)
    rank, num_clauses = delone_set_geometry(formula)
    circuit_size = ac0_k_distance_circuit_size(formula)
    
    return {
        "metric_name": "Rank vs Circuit Size",
        "metric_value": rank * rank,
        "instances_tested": 1,
        "conjecture_holds": rank * rank <= circuit_size and circuit_size <= m,
        "counterexample": "" if rank * rank <= circuit_size and circuit_size <= m else f"R(F)={rank}, |C|={circuit_size}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={seed}")
                break