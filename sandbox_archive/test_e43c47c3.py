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
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for _ in range(n):
            clause = random.sample(variables + [f'~{v}' for v in variables], 3)
            clauses.append(' | '.join(clause))
        return ' & '.join(clauses)

    def tseitin_circuit(formula):
        literals = set()
        for literal in formula.split():
            if literal.startswith('~'):
                literals.add(literal[1:])
            else:
                literals.add(literal)
        
        circuit = {}
        for literal in literals:
            circuit[literal] = [f'~{literal}', f'{literal}']
        
        return circuit

    def galois_representation_order(n):
        # Simplified approximation for demonstration
        return 2 ** (n - 1)

    def quadratic_residue_rank(n):
        # Simplified approximation for demonstration
        return n / 2

    n = random.randint(5, 40)
    formula = generate_3cnf(n)
    circuit = tseitin_circuit(formula)
    
    order = galois_representation_order(n)
    rank = quadratic_residue_rank(n)
    
    expected_order = math.log2(2 ** n)
    expected_rank = expected_order / 2
    
    return {
        "metric_name": "galois_representation_order",
        "metric_value": order,
        "instances_tested": 1,
        "conjecture_holds": order <= expected_order and rank >= expected_rank,
        "counterexample": f"order={order}, rank={rank}, expected_order={expected_order}, expected_rank={expected_rank}" if not (order <= expected_order and rank >= expected_rank) else ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")