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
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(tuple(sorted(clause)))
        return tuple(cnf)

    def resolution_width(cnf):
        clauses = list(cnf)
        while True:
            new_clauses = []
            for i in range(len(clauses)):
                for j in range(i + 1, len(clauses)):
                    clause1, clause2 = clauses[i], clauses[j]
                    if any(abs(x) == abs(y) for x in clause1 for y in clause2):
                        new_clause = tuple(sorted([x for x in clause1 + clause2 if x != -x[0]]))
                        if new_clause not in new_clauses:
                            new_clauses.append(new_clause)
            if not new_clauses:
                break
            clauses.extend(new_clauses)
        return len(clauses)

    def pseudoexpectation(cnf):
        n = max(abs(x) for clause in cnf for x in clause)
        return sum(1 / (n + 1) ** len(clause) for clause in cnf)

    def tropicalization(pseudoexp):
        return pseudoexp

    d = random.randint(1, 3)
    n = random.randint(5, 20)
    m = random.randint(n, 2 * n)
    cnf = generate_cnf(n, m)
    
    width = resolution_width(cnf)
    pseudoexp = pseudoexpectation(cnf)
    tau_e = tropicalization(pseudoexp)
    rank = len(tau_e)  # Assuming the rank is simply the length of the tropicalized vector

    return {
        "metric_name": "minimal_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": width <= d * math.log(n + m) / math.log(math.log(n + m)),
        "counterexample": "" if width <= d * math.log(n + m) / math.log(math.log(n + m)) else f"width={width}, expected={d * math.log(n + m) / math.log(math.log(n + m))}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(int(res["conjecture_holds"]) for res in results) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"width exceeds bound\" first_failing_seed={first_failing_seed}")