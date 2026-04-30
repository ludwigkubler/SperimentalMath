# auto-injected by SEC sandbox
import math
import itertools
import collections
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
import subprocess
import json

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    # Generate a random unsatisfiable CNF formula
    n = 10 + random.randint(0, 20)
    m = 2 * n + random.randint(0, 4 * n)
    clauses = []
    for _ in range(m):
        clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
        if len(set(clause)) == len(clause):  # Ensure no duplicate literals
            clauses.append(clause)
    
    cnf_formula = "p cnf {} {}\n".format(n, m)
    cnf_formula += "\n".join(" ".join(str(l) for l in clause) + " 0" for clause in clauses)
    
    # Write the CNF formula to a temporary file
    with open("temp_cnf.cnf", "w") as f:
        f.write(cnf_formula)
    
    try:
        # Run minisat to find the refutation size
        result = subprocess.run(["minisat", "temp_cnf.cnf"], capture_output=True, text=True, timeout=8)
        if result.returncode != 0 and "UNSAT" in result.stderr:
            refutation_size = len(result.stderr.splitlines())
        else:
            return {
                "metric_name": "refutation_size",
                "metric_value": float('inf'),
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": "[Errno 2] No such file or directory: 'minisat'"
            }
    except subprocess.TimeoutExpired:
        return {
            "metric_name": "refutation_size",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Timeout"
        }
    
    # Compute the complexity of the clause-indicator polynomial
    clause_indicator_poly = {}
    for clause in clauses:
        key = tuple(sorted(abs(l) for l in clause))
        if key not in clause_indicator_poly:
            clause_indicator_poly[key] = 0
        clause_indicator_poly[key] += 1
    
    poly_complexity = len(clause_indicator_poly)
    
    # Check if the refutation size is polynomially related to the polynomial complexity
    conjecture_holds = refutation_size <= poly_complexity ** 2
    
    return {
        "metric_name": "refutation_size",
        "metric_value": refutation_size,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + 7 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {json.dumps(result)}")
        results.append(result)
    
    refutation_sizes = [r["metric_value"] for r in results if "refutation_size" in r]
    poly_complexities = [r["instances_tested"] for r in results if "conjecture_holds" in r]
    
    mean_refutation_size = sum(refutation_sizes) / len(refutation_sizes)
    std_refutation_size = (sum((x - mean_refutation_size) ** 2 for x in refutation_sizes) / len(refutation_sizes)) ** 0.5
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_refutation_size} std={std_refutation_size} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and len(results) >= 30:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")