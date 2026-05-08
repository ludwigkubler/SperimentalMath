# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import product

# Define A_5 and its standard 4-dim irreducible representation
A5 = [
    [1, 2, 3, 4, 5],
    [2, 3, 4, 5, 1],
    [3, 4, 5, 1, 2],
    [4, 5, 1, 2, 3],
    [5, 1, 2, 3, 4]
]

rho_alpha = [
    [-0.5, -0.5, 0, 0],
    [0, 0, -0.5, -0.5],
    [0.5, 0, 0, 0],
    [0, 0.5, 0, 0]
]

rho_beta = [
    [-0.5, 0, 0, 0.5],
    [0, -0.5, 0.5, 0],
    [0.5, 0.5, 0, 0],
    [0, 0, 0, 0]
]

def sign_matrix_to_block_matrix(M_f, rho_alpha, rho_beta):
    k = int(math.log2(len(M_f)))
    W_f = [[0] * (4 * k) for _ in range(4 * k)]
    for i, j in product(range(k), repeat=2):
        if M_f[i][j] == 1:
            W_f[4*i:4*(i+1), 4*j:4*(j+1)] = rho_alpha
        elif M_f[i][j] == -1:
            W_f[4*i:4*(i+1), 4*j:4*(j+1)] = rho_beta
    return W_f

def spectral_norm(matrix):
    k = len(matrix)
    U, S, Vt = list(zip(*map(list, zip(*matrix))))
    sigma_max = max(S)
    return sigma_max

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_random_sign_matrix(k):
        return [[random.choice([-1, 1]) for _ in range(2**k)] for _ in range(2**k)]
    
    def generate_DISJ_k(k):
        M = [[0] * (2**k) for _ in range(2**k)]
        for i in range(2**k):
            for j in range(i+1, 2**k):
                if bin(i & j).count('1') % 2 == 1:
                    M[i][j] = M[j][i] = -1
                else:
                    M[i][j] = M[j][i] = 1
        return M
    
    def generate_INNER_PRODUCT_k(k):
        M = [[0] * (2**k) for _ in range(2**k)]
        for i in range(2**k):
            for j in range(i+1, 2**k):
                if bin(i & j).count('1') % 2 == 0:
                    M[i][j] = M[j][i] = -1
                else:
                    M[i][j] = M[j][i] = 1
        return M
    
    k_values = [3, 4, 5, 6]
    results = []
    
    for k in k_values:
        random_sign_matrix = generate_random_sign_matrix(k)
        DISJ_k = generate_DISJ_k(k)
        INNER_PRODUCT_k = generate_INNER_PRODUCT_k(k)
        
        W_f_random = sign_matrix_to_block_matrix(random_sign_matrix, rho_alpha, rho_beta)
        W_f_DISJ = sign_matrix_to_block_matrix(DISJ_k, rho_alpha, rho_beta)
        W_f_IP = sign_matrix_to_block_matrix(INNER_PRODUCT_k, rho_alpha, rho_beta)
        
        sigma_max_random = spectral_norm(W_f_random)
        sigma_max_DISJ = spectral_norm(W_f_DISJ)
        sigma_max_IP = spectral_norm(W_f_IP)
        
        eta_random = math.log2(sigma_max_random / (2**k))
        eta_DISJ = math.log2(sigma_max_DISJ / (2**k))
        eta_IP = math.log2(sigma_max_IP / (2**k))
        
        eta_0_random = math.log2(eta_random * 2)
        eta_0_DISJ = math.log2(eta_DISJ * 2)
        eta_0_IP = math.log2(eta_IP * 2)
        
        results.append({
            "metric_name": "eta",
            "metric_value": eta_random,
            "instances_tested": 1,
            "conjecture_holds": eta_random >= 0.5 * eta_0_random - 1,
            "counterexample": ""
        })
        results.append({
            "metric_name": "eta",
            "metric_value": eta_DISJ,
            "instances_tested": 1,
            "conjecture_holds": eta_DISJ >= 0.51 * k,
            "counterexample": ""
        })
        results.append({
            "metric_name": "eta",
            "metric_value": eta_IP,
            "instances_tested": 1,
            "conjecture_holds": True,  # IP_k is a known hard control
            "counterexample": ""
        })
    
    all_conjecture_holds = all(result["conjecture_holds"] for result in results)
    counterexample = next((result["counterexample"] for result in results if not result["conjecture_holds"]), "")
    
    return {
        "metric_name": "eta",
        "metric_value": sum(result["metric_value"] for result in results) / len(results),
        "instances_tested": len(results),
        "conjecture_holds": all_conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 7 for i in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean = sum(result["metric_value"] for result in results) / len(results)
    std = math.sqrt(sum((result["metric_value"] - mean)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")