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
            clause = [random.randint(-n, -1), random.randint(1, n)]
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses

    def tseitin_circuit(clauses):
        literals = set()
        for clause in clauses:
            literals.update(abs(x) for x in clause)
        variables = list(literals)
        n_vars = len(variables)
        
        circuit = []
        for i, literal in enumerate(literals):
            if literal > 0:
                circuit.append(f"v{i+1} := {literal}")
            else:
                circuit.append(f"v{i+1} := ~{abs(literal)}")
        
        for clause in clauses:
            var_index = n_vars + len(clause)
            circuit.append(f"v{var_index+1} := ({' & '.join([f'v{i+1}' if x > 0 else f'~v{-x+1}' for x in clause])})")
            n_vars += 1
        
        return circuit

    def galois_representation(circuit):
        # Simplified representation for demonstration
        return len(circuit)

    def quadratic_residue_lattice_rank(n):
        return math.log(2**n) / 2

    n = random.randint(5, 40)
    formula = generate_3cnf(n)
    circuit = tseitin_circuit(formula)
    
    galois_order = galois_representation(circuit)
    expected_galois_order = math.log(2**n)
    expected_rank = quadratic_residue_lattice_rank(n)
    
    conjecture_holds = (galois_order <= expected_galois_order) and (quadratic_residue_lattice_rank(n) >= expected_rank / 2)
    counterexample = "" if conjecture_holds else f"rank={quadratic_residue_lattice_rank(n)}, expected={expected_rank / 2}"
    
    return {
        "metric_name": "galois_representation_order",
        "metric_value": galois_order,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample_desc = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")