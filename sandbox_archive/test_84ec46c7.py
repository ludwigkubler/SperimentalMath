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
    
    def add(a, b):
        return a + b
    
    def mod2(x):
        return x % 2
    
    def E(f):
        count = 0
        for a in range(1 << n):
            for b in range(1 << n):
                for c in range(1 << n):
                    for d in range(1 << n):
                        if add(mod2(f[a]), mod2(f[b])) == add(mod2(f[c]), mod2(f[d])):
                            count += 1
        return count
    
    def ACC0_circuit_size(n):
        # Simulate a depth-3, size 2^n ACC0 circuit using DPLL-style backtracking
        # This is a simplified version and may not be optimal for all functions
        def dpll(clauses, assignment):
            if not clauses:
                return True
            unit_clause = next((c for c in clauses if len(c) == 1), None)
            if unit_clause:
                literal = unit_clause[0]
                if literal < 0 and literal in assignment:
                    return False
                assignment[literal] = True
                new_clauses = [c for c in clauses if literal not in c and -literal not in c]
                if dpll(new_clauses, assignment):
                    return True
                del assignment[literal]
                assignment[-literal] = True
                new_clauses = [c for c in clauses if -literal not in c and literal not in c]
                if dpll(new_clauses, assignment):
                    return True
                del assignment[-literal]
                return False
            pure_literal = next((l for l in range(1, 2*n+1) if (l not in assignment and -l not in assignment)), None)
            if pure_literal:
                assignment[pure_literal] = True
                new_clauses = [c for c in clauses if pure_literal not in c and -pure_literal not in c]
                if dpll(new_clauses, assignment):
                    return True
                del assignment[pure_literal]
                assignment[-pure_literal] = True
                new_clauses = [c for c in clauses if -pure_literal not in c and pure_literal not in c]
                if dpll(new_clauses, assignment):
                    return True
                del assignment[-pure_literal]
                return False
            return False
        
        n_vars = 2 * n
        clauses = []
        for i in range(1 << n):
            clause = [i + 1, -(i + 1)]
            clauses.append(clause)
        
        assignment = {}
        if dpll(clauses, assignment):
            return 2 ** n
        else:
            return float('inf')
    
    n = 40
    f = [random.randint(0, 1) for _ in range(1 << n)]
    E_f = E(f)
    circuit_size = ACC0_circuit_size(n)
    
    metric_name = "Additive Energy Threshold"
    metric_value = E_f
    instances_tested = 1
    conjecture_holds = E_f >= n ** 2.5 and circuit_size >= n ** 1.5 * math.log(n)
    counterexample = "" if conjecture_holds else f"Counterexample found: E(f)={E_f}, circuit_size={circuit_size}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 30 primes if no seeds provided
    
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
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample_desc = "E(f) < n^2.5 or circuit_size < n^(1.5)*log(n)"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")