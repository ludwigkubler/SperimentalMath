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
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if not any(clause[i] == -clause[j] for i in range(n) for j in range(i + 1, n)):
                clauses.append(clause)
        return clauses
    
    def tropical_convex_hull(clauses):
        # Placeholder for actual implementation
        return len(clauses)
    
    def acc0_circuit_size(clauses):
        # Placeholder for actual implementation
        return len(clauses) * 2
    
    n = random.randint(5, 40)
    clauses = generate_3cnf(n)
    hull_dimension = tropical_convex_hull(clauses)
    circuit_size = acc0_circuit_size(clauses)
    
    if hull_dimension == math.log(n, 2):
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = "mapping_undefined"
    
    return {
        "metric_name": "hull_dimension",
        "metric_value": hull_dimension,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2%}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")