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
    
    def generate_random_boolean_circuit(n):
        circuit = []
        for _ in range(2**n):
            gate = (random.choice(['AND', 'OR']), [random.randint(0, n-1), random.randint(0, n-1)])
            circuit.append(gate)
        return circuit

    def compute_hypergraph(circuit):
        hypergraph = {}
        for gate in circuit:
            inputs = gate[1]
            if tuple(inputs) not in hypergraph:
                hypergraph[tuple(inputs)] = []
            hypergraph[tuple(inputs)].append(len(hypergraph))
        return hypergraph

    def min_local_induction_dimension(hypergraph):
        n = len(hypergraph)
        mld = [0] * n
        for i in range(n):
            if not hypergraph[i]:
                continue
            neighbors = set()
            for j in hypergraph[i]:
                neighbors.update(hypergraph[j])
            mld[i] = len(neighbors) - 1
        return max(mld)

    def frege_proof_length(circuit):
        # Simplified Frege proof length calculation (not actual Frege proofs)
        return sum(2 for gate in circuit if gate[0] == 'AND') + sum(1 for gate in circuit if gate[0] == 'OR')

    n_values = [5, 10, 15, 20, 30, 40]
    mld_values = []
    frege_length_values = []

    for n in n_values:
        circuit = generate_random_boolean_circuit(n)
        hypergraph = compute_hypergraph(circuit)
        mld_value = min_local_induction_dimension(hypergraph)
        frege_length_value = frege_proof_length(circuit)
        mld_values.append(mld_value)
        frege_length_values.append(frege_length_value)

    correlation_coefficient = sum((mld - mean_mld) * (frege - mean_frege) for mld, frege in zip(mld_values, frege_length_values)) / math.sqrt(sum((mld - mean_mld)**2 for mld in mld_values) * sum((frege - mean_frege)**2 for frege in frege_length_values))
    mean_mld = sum(mld_values) / len(mld_values)
    mean_frege = sum(frege_length_values) / len(frege_length_values)

    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": 0.5 <= correlation_coefficient < 0.7,
        "counterexample": "" if 0.5 <= correlation_coefficient < 0.7 else "Pearson correlation coefficient is below 0.5"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or list(range(2, 30))  # Default to first 30 primes if no seeds provided

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and min(result["metric_value"] for result in results if not result["conjecture_holds"]) >= 0.5:
        print(f"RESULT: FALSIFIED counterexample='Pearson correlation coefficient is below 0.5' first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")