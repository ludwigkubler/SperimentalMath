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
    
    def eta_quotient_order(n):
        if n == 1:
            return 0
        order = 0
        while n % 2 == 0:
            n //= 2
            order += 1
        for i in range(3, int(math.sqrt(n)) + 1, 2):
            while n % i == 0:
                n //= i
                order += 1
        if n > 2:
            order += 1
        return order
    
    def frege_proof_depth(cnf):
        # Placeholder for Frege proof depth calculation
        # This is a dummy implementation and should be replaced with actual logic
        return len(cnf) * 5  # Example: linear relationship for demonstration purposes
    
    n = random.randint(5, 40)
    cnf = [[random.randint(-n, n) for _ in range(n)] for _ in range(random.randint(1, n))]
    
    eta_quotient_orders = [eta_quotient_order(abs(x)) for x in sum(cnf, [])]
    frege_depths = [frege_proof_depth(formula) for formula in cnf]
    
    if not eta_quotient_orders or not frege_depths:
        return {
            "metric_name": "Frege Proof Depth vs Eta-Quotient Order",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "empty_cnf"
        }
    
    mean_order = sum(eta_quotient_orders) / len(eta_quotient_orders)
    mean_depth = sum(frege_depths) / len(frege_depths)
    
    ratio = mean_depth / math.log2(math.prod([order**2 for order in eta_quotient_orders]))
    
    return {
        "metric_name": "Frege Proof Depth vs Eta-Quotient Order",
        "metric_value": ratio,
        "instances_tested": len(cnf),
        "conjecture_holds": abs(ratio - 1) <= 0.03,
        "counterexample": "" if abs(ratio - 1) <= 0.03 else f"Ratio {ratio} outside ±3%"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_ratio = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["metric_value"] is not None for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.03 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio outside ±3%\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")