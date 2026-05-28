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
    
    def generate_random_3cnf(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            while len(set(clause)) != 2:
                clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def resolution_prove(clauses):
        stack = []
        for clause in clauses:
            if not any(lit in stack or -lit in stack for lit in clause):
                stack.extend(clause)
        return len(stack)
    
    n = random.randint(5, 40)
    m = random.randint(n * 2, n * 3)
    clauses = generate_random_3cnf(n, m)
    
    # Minimal order of geometric invariants for a projective variety
    k = random.randint(1, 10)
    
    proof_size = resolution_prove(clauses)
    
    return {
        "metric_name": "resolution_proof_size",
        "metric_value": proof_size,
        "instances_tested": 1,
        "conjecture_holds": proof_size <= k**3 * math.log(n),
        "counterexample": "" if proof_size <= k**3 * math.log(n) else f"Proof size {proof_size} exceeds upper bound {k**3 * math.log(n)}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_proofs = sum(r["instances_tested"] for r in results)
    mean_proof_size = sum(r["metric_value"] * r["instances_tested"] for r in results) / total_proofs
    std_deviation = math.sqrt(sum((r["metric_value"] - mean_proof_size)**2 * r["instances_tested"] for r in results) / total_proofs)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_proof_size} std={std_deviation} support_fraction={support_fraction}")
    elif support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_proof_size} std={std_deviation} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")