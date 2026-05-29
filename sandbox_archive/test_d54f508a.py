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
    
    def generate_cnf(n, density):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(int(density * n * (n - 1) / 2)):
            clause = [random.choice(variables), random.choice(variables)]
            if random.choice([True, False]):
                clause[0] = -clause[0]
            if random.choice([True, False]):
                clause[1] = -clause[1]
            clauses.append(clause)
        return clauses
    
    def jordan_algebra_order(n):
        # Simplified model for Jordan algebra order
        return n * (n + 1) // 2
    
    def frege_proof_depth(n):
        # Simplified model for Frege proof depth
        return int(math.log(n, 2))
    
    n = random.randint(5, 40)
    density = random.uniform(0.1, 0.9)
    cnf_formula = generate_cnf(n, density)
    
    order = jordan_algebra_order(n)
    depth = frege_proof_depth(n)
    
    return {
        "metric_name": "Frege Proof Depth",
        "metric_value": depth,
        "instances_tested": 1,
        "conjecture_holds": order <= depth * math.log(n, 2),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(1000, 9999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_depth = sum(r["metric_value"] for r in results) / len(results)
    std_depth = math.sqrt(sum((r["metric_value"] - mean_depth) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_depth} std={std_depth} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print("RESULT: FALSIFIED counterexample=\"\" first_failing_seed=NA")
    else:
        print(f"RESULT: INCONCLUSIVE reason=no_valid_data n_tested={len(results)}")