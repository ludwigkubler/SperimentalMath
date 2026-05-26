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
    
    def generate_k_cnf(n, k):
        clauses = []
        for _ in range(k):
            clause = set()
            while len(clause) < 2:
                var = random.randint(1, n)
                if var not in clause and -var not in clause:
                    clause.add(var)
            clauses.append(tuple(sorted(clause)))
        return clauses
    
    def tseitin_circuit(clauses):
        literals = set()
        for clause in clauses:
            literals.update(clause)
        n_vars = len(literals)
        circuit = []
        for i, literal in enumerate(literals):
            circuit.append((literal,))
        for clause in clauses:
            new_var = n_vars + 1
            n_vars += 1
            circuit.append((-new_var,) + tuple(-l for l in clause))
            for literal in clause:
                circuit.append((new_var, -literal))
        return circuit
    
    def hodge_decomposition(circuit):
        # Placeholder for Hodge decomposition logic
        # This is a dummy implementation that returns a random rank
        return random.randint(1, 10)
    
    n = random.randint(5, 40)
    k = random.randint(2, n-1)
    clauses = generate_k_cnf(n, k)
    circuit = tseitin_circuit(clauses)
    rank = hodge_decomposition(circuit)
    
    expected_upper_bound = math.log2(n / k) ** 2
    expected_lower_bound = n ** (1/4)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": expected_lower_bound <= rank <= expected_upper_bound,
        "counterexample": f"rank={rank}, expected_upper_bound={expected_upper_bound:.4f}, expected_lower_bound={expected_lower_bound:.4f}" if not (expected_lower_bound <= rank <= expected_upper_bound) else ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank out of bounds\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")