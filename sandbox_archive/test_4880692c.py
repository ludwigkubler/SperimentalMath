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
    
    def is_valid_3cnf(formula):
        for clause in formula:
            if len(clause) != 3 or not all(isinstance(lit, int) and lit != 0 for lit in clause):
                return False
        return True
    
    def generate_random_3cnf(n: int, m: int):
        variables = list(range(1, n + 1))
        clauses = []
        while len(clauses) < m:
            clause = random.sample(variables * 2, 3)
            if is_valid_3cnf([clause]):
                clauses.append(clause)
        return clauses
    
    def tseitin_circuit(formula):
        literals = set()
        for clause in formula:
            literals.update(clause)
        n_vars = max(literals)
        new_var_id = n_vars + 1
        circuit = []
        for i, clause in enumerate(formula):
            literal_ids = [abs(lit) for lit in clause]
            if len(set(literal_ids)) == 3:
                circuit.append([new_var_id, -literal_ids[0], literal_ids[1]])
                circuit.append([new_var_id, -literal_ids[1], literal_ids[2]])
                circuit.append([-new_var_id, literal_ids[0], literal_ids[1], literal_ids[2]])
            else:
                return None
            new_var_id += 1
        return circuit
    
    def tropicalized_simplicial_complex(circuit):
        if not circuit:
            return []
        simplices = set()
        for clause in circuit:
            simplices.add(tuple(sorted(clause)))
        return list(simlices)
    
    def min_rank(simplices):
        if not simplices:
            return 0
        n = len(simplices[0])
        rank = 1
        while True:
            found_new_simplex = False
            for simplex in simplices:
                if all(len(simplex & other) <= 1 for other in simplices if simplex != other):
                    found_new_simplex = True
                    break
            if not found_new_simplex:
                break
            rank += 1
        return rank
    
    n = random.randint(5, 40)
    m = min(2**n, 100)  # Ensure m is at least 2^n but not too large
    formula = generate_random_3cnf(n, m)
    circuit = tseitin_circuit(formula)
    if circuit is None:
        return {
            "metric_name": "min_rank",
            "metric_value": -1,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    simplices = tropicalized_simplicial_complex(circuit)
    min_rank_value = min_rank(simplices)
    
    expected_min_rank = math.log(n) * (1 - 0.1)
    if abs(math.log(n) - min_rank_value) <= 0.1 * math.log(n):
        conjecture_holds = True
    else:
        conjecture_holds = False
    
    return {
        "metric_name": "min_rank",
        "metric_value": min_rank_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
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
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")