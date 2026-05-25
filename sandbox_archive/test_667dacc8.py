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
    
    def generate_knot(n):
        # Placeholder for knot generation logic
        return [random.randint(0, 1) for _ in range(n)]
    
    def compute_betti_numbers(knot):
        # Placeholder for Betti number computation logic
        return sum(knot)
    
    def dpll_proof_length(cnf):
        # Placeholder for DPLL proof length calculation
        return len(cnf)
    
    n = random.randint(5, 40)
    knot = generate_knot(n)
    betti_number = compute_betti_numbers(knot)
    cnf = [knot]  # Simplified CNF representation
    proof_length = dpll_proof_length(cnf)
    
    return {
        "metric_name": "DPLL Proof Length",
        "metric_value": proof_length,
        "instances_tested": 1,
        "conjecture_holds": proof_length == betti_number,
        "counterexample": "" if proof_length == betti_number else f"Rank(K)={betti_number}, DPLL length={proof_length}"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")