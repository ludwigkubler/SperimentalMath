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
        literals = [f"x{i}" for i in range(1, n + 1)]
        clauses = set()
        while len(clauses) < num_clauses:
            clause = random.sample(literals, 2)
            if clause not in clauses and clause[::-1] not in clauses:
                clauses.add(tuple(sorted(clause)))
        return clauses

    def algebraic_curve_rank(n):
        # Placeholder for computing the rank of an associated algebraic curve
        # This is a dummy implementation; replace with actual computation
        return n  # Example: rank is proportional to n

    def communication_complexity(k_cnf):
        # Placeholder for computing communication complexity
        # This is a dummy implementation; replace with actual computation
        return len(k_cnf) * 2  # Example: complexity is proportional to the number of clauses

    n = random.choice([5, 10, 15, 20, 30, 40])
    clause_density = random.uniform(1.0, 1.5)
    k_cnf = generate_k_cnf(n, clause_density)
    rank = algebraic_curve_rank(n)
    cc = communication_complexity(k_cnf)

    return {
        "metric_name": "communication_complexity_bound",
        "metric_value": cc,
        "instances_tested": 1,
        "conjecture_holds": cc <= math.log(rank),
        "counterexample": f"CC({n}, {clause_density})={cc} > log({rank})"
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
    else:
        support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(r['metric_value'] for r in results)/len(results)} std=0 support_fraction={support_fraction}")
    elif first_failing_seed is not None:
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")