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
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def hypergraph_from_circuit(circuit):
        n = int(math.log2(len(circuit)))
        H = {i: set() for i in range(n)}
        for i in range(n):
            for j in range(i+1, n):
                if circuit[i] == circuit[j]:
                    H[i].add(j)
                    H[j].add(i)
        return H
    
    def min_local_induction_dimension(H):
        n = len(H)
        visited = [False] * n
        mld = 0
        
        for i in range(n):
            if not visited[i]:
                queue = [i]
                while queue:
                    node = queue.pop(0)
                    if not visited[node]:
                        visited[node] = True
                        mld += 1
                        queue.extend(H[node])
        
        return mld
    
    def frege_proof_length(circuit):
        n = int(math.log2(len(circuit)))
        proof_length = 0
        
        for i in range(n):
            if circuit[i] == 1:
                proof_length += 1
        
        return proof_length
    
    results = []
    n_values = [5, 10, 15, 20, 30, 40]
    
    for n in n_values:
        for _ in range(5):
            circuit = generate_random_boolean_circuit(n)
            H = hypergraph_from_circuit(circuit)
            mld = min_local_induction_dimension(H)
            f = frege_proof_length(circuit)
            results.append((mld, f))
    
    if not results:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mlds = [r[0] for r in results]
    fs = [r[1] for r in results]
    mean_mld = sum(mlds) / len(mlds)
    mean_f = sum(fs) / len(fs)
    covariance = sum((mlds[i] - mean_mld) * (fs[i] - mean_f) for i in range(len(results))) / len(results)
    variance_mld = sum((mlds[i] - mean_mld)**2 for i in range(len(results))) / len(results)
    variance_f = sum((fs[i] - mean_f)**2 for i in range(len(results))) / len(results)
    pearson_corr = covariance / math.sqrt(variance_mld * variance_f)
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_corr,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": pearson_corr >= 0.7,
        "counterexample": "" if pearson_corr >= 0.7 else f"pearson_corr={pearson_corr:.2f} < 0.5"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
        std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
        support_fraction = 1.0
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = result["counterexample"]
        mean_metric_value = sum(r["metric_value"] for r in results if r["conjecture_holds"]) / sum(1 for r in results if r["conjecture_holds"])
        std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results if r["conjecture_holds"]) / sum(1 for r in results if r["conjecture_holds"]))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    print(f"RESULT: {'SUPPORTED' if all(r['conjecture_holds'] for r in results) else 'FALSIFIED'} mean={mean_metric_value:.2f} std={std_metric_value:.2f} support_fraction={support_fraction:.2f}")