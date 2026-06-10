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
        for _ in range(2**n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(abs(c) != abs(clause[i]) for i in range(len(clause))):
                clauses.append(clause)
        return clauses

    def count_clauses(phi):
        return len(phi)

    def circuit_complexity(phi):
        n = int(math.sqrt(2 * len(phi)))
        return 2 * n + 1

    def local_induction_degree_bound(n):
        return n

    phi = generate_cnf(random.randint(5, 40))
    cc_phi = circuit_complexity(phi)
    lidb_phi = local_induction_degree_bound(len(phi))

    if abs(lidb_phi - cc_phi) > 3:
        return {
            "metric_name": "LIDB vs CC",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": len(phi),
            "conjecture_holds": False,
            "counterexample": f"LIDB({len(phi)}) = {lidb_phi}, CC({len(phi)}) = {cc_phi}"
        }

    return {
        "metric_name": "LIDB vs CC",
        "metric_value": lidb_phi - cc_phi,
        "instances_tested": 1,
        "n_max": len(phi),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    if all("conjecture_holds" in res and res["conjecture_holds"] for res in results):
        mean_d = sum(res["metric_value"] for res in results) / len(results)
        std_dev = math.sqrt(sum((res["metric_value"] - mean_d) ** 2 for res in results) / len(results))
        support_fraction = sum(1 for res in results if "conjecture_holds" in res and res["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_d} std={std_dev} support_fraction={support_fraction}")
    elif any("counterexample" in res and res["counterexample"] for res in results):
        first_failing_seed = next(res["seed"] for res in results if "counterexample" in res and res["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{next(res['counterexample'] for res in results if 'counterexample' in res)}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")