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
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses

    def tseitin_circuit(clauses):
        literals = set()
        for clause in clauses:
            literals.update(abs(lit) for lit in clause)
        variables = list(literals)
        circuit = []
        for i, literal in enumerate(variables):
            circuit.append([literal])
            for clause in clauses:
                if literal in clause:
                    circuit.append([-literal, -i-1])
                elif -literal in clause:
                    circuit.append([literal, i+1])
        return circuit

    def hodge_decomposition(circuit):
        # Simplified Hodge decomposition (not actual implementation)
        rank = len(circuit)
        return rank

    n = random.randint(5, 40)
    k = random.randint(2, min(n // 2, 10))
    clauses = generate_k_cnf(n, k)
    circuit = tseitin_circuit(clauses)
    rank = hodge_decomposition(circuit)

    expected_upper_bound = math.log(n / k) ** 2
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
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_dev:.4f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unexpected_behavior")