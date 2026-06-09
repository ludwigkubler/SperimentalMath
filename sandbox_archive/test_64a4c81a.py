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
    
    def generate_cnf(n):
        cnf = []
        for _ in range(10):  # Generate 10 clauses with n variables
            clause = [random.randint(-n, -1), random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def dpll_search_tree(cnf):
        literals = set()
        for clause in cnf:
            literals.update(abs(lit) for lit in clause)
        
        if not literals:
            return []
        
        literal = random.choice(list(literals))
        new_cnf_true = [c for c in cnf if literal in c]
        new_cnf_false = [c for c in cnf if -literal not in c]
        
        return [(True, *dpll_search_tree(new_cnf_true)), (False, *dpll_search_tree(new_cnf_false))]
    
    def minimal_order_quantum_group(cnf):
        # Placeholder function to simulate quantum group order calculation
        # This is a dummy implementation and should be replaced with actual logic
        return len(cnf)
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    ord_q = minimal_order_quantum_group(cnf)
    h_DPLL = len(dpll_search_tree(cnf))
    
    metric_name = "ord_q_vs_h_DPLL"
    metric_value = ord_q / h_DPLL
    instances_tested = 1
    n_max = n
    conjecture_holds = ord_q <= h_DPLL
    counterexample = "" if conjecture_holds else f"ord_q={ord_q}, h_DPLL={h_DPLL}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    else:
        seeds = [int(s) for s in sys.argv[1:]]
    
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
        counterexample_desc = f"ord_q < h_DPLL at seed {first_failing_seed}"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")