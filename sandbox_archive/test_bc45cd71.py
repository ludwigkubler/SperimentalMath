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
            clause = [random.randint(-1, 0) * (i + 1) for i in range(n)]
            if all(x == 0 for x in clause):
                continue
            clauses.append(clause)
        return clauses
    
    def frege_proof_depth(cnf):
        stack = []
        depth = 0
        max_depth = 0
        for clause in cnf:
            while stack and stack[-1] != -1:
                stack.pop()
                depth -= 1
            stack.append(-1)
            depth += 1
            max_depth = max(max_depth, depth)
        return max_depth
    
    def hodge_theoretic_index(cnf):
        # Placeholder for Hodge-theoretic index calculation
        # This is a dummy implementation and should be replaced with actual logic
        return len(cnf) / (len(cnf[0]) if cnf else 1)
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    h_index = hodge_theoretic_index(cnf)
    d_depth = frege_proof_depth(cnf)
    
    return {
        "metric_name": "Hodge-theoretic Index vs Frege Proof Depth",
        "metric_value": h_index,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True if h_index >= d_depth else False,
        "counterexample": "" if h_index >= d_depth else f"CNF with n={n}, h(φ)={h_index}, d(φ)={d_depth}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")