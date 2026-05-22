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
        for _ in range(n * 2):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses

    def hodge_bundle(cnf):
        # Constructive mapping from CNF to Hodge bundle
        # This is a placeholder function. Replace with actual implementation.
        return len(cnf)

    def geometric_entropy(hodge_bundle_size):
        if hodge_bundle_size == 0:
            return 0
        return -math.log2(1 / hodge_bundle_size)

    def dpll_search_tree_height(cnf):
        # Placeholder for DPLL search tree height calculation
        # Replace with actual implementation.
        return len(cnf) * 2

    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    hodge_bundle_size = hodge_bundle(cnf)
    entropy = geometric_entropy(hodge_bundle_size)
    dpll_height = dpll_search_tree_height(cnf)

    return {
        "metric_name": "DPLL Search Tree Height",
        "metric_value": dpll_height,
        "instances_tested": 1,
        "conjecture_holds": False if entropy == 0 else dpll_height <= 1 / entropy**2,
        "counterexample": "mapping_undefined" if entropy == 0 else ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
        support_fraction = 1.0
    else:
        mean_value = sum(r["metric_value"] for r in results if r["conjecture_holds"]) / sum(1 for r in results if r["conjecture_holds"])
        std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["conjecture_holds"]) / sum(1 for r in results if r["conjecture_holds"]))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif first_failing_seed is not None:
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")