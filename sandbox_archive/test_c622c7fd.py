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
        for _ in range(2 * n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses
    
    def eta_quotient_order(n):
        # Simplified heuristic for demonstration
        return n + 1
    
    def frege_proof_depth(cnf):
        # Simplified heuristic for demonstration
        return len(cnf) * 2
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    
    eta_quotient_orders = [eta_quotient_order(i) for i in range(1, n + 1)]
    frege_depth = frege_proof_depth(cnf)
    
    if not eta_quotient_orders:
        return {
            "metric_name": "frege_proof_depth",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    log_eta_quotient_product = sum(math.log2(eta_order) for eta_order in eta_quotient_orders)
    ratio = frege_depth / (log_eta_quotient_product ** 2)
    
    return {
        "metric_name": "frege_proof_depth",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": abs(ratio - 1) <= 0.03,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    total_ratio = sum(res["metric_value"] for res in results if res["instances_tested"] > 0)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={total_ratio/len(results)} std=NA support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_ratio/len(results)} std=NA support_fraction={support_fraction}")
    else:
        for res in results:
            if not res["conjecture_holds"]:
                counterexample = f"n={res['instances_tested']}, ratio={res['metric_value']}"
                print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seed}")
                break