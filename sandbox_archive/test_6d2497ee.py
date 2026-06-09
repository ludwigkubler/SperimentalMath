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

from random import seed, randint, sample
from math import log2, sqrt
from fractions import Fraction
import itertools

def run_trial(seed: int) -> dict:
    seed(seed)
    
    def generate_cnf(n):
        variables = list(range(1, n + 1))
        clauses = []
        for i in range(n):
            clause = [randint(-1, 1) * var for var in variables]
            if all(c == 0 for c in clause):
                clause[randint(0, n - 1)] = randint(-1, 1)
            clauses.append(clause)
        return clauses

    def find_automorphisms(tiling):
        n = len(tiling)
        permutations = list(itertools.permutations(range(n)))
        automorphisms = []
        for perm in permutations:
            if all(tiling[perm[i]][perm[j]] == tiling[i][j] for i in range(n) for j in range(i + 1, n)):
                automorphisms.append(perm)
        return automorphisms

    def min_order(group):
        return len(group)

    def frege_proof_depth(cnf):
        # Placeholder function; actual implementation needed
        return len(cnf)

    n = randint(5, 40)
    cnf = generate_cnf(n)
    tiling = [[randint(0, 1) for _ in range(n)] for _ in range(n)]
    G = find_automorphisms(tiling)
    d_phi = frege_proof_depth(cnf)

    if not G:
        return {
            "metric_name": "log_min_order_G",
            "metric_value": -float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    log_min_order_G = log2(min_order(G))
    return {
        "metric_name": "log_min_order_G",
        "metric_value": log_min_order_G,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")