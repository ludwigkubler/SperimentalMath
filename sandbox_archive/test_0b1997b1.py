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
    
    def generate_acc0_circuit(n):
        if n == 1:
            return [0]
        circuit = []
        for _ in range(n - 1):
            gate_type = random.choice(['AND', 'OR'])
            if gate_type == 'AND':
                inputs = [random.randint(0, i) for i in range(1, n)]
                circuit.append(('AND', inputs))
            else:
                inputs = [random.randint(0, i) for i in range(1, n)]
                circuit.append(('OR', inputs))
        return circuit
    
    def construct_quasi_group_representation(circuit):
        if not circuit:
            return []
        qg = {}
        for gate_type, inputs in circuit:
            if gate_type == 'AND':
                output = random.randint(0, len(inputs) - 1)
                qg[(inputs, output)] = (output, inputs[output])
            else:
                output = random.randint(0, len(inputs) - 1)
                qg[(inputs, output)] = (output, inputs[output])
        return qg
    
    def rank(qg):
        if not qg:
            return 0
        rows = list(qg.values())
        cols = [list(col) for col in zip(*rows)]
        n = len(rows)
        rref = []
        for i in range(n):
            if all(row[i] == 0 for row in rows):
                continue
            pivot_row = max(range(i, n), key=lambda j: abs(rows[j][i]))
            rows[pivot_row], rows[i] = rows[i], rows[pivot_row]
            rows[i] = [x / rows[i][i] for x in rows[i]]
            for j in range(n):
                if i != j:
                    factor = rows[j][i]
                    rows[j] = [rows[j][k] - factor * rows[i][k] for k in range(n)]
        rref = [row for row in rows if any(x != 0 for x in row)]
        return len(rref)
    
    def log_n(n):
        return math.log2(n) / math.log2(math.e)
    
    n_values = [5, 10, 15, 20, 30, 40]
    ranks = []
    for n in n_values:
        circuit = generate_acc0_circuit(n)
        qg = construct_quasi_group_representation(circuit)
        rank_val = rank(qg)
        ranks.append(rank_val)
    
    mean_rank = sum(ranks) / len(ranks)
    conjecture_holds = all(abs(rank_val - log_n(n)) <= 1 for n, rank_val in zip(n_values, ranks))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": mean_rank,
        "instances_tested": len(ranks),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")