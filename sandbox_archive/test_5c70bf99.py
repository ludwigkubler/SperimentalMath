# auto-injected by SEC sandbox
import itertools
import json
import sys
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from collections import defaultdict

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(A, b):
        n = len(b)
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            for j in range(i+1, n):
                factor = A[j][i] / A[i][i]
                A[j][i:] = [A[j][k] - factor * A[i][k] for k in range(i, n)]
                b[j] -= factor * b[i]
        x = [0] * n
        for i in range(n-1, -1, -1):
            x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
        return x

    def matrix_multiply(A, B):
        m, k = len(A), len(B[0])
        result = [[0] * k for _ in range(m)]
        for i in range(m):
            for j in range(k):
                result[i][j] = sum(A[i][l] * B[l][j] for l in range(len(B)))
        return result

    def determinant(A):
        n = len(A)
        if n == 1:
            return A[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += (-1) ** j * A[0][j] * determinant(submatrix)
        return det

    def inverse(A):
        n = len(A)
        det_A = determinant(A)
        if det_A == 0:
            raise ValueError("Matrix is singular")
        adjoint = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                submatrix = [row[:j] + row[j+1:] for row in A[:i] + A[i+1:]]
                cofactor = determinant(submatrix) * (-1) ** (i+j)
                adjoint[j][i] = cofactor
        return matrix_multiply(adjoint, [[1/det_A]*n for _ in range(n)])

    def generate_k_clique_dnf(n, k):
        edges = [(i, j) for i in range(n) for j in range(i+1, n)]
        clique_edges = random.sample(edges, k*(k-1)//2)
        dnf = []
        for edge_set in itertools.combinations(clique_edges, k):
            term = [0] * (n*(n-1)//2)
            for i, j in edge_set:
                term[i*n - i + j - 1] = 1
            dnf.append(term)
        return dnf

    def generate_random_dnf(n, m):
        edges = [(i, j) for i in range(n) for j in range(i+1, n)]
        dnf = []
        for _ in range(m):
            width = random.randint(2, n*(n-1)//2)
            term = [0] * (n*(n-1)//2)
            selected_edges = random.sample(edges, width)
            for i, j in selected_edges:
                term[i*n - i + j - 1] = 1
            dnf.append(term)
        return dnf

    def greedy_certifier(dnf, x):
        live_terms = [i for i, term in enumerate(dnf) if any(x[j] == 0 for j in range(len(term)) if term[j] == 1)]
        cert_length = 0
        while len(live_terms) > 0:
            max_live_vars = sum([sum(1 for j in range(len(term)) if term[j] == 1 and x[j] == 0) for i, term in enumerate(dnf) if i in live_terms])
            var_to_reveal = -1
            for j in range(n*(n-1)//2):
                if any(x[j] == 0 for i, term in enumerate(dnf) if i in live_terms and term[j] == 1):
                    num_live_terms = sum(1 for i, term in enumerate(dnf) if i in live_terms and term[j] == 1)
                    if var_to_reveal == -1 or num_live_terms > max_live_vars:
                        max_live_vars = num_live_terms
                        var_to_reveal = j
            x[var_to_reveal] = 1
            cert_length += 1
            live_terms = [i for i, term in enumerate(dnf) if any(x[j] == 0 for j in range(len(term)) if term[j] == 1)]
        return cert_length

    def calculate_mu(F, n):
        D_k = [random.getrandbits(n*(n-1)//2) for _ in range(30)]
        mu = sum(greedy_certifier(F, x) for x in D_k) / len(D_k)
        return mu

    n_values = [6, 7, 8, 9, 10]
    k_values = [3, 4]
    results = []

    for n in n_values:
        m_values = [10, 30, n**2]
        
        F_clique = generate_k_clique_dnf(n, k)
        mu_clique = calculate_mu(F_clique, n)
        results.append({"metric_name": "mu_clique", "metric_value": mu_clique, "instances_tested": 30, "conjecture_holds": mu_clique >= n//4, "counterexample": ""})
        
        for m in m_values:
            F_rand = generate_random_dnf(n, m)
            mu_rand = calculate_mu(F_rand, n)
            results.append({"metric_name": f"mu_rand_{m}", "metric_value": mu_rand, "instances_tested": 30, "conjecture_holds": mu_rand <= 3*math.log2(n)+8, "counterexample": ""})

    return {
        "TRIAL": results
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    all_results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        all_results.extend(result["TRIAL"])

    mu_clique_values = [r["metric_value"] for r in all_results if r["metric_name"] == "mu_clique"]
    mu_rand_values = [r["metric_value"] for r in all_results if r["metric_name"].startswith("mu_rand_")]

    mean_mu_clique = sum(mu_clique_values) / len(mu_clique_values)
    std_mu_clique = math.sqrt(sum((x - mean_mu_clique) ** 2 for x in mu_clique_values) / len(mu_clique_values))
    support_fraction_clique = sum(1 for r in all_results if r["metric_name"] == "mu_clique" and r["conjecture_holds"]) / len(all_results)

    mean_mu_rand = sum(mu_rand_values) / len(mu_rand_values)
    std_mu_rand = math.sqrt(sum((x - mean_mu_rand) ** 2 for x in mu_rand_values) / len(mu_rand_values))
    support_fraction_rand = sum(1 for r in all_results if r["metric_name"].startswith("mu_rand_") and r["conjecture_holds"]) / len(all_results)

    if support_fraction_clique >= 0.95 and support_fraction_rand >= 0.95:
        RESULT = f"SUPPORTED mean_mu_clique={mean_mu_clique} std_mu_clique={std_mu_clique} support_fraction_clique={support_fraction_clique}"
    elif any(not r["conjecture_holds"] for r in all_results):
        counterexample = next(r for r in all_results if not r["conjecture_holds"])["metric_name"]
        RESULT = f"FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[next(i for i, r in enumerate(all_results) if not r['conjecture_holds'])]}"
    else:
        RESULT = "INCONCLUSIVE reason=insufficient_support"

    print(RESULT)