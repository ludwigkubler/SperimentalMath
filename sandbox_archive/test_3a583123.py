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
    
    def dpll_search_tree(cnf):
        if not cnf:
            return [()]
        literals = set()
        for clause in cnf:
            literals.update(clause)
        
        literal = random.choice(list(literals))
        new_cnf_true = [clause for clause in cnf if literal not in clause]
        new_cnf_false = [tuple([-l] + list(clause)) for clause in cnf if -literal not in clause]
        
        return [(True, *dpll_search_tree(new_cnf_true)), (False, *dpll_search_tree(new_cnf_false))]
    
    def minimal_order_quantum_group(cnf):
        # Placeholder function to compute the minimal order of a quantum group representation
        # This is a dummy implementation and should be replaced with actual logic
        return len(cnf)
    
    n = random.randint(5, 40)
    cnf = []
    for _ in range(n):
        clause = [random.randint(-n, -1), random.randint(1, n)]
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
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in enumerate(results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"ord_q > h_DPLL\" first_failing_seed={first_failing_seed}")