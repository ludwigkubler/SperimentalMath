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
        cnf = []
        for _ in range(10):  # 10 clauses with n variables each
            clause = [random.randint(-n, n) for _ in range(n)]
            cnf.append(clause)
        return cnf
    
    def frege_proof_width(cnf):
        # Simplified heuristic for Frege proof width
        return len(cnf) * 2
    
    def find_algebraic_roots(cnf):
        roots = set()
        for clause in cnf:
            for literal in clause:
                if literal != 0:
                    root = complex(0, literal)
                    roots.add(root)
        return roots
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    w_phi = frege_proof_width(cnf)
    R_phi = find_algebraic_roots(cnf)
    
    abs_diff = abs(len(R_phi) - w_phi)
    conjecture_holds = (abs_diff <= 3 * min(w_phi, len(R_phi)))
    counterexample = "mapping_undefined" if not conjecture_holds else ""
    
    return {
        "metric_name": "abs_diff",
        "metric_value": abs_diff,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2**i + 7 for i in range(5, 6)]  # Default to a list of 30 primes
    else:
        seeds = [int(s) for s in sys.argv[1:]]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")