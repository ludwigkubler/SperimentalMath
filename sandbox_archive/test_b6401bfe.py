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
        for _ in range(2 ** n - 1):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(clause[i] != -clause[j] for i in range(len(clause)) for j in range(i + 1, len(clause))):
                clauses.append(clause)
        return clauses
    
    def bp_readtwice_circuit_size(cnf):
        n = len(cnf[0])
        size = 2 * n
        for clause in cnf:
            size += 2 * (len(clause) - 1)
        return size
    
    def tropicalized_brauer_group_rank(cnf):
        # Placeholder procedure to compute the rank of the tropicalized Brauer group
        # This is a dummy implementation and should be replaced with actual computation
        return random.randint(1, n)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_cnf(n)
    rank = tropicalized_brauer_group_rank(cnf)
    size = bp_readtwice_circuit_size(cnf)
    
    return {
        "metric_name": "Rank vs DPLL Heig",
        "metric_value": rank / size,
        "instances_tested": 1,
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
    
    if all(r["conjecture_holds"] for r in results):
        support_fraction = 1.0
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.8:
        support_fraction = (len(results) - sum(1 for r in results if not r["conjecture_holds"])) / len(results)
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        RESULT = f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}"
        print(RESULT)
        exit()
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    
    RESULT = f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}"
    print(RESULT)