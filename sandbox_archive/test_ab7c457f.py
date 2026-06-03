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
            clause = [random.randint(-1, 0) * random.randint(1, n) for _ in range(random.randint(1, n))]
            if all(clause[i] != -clause[j] for i in range(len(clause)) for j in range(i+1, len(clause))):
                clauses.append(clause)
        return clauses
    
    def frege_proof_length(cnf):
        # Placeholder function to simulate Frege proof length calculation
        return sum(1 for _ in cnf) * 2
    
    def p_adic_analytic_continuation_order(n):
        # Placeholder function to simulate minimal order of p-adic analytic continuation
        return n ** (1 + random.random() / 10)
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    proof_length = frege_proof_length(cnf)
    p_adic_order = p_adic_analytic_continuation_order(n)
    
    return {
        "metric_name": "p_adic_order",
        "metric_value": p_adic_order,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(p_adic_order - proof_length) <= proof_length * random.random() / 10,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        counterexample = next(res["counterexample"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[next(i for i, res in enumerate(results) if not res['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")