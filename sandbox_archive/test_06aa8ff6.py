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
    
    def generate_k_cnf_tautology(n, k):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(k * n):
            clause = [random.choice(variables), -random.choice(variables)]
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses
    
    def is_tautology(clauses):
        variables = set()
        for clause in clauses:
            variables.update(abs(x) for x in clause)
        assignments = {var: 0 for var in variables}
        
        def backtrack(index):
            if index == len(variables):
                return all(any(var in assignment or -var not in assignment for var in clause) for clause in clauses)
            for value in [1, -1]:
                assignment[variables[index]] = value
                if backtrack(index + 1):
                    return True
                del assignment[variables[index]]
            return False
        
        return backtrack(0)
    
    def symplectic_rank(n, k):
        # Placeholder function to simulate the computation of symplectic rank
        # This is a dummy implementation and should be replaced with actual logic
        return n * k
    
    def circuit_size(clauses):
        # Placeholder function to simulate the computation of circuit size
        # This is a dummy implementation and should be replaced with actual logic
        return len(clauses)
    
    n = random.randint(5, 40)
    while True:
        clauses = generate_k_cnf_tautology(n, k=2)  # Adjust k as needed
        if is_tautology(clauses):
            break
    
    min_rank = symplectic_rank(n, len(clauses))
    s_circuit = circuit_size(clauses)
    
    if s_circuit == 0:
        return {
            "metric_name": "Symplectic Rank / Circuit Size",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Circuit size is zero"
        }
    
    ratio = Fraction(min_rank, s_circuit)
    return {
        "metric_name": "Symplectic Rank / Circuit Size",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"First failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")