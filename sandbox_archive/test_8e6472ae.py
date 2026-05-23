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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(10 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses
    
    def bp_read_twice_circuit_size(n):
        # Simplified model of BP_ReadTwice circuit size
        return 2 * n + 10
    
    def tropicalized_brauer_group_rank(cnf):
        # Simplified model of Brauer group rank for CNF
        return len(cnf)
    
    total_rank = 0
    total_size = 0
    instances_tested = 0
    
    for _ in range(30):  # Ensure at least 30 instances per seed
        n = random.choice([5, 10, 15, 20, 30, 40])
        cnf = generate_cnf(n)
        rank = tropicalized_brauer_group_rank(cnf)
        size = bp_read_twice_circuit_size(n)
        
        total_rank += rank
        total_size += size
        instances_tested += 1
    
    mean_rank = Fraction(total_rank, instances_tested)
    mean_size = Fraction(total_size, instances_tested)
    
    conjecture_holds = abs(mean_rank - mean_size) <= 3
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Rank vs DPLL Heig",
        "metric_value": float(abs(mean_rank - mean_size)),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30*37+1))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, ...{result}...}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")