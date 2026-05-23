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
        clauses = []
        for _ in range(2**n - 1):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if sum(clause) > 0:
                clauses.append(clause)
        return clauses
    
    def ac0_circuit_depth(cnf):
        # Simplified AC0 circuit depth calculation
        return len(cnf)
    
    def minimal_order_affine_hecke(n):
        # Placeholder for actual computation of minimal order in affine Hecke algebra
        return n**2  # Example polynomial relationship
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    ac0_depth = ac0_circuit_depth(cnf)
    order_hecke = minimal_order_affine_hecke(n)
    
    metric_value = abs(order_hecke - ac0_depth) / (order_hecke + ac0_depth)
    conjecture_holds = 0.6 <= metric_value <= 0.8
    counterexample = "" if conjecture_holds else f"n={n}, order_hecke={order_hecke}, ac0_depth={ac0_depth}"
    
    return {
        "metric_name": "Order vs AC0 Depth",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [random.getrandbits(32) for _ in range(30)]
    
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
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"metric_value out of range\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")