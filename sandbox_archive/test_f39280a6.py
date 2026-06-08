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
    
    def generate_cnf(n: int):
        cnf = []
        for _ in range(n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def dpll(cnf):
        if not cnf:
            return True
        literal = random.choice([x for x in set(lit for clause in cnf for lit in clause) if lit > 0])
        new_cnf = [clause for clause in cnf if literal not in clause and -literal not in clause]
        if dpll(new_cnf):
            return True
        new_cnf = [clause for clause in cnf if -literal not in clause]
        return dpll(new_cnf)
    
    def local_coherence_index(cnf):
        n = len(cnf)
        index = 0
        for i in range(n):
            for j in range(i + 1, n):
                if all(lit in cnf[i] or -lit in cnf[j] for lit in cnf[j]):
                    index += 1
        return index
    
    metrics = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            cnf = generate_cnf(n)
            proof_length = len(cnf) if dpll(cnf) else float('inf')
            index = local_coherence_index(cnf)
            metrics.append((index, proof_length))
    
    n_max = max(n for _, _ in metrics)
    instances_tested = len(metrics)
    mean_index = sum(index for index, _ in metrics) / instances_tested
    mean_proof_length = sum(proof_length for _, proof_length in metrics) / instances_tested
    
    correlation_coefficient = 0.0
    if n_max >= 16:
        numerator = sum((index - mean_index) * (proof_length - mean_proof_length) for index, proof_length in metrics)
        denominator = math.sqrt(sum((index - mean_index) ** 2 for index, _ in metrics)) * math.sqrt(sum((proof_length - mean_proof_length) ** 2 for _, proof_length in metrics))
        correlation_coefficient = numerator / denominator if denominator != 0 else 0.0
    
    conjecture_holds = abs(correlation_coefficient) >= 3
    counterexample = "" if conjecture_holds else f"Correlation coefficient: {correlation_coefficient}"
    
    return {
        "metric_name": "LocalCoherenceIndex vs DPLLProofLength",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")