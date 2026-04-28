# auto-injected by SEC sandbox
import itertools
import collections
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
import json

# Helper functions for basic linear algebra and combinatorics
def dot_product(v1, v2):
    return sum(x * y for x, y in zip(v1, v2))

def hamming_distance(v1, v2):
    return sum(1 for x, y in zip(v1, v2) if x != y)

def matrix_multiply(A, B):
    n = len(A)
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                result[i][j] += A[i][k] * B[k][j]
    return result

def gaussian_elimination(matrix, b):
    n = len(matrix)
    augmented_matrix = [row + [b[i]] for i, row in enumerate(matrix)]
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(augmented_matrix[j][i]) > abs(augmented_matrix[max_row][i]):
                max_row = j
        augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
        factor = augmented_matrix[i][i]
        for j in range(i, n+1):
            augmented_matrix[i][j] /= factor
        for j in range(n):
            if j != i:
                factor = augmented_matrix[j][i]
                for k in range(i, n+1):
                    augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
    return [row[-1] for row in augmented_matrix]

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

# Define the 2-bit inner-product MetricGadget
def ip_2(v1, v2):
    return dot_product(v1[:2], v2[:2])

# Define the coordinatewise additive metric
def d_plus(v1, v2):
    return sum(hamming_distance(v1[i], v2[i]) for i in range(len(v1)))

# Define the GadgetComposition function
def gadget_composition(gadgets):
    n = len(gadgets)
    result = [[0] * (n**2) for _ in range(n**2)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                for l in range(n):
                    result[i*n+k][j*n+l] = gadgets[i][k] + gadgets[j][l]
    return result

# Define the LiftedInputSpace function
def lifted_input_space(gadget, metric):
    n = len(gadget)
    result = [[0] * (n**2) for _ in range(n**2)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                for l in range(n):
                    result[i*n+k][j*n+l] = metric(gadget[i], gadget[j]) + metric(gadget[k], gadget[l])
    return result

# Define the AsdimCertify function
def asdim_certify(lifted_space, R):
    n = int(math.sqrt(len(lifted_space)))
    for m in range(1, n+1):
        covers = []
        for i in range(n):
            for j in range(n):
                cover = [(i*n+k, j*n+l) for k in range(m) for l in range(m)]
                if all(d_plus(lifted_space[i*n+k], lifted_space[j*n+l]) <= R for (k1, l1), (k2, l2) in itertools.combinations(cover, 2)):
                    covers.append(cover)
        if len(covers) > 0:
            return m
    return n

# Define the CoarsePullbackProtocol function
def coarse_pullback_protocol(protocol, lifted_space):
    n = int(math.sqrt(len(lifted_space)))
    result = []
    for i in range(n):
        for j in range(n):
            result.append((i*n+j, protocol[i][j]))
    return result

# Define the run_trial function
def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    # Parameters
    k_values = [1, 2, 3]
    n_values = [2, 3]
    f_functions = [lambda x: all(x), lambda x: sum(x) % 2 == 0]
    
    metric_value = 0.0
    instances_tested = 0
    
    for k in k_values:
        G_k = gadget_composition([ip_2] * k)
        lifted_space = lifted_input_space(G_k, d_plus)
        
        for f in f_functions:
            Q_f = len(f(range(2**n)))
            
            # AsdimCertify
            m = asdim_certify(lifted_space, 4)
            if m < k + 1:
                return {
                    "metric_name": "AsdimCertify",
                    "metric_value": m,
                    "instances_tested": instances_tested,
                    "conjecture_holds": False,
                    "counterexample": f"asdim_certify failed for k={k}, Q(f)={Q_f}"
                }
            metric_value += m
            instances_tested += 1
            
            # Protocol enumeration
            max_cost = math.ceil(Q_f * math.log2(k + 1)) - 1
            found_protocol = False
            for c in range(1, max_cost + 1):
                protocol = [[0] * (n**2) for _ in range(n**2)]
                if enumerate_protocols(lifted_space, f, protocol, c):
                    found_protocol = True
                    break
            if not found_protocol:
                return {
                    "metric_name": "ProtocolEnumeration",
                    "metric_value": None,
                    "instances_tested": instances_tested,
                    "conjecture_holds": False,
                    "counterexample": f"protocol enumeration failed for k={k}, Q(f)={Q_f}"
                }
            metric_value += c
            instances_tested += 1
    
    return {
        "metric_name": "AsdimCertify and ProtocolEnumeration",
        "metric_value": metric_value / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": True,
        "counterexample": ""
    }

# Define the protocol enumeration function
def enumerate_protocols(lifted_space, f, protocol, c):
    n = int(math.sqrt(len(lifted_space)))
    for i in range(n):
        for j in range(n):
            if sum(protocol[i*n+k][j*n+l] for k in range(n) for l in range(n)) != c:
                return False
    return True

# Main function to run trials and print results
if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {json.dumps(result)}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = next(result["counterexample"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")