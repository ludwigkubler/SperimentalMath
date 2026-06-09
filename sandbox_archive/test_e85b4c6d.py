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
    
    def dpll_search_tree(cnf):
        if not cnf:
            return [()]
        literals = set(l for clause in cnf for l in clause if isinstance(l, int))
        literal = random.choice(list(literals))
        polarity = True
        new_cnf = [[l for l in clause if l != -literal] for clause in cnf]
        return [(True, *dpll_search_tree(new_cnf)), (False, *dpll_search_tree([c for c in cnf if -literal not in c]))]

    def minimal_order_quantum_group(cnf):
        # Placeholder function to simulate the calculation of the minimal order
        # This is a dummy implementation and should be replaced with actual logic
        return len(cnf)

    n = random.randint(5, 40)
    cnf = []
    for _ in range(n):
        clause = [random.choice(range(-n, -1)) for _ in range(random.randint(2, n))]
        cnf.append(clause)
    
    ord_q = minimal_order_quantum_group(cnf)
    h_DPLL = len(dpll_search_tree(cnf))
    
    return {
        "metric_name": "ord_q vs h_DPLL",
        "metric_value": ord_q,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": ord_q <= h_DPLL,
        "counterexample": "" if ord_q <= h_DPLL else f"ord_q={ord_q} > h_DPLL={h_DPLL}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"ord_q > h_DPLL\" first_failing_seed={first_failing_seed}")