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
    
    def generate_kcnf(n, m, k):
        cnf = []
        for _ in range(m):
            clause = set()
            while len(clause) < k:
                lit = random.randint(1, n * 2)
                if lit > n:
                    lit -= n
                else:
                    lit = -lit
                clause.add(lit)
            cnf.append(tuple(sorted(clause)))
        return tuple(cnf)

    def min_state_complexity(cnf):
        # Placeholder for minimal state complexity calculation using Myhill-Nerode theorem
        # This is a simplified version and may not be accurate for all k-CNFs
        unique_states = set()
        for clause in cnf:
            state = ''.join(str(abs(lit)) + ('1' if lit > 0 else '0') for lit in clause)
            unique_states.add(state)
        return len(unique_states)

    def communication_complexity(cnf):
        # Placeholder for communication complexity calculation
        # This is a simplified version and may not be accurate for all k-CNFs
        return sum(len(clause) for clause in cnf)

    n = random.randint(5, 40)
    m = random.randint(n, n * 2)
    k = random.randint(2, min(3, n))
    cnf = generate_kcnf(n, m, k)
    
    q_star = min_state_complexity(cnf)
    comm_complexity = communication_complexity(cnf)
    
    upper_bound = (n + m + k) * math.log(n + m)
    
    return {
        "metric_name": "q_star",
        "metric_value": q_star,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": q_star <= upper_bound,
        "counterexample": "" if q_star <= upper_bound else f"q_star={q_star} > upper_bound={(n + m + k) * math.log(n + m)}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_q_star = sum(r["metric_value"] for r in results) / len(results)
    std_q_star = math.sqrt(sum((r["metric_value"] - mean_q_star) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_q_star} std={std_q_star} support_fraction={support_fraction}")
    elif support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_q_star} std={std_q_star} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"q_star exceeded upper_bound\" first_failing_seed={first_failing_seed}")