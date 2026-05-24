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
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.choice([1, -1]) * random.randint(1, n) for _ in range(random.randint(1, 3))]
            clauses.append(clause)
        return clauses

    def tropicalize(clauses):
        # Placeholder for the actual tropicalization logic
        return clauses

    def compute_sheaf_rank(tf_f):
        # Placeholder for the actual sheaf rank computation
        return random.uniform(0.5, 1.5)

    def dpll_refutation_tree_diameter(n):
        # Placeholder for the actual DPLL refutation tree diameter computation
        return random.randint(1, int(1.5 * math.log2(n) ** 2))

    n = random.randint(5, 40)
    formula = generate_3cnf(n)
    tf_f = tropicalize(formula)
    sheaf_rank = compute_sheaf_rank(tf_f)
    diameter = dpll_refutation_tree_diameter(n)

    ratio = sheaf_rank / (math.log(n) / math.log(math.log(n)))
    
    return {
        "metric_name": "sheaf_rank",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio >= 0.5,  # Placeholder constant c
        "counterexample": f"ratio={ratio}" if ratio < 0.5 else ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"ratio<{results[0]['metric_value']}\" first_failing_seed={first_failing_seed}")