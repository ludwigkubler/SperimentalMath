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
    
    def generate_random_boolean_circuit(n):
        if n == 1:
            return [random.choice([0, 1])]
        else:
            subcircuits = [generate_random_boolean_circuit(random.randint(1, n-1)) for _ in range(2)]
            return [random.choice([0, 1]) + subcircuit for subcircuit in subcircuits]
    
    def compute_hypergraph(circuit):
        hypergraph = {}
        for i, gate in enumerate(circuit):
            if gate == 0:
                continue
            inputs = circuit[:i]
            if len(inputs) > 1:
                hypergraph[i] = set(inputs)
        return hypergraph
    
    def min_local_induction_dimension(hypergraph):
        n = len(hypergraph)
        mld = [0] * n
        for i in range(n):
            if i not in hypergraph:
                continue
            for j in hypergraph[i]:
                if j < i and mld[j] < mld[i]:
                    mld[i] = mld[j]
            mld[i] += 1
        return max(mld)
    
    def frege_proof_length(circuit):
        length = 0
        stack = []
        for gate in circuit:
            if gate == 0:
                continue
            inputs = stack[-gate:]
            stack.append(inputs)
            length += len(inputs) + 1
        return length
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        circuit = generate_random_boolean_circuit(n)
        hypergraph = compute_hypergraph(circuit)
        mld_value = min_local_induction_dimension(hypergraph)
        f_value = frege_proof_length(circuit)
        metric_values.append((mld_value, f_value))
    
    if not metric_values:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "empty_metric_values"
        }
    
    mld_values, f_values = zip(*metric_values)
    mean_mld = sum(mld_values) / len(mld_values)
    mean_f = sum(f_values) / len(f_values)
    covariance = sum((mld - mean_mld) * (f - mean_f) for mld, f in metric_values) / len(metric_values)
    variance_mld = sum((mld - mean_mld) ** 2 for mld in mld_values) / len(mld_values)
    variance_f = sum((f - mean_f) ** 2 for f in f_values) / len(f_values)
    
    if variance_mld == 0 or variance_f == 0:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "zero_variance"
        }
    
    pearson_correlation = covariance / (math.sqrt(variance_mld) * math.sqrt(variance_f))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_correlation,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": pearson_correlation >= 0.7,
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
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = len([r for r in results if "conjecture_holds" in r and r["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if "conjecture_holds" not in r or not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")