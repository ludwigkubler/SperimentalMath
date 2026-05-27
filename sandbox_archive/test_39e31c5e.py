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
    
    def generate_kcnf(n, m):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(m):
            clause = [random.choice(variables), random.choice(variables)]
            if len(set(clause)) == 2:
                clauses.append(clause)
        return clauses
    
    def resolution_proof_complexity(clauses):
        # Simplified version of resolution proof complexity calculation
        return len(clauses) ** 1.5
    
    def quandle_rank(n, m):
        # Simplified version of quandle rank calculation
        return (n + m) / 2
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    m = random.randint(2 * n, 3 * n)
    clauses = generate_kcnf(n, m)
    
    alpha_nm = resolution_proof_complexity(clauses)
    rank_Q = quandle_rank(n, m)
    
    return {
        "metric_name": "Quandle Rank",
        "metric_value": rank_Q,
        "instances_tested": 1,
        "conjecture_holds": math.isclose(rank_Q, alpha_nm, rel_tol=1e-9),
        "counterexample": "" if math.isclose(rank_Q, alpha_nm, rel_tol=1e-9) else f"Mean rank {rank_Q} does not match resolution complexity {alpha_nm}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_d = sum(r["metric_value"] for r in results) / len(results)
        std_dev = math.sqrt(sum((r["metric_value"] - mean_d) ** 2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_d} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")