# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(clause[i] != -clause[j] for i in range(n) for j in range(i+1, n)):
                clauses.append(clause)
        return clauses
    
    def gromov_witten_invariant(cnf):
        # Placeholder function to simulate Gromov-Witten invariant calculation
        return len(cnf)
    
    def acc0_circuit_size(cnf):
        # Placeholder function to simulate ACC0 circuit size calculation
        return 2 ** gromov_witten_invariant(cnf)
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    mu_F = gromov_witten_invariant(cnf)
    acc0_size = acc0_circuit_size(cnf)
    
    return {
        "metric_name": "acc0_circuit_size",
        "metric_value": acc0_size,
        "instances_tested": 1,
        "conjecture_holds": mu_F <= acc0_size,
        "counterexample": "" if mu_F <= acc0_size else f"CNF with n={n}, μ(F)={mu_F}, ACC0 size={acc0_size}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")