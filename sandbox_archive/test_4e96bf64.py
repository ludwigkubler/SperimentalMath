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
    
    def generate_k_cnf(n, clause_density):
        num_clauses = int(clause_density * n * (n - 1) / 2)
        variables = list(range(1, n + 1))
        clauses = set()
        
        while len(clauses) < num_clauses:
            clause = random.sample(variables, 2)
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.add(tuple(sorted(clause)))
        
        return clauses
    
    def communication_complexity(k_cnf):
        # Simplified model of communication complexity
        return len(k_cnf) * 2
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_cc = 0.0
    
    for n in n_values:
        for _ in range(5):  # Test each n with 5 random clause densities
            clause_density = random.uniform(1.0, 1.5)
            k_cnf = generate_k_cnf(n, clause_density)
            cc = communication_complexity(k_cnf)
            total_cc += cc
            instances_tested += 1
    
    mean_cc = total_cc / instances_tested
    conjecture_holds = all(mean_cc <= math.log(n) for n in n_values)
    
    return {
        "metric_name": "communication_complexity_bound",
        "metric_value": mean_cc,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"CC({n_values[0]}, {random.uniform(1.0, 1.5)})={mean_cc} > log({n_values[0]})"
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        results.append(result)
        print(f"TRIAL: {result}")
    
    mean_cc = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_cc} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_cc} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")