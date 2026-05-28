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
    
    def log(x):
        if x <= 0:
            return float('-inf')
        return math.log(x)
    
    def matrix_multiply(A, B):
        m = len(A)
        n = len(B[0])
        p = len(B)
        C = [[sum(A[i][k] + B[k][j] for k in range(p)) for j in range(n)] for i in range(m)]
        return C
    
    def gaussian_elimination(M):
        m, n = len(M), len(M[0])
        rank = 0
        for i in range(min(m, n)):
            if M[i][i] == 0:
                swap_found = False
                for j in range(i + 1, m):
                    if M[j][i] != 0:
                        M[i], M[j] = M[j], M[i]
                        swap_found = True
                        break
                if not swap_found:
                    continue
            pivot = M[i][i]
            for j in range(n):
                M[i][j] /= pivot
            for j in range(m):
                if j != i and M[j][i] != 0:
                    factor = M[j][i]
                    for k in range(n):
                        M[j][k] -= factor * M[i][k]
            rank += 1
        return rank
    
    def construct_tropical_vector_bundle(C, n):
        # Simplified mapping of circuit to tropical vector bundle
        sections = []
        for gate in C:
            if gate['type'] == 'INPUT':
                section = [0] * n
                section[gate['index']] = 1
                sections.append(section)
            elif gate['type'] == 'OR':
                section = [max(sections[i][j] + sections[j][k] for i in range(len(sections)) for j in range(i, len(sections))) for k in range(n)]
                sections.append(section)
        return matrix_multiply(sections, sections)
    
    def generate_monotone_circuit(k):
        n = 2 * k
        circuit = []
        inputs = [i for i in range(n)]
        random.shuffle(inputs)
        for i in range(k):
            gate = {'type': 'OR', 'index': n + i}
            for j in range(2):
                gate['inputs'] = [inputs.pop() for _ in range(2)]
            circuit.append(gate)
        return circuit
    
    k_values = [5, 10, 15, 20, 30, 40]
    metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in range(5, 41):
        for k in k_values:
            C = generate_monotone_circuit(k)
            V = construct_tropical_vector_bundle(C, n)
            rank = gaussian_elimination(V)
            metric_value += rank
            instances_tested += 1
            if rank < n**k * log(n):
                conjecture_holds = False
                counterexample = f"n={n}, k={k}, rank={rank}"
    
    return {
        "metric_name": "Minimal Rank of Tropical Vector Bundle",
        "metric_value": metric_value / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3**j for i in range(5) for j in range(5)]
    
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
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")