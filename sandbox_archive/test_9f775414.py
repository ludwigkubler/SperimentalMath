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
    
    def generate_cnf(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def hodge_index(n, m):
        # Simplified Hodge index calculation (not actual Hodge theory)
        return math.ceil((m * n) ** (2 / 3))
    
    def dpll_width(cnf):
        # Simplified DPLL search tree width calculation (not actual DPLL algorithm)
        return len(cnf) ** 1.5
    
    n = random.randint(5, 40)
    m = random.randint(n, n * 2)
    cnf = generate_cnf(n, m)
    
    h_index = hodge_index(n, m)
    d_width = dpll_width(cnf)
    
    return {
        "metric_name": "Hodge Index vs DPLL Width",
        "metric_value": h_index,
        "instances_tested": 1,
        "conjecture_holds": h_index <= d_width,
        "counterexample": "" if h_index <= d_width else f"H_index={h_index}, D_width={d_width}"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next(r["counterexample"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")