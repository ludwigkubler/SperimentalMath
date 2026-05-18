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
    def generate_disj_matrix(n):
        M1 = [[1, 1], [1, 0]]
        M = M1
        for _ in range(1, n):
            M_next = []
            for i in range(len(M)):
                for j in range(len(M[0])):
                    row = []
                    for k in range(len(M1)):
                        for l in range(len(M1[0])):
                            row.append(M[i][j] * M1[k][l])
                    M_next.append(row)
            M = M_next
        return M

    def generate_random_sign_matrix(N):
        return [[random.choice([-1, 1]) for _ in range(N)] for _ in range(N)]

    def generate_low_rank_decoy(N, k):
        u = [random.random() for _ in range(k)]
        v = [random.random() for _ in range(k)]
        return [[u[i] * v[j] for j in range(N)] for i in range(N)]

    def generate_hadamard_matrix(N):
        if N == 1:
            return [[1]]
        H_half = generate_hadamard_matrix(N // 2)
        H = []
        for i in range(N):
            row = []
            for j in range(N):
                if (i < N // 2 and j < N // 2) or (i >= N // 2 and j >= N // 2):
                    row.append(H_half[i % (N // 2)][j % (N // 2)])
                else:
                    row.append(-H_half[i % (N // 2)][j % (N // 2)])
            H.append(row)
        return H

    def matrix_multiply(A, B):
        N = len(A)
        result = [[0 for _ in range(N)] for _ in range(N)]
        for i in range(N):
            for j in range(N):
                for k in range(N):
                    result[i][j] += A[i][k] * B[k][j]
        return result

    def power_iteration(B, max_iter=50):
        N = len(B)
        x = [1] * N
        norm_x = sum(x[i]**2 for i in range(N))**0.5
        for _ in range(max_iter):
            x_new = matrix_multiply(B, x)
            norm_x_new = sum(x_new[i]**2 for i in range(N))**0.5
            if norm_x_new == 0:
                break
            x = [x_new[i] / norm_x_new for i in range(N)]
            norm_x = norm_x_new
        return max(abs(x[i]) for i in range(N)), x

    def bridge_invariant(M):
        N = len(M)
        B = matrix_multiply(M, M)
        s1 = sum(B[i][i] for i in range(N)) / (N**2)
        B_norm_F = 0
        for i in range(N):
            for j in range(N):
                B_norm_F += B[i][j]**2
        B_norm_F /= N**3
        s2 = B_norm_F
        B_squared = matrix_multiply(B, B)
        s3 = sum(sum(B_squared[i][j] * B[k][l] for l in range(N)) for i in range(N) for k in range(N)) / (N**4)
        B_squared_norm_F = 0
        for i in range(N):
            for j in range(N):
                B_squared_norm_F += B_squared[i][j]**2
        B_squared_norm_F /= N**5
        s4 = B_squared_norm_F
        kappa_2 = s2 - s1**2
        kappa_4 = s4 - 4 * s1 * s3 - 2 * s2**2 + 10 * s1**2 * s2 - 5 * s1**4
        sr = sum(B[i][i] for i in range(N)) / (sum(sum(M[i][j]**2 for j in range(N)) for i in range(N))**0.5)**2
        tau = min(math.log2(1 + abs(kappa_4) / (kappa_2**2 + N**-2)), math.log2(sr))
        return tau

    def compute_metric(M):
        N = len(M)
        B = matrix_multiply(M, M)
        s1 = sum(B[i][i] for i in range(N)) / (N**2)
        B_norm_F = 0
        for i in range(N):
            for j in range(N):
                B_norm_F += B[i][j]**2
        B_norm_F /= N**3
        s2 = B_norm_F
        B_squared = matrix_multiply(B, B)
        s3 = sum(sum(B_squared[i][j] * B[k][l] for l in range(N)) for i in range(N) for k in range(N)) / (N**4)
        B_squared_norm_F = 0
        for i in range(N):
            for j in range(N):
                B_squared_norm_F += B_squared[i][j]**2
        B_squared_norm_F /= N**5
        s4 = B_squared_norm_F
        return {"s1": s1, "s2": s2, "s3": s3, "s4": s4}

    def check_conjecture(metric):
        kappa_2 = metric["s2"] - metric["s1"]**2
        kappa_4 = metric["s4"] - 4 * metric["s1"] * metric["s3"] - 2 * metric["s2"]**2 + 10 * metric["s1"]**2 * metric["s2"] - 5 * metric["s1"]**4
        sr = sum(metric["B"][i][i] for i in range(N)) / (sum(sum(M[i][j]**2 for j in range(N)) for i in range(N))**0.5)**2
        tau = min(math.log2(1 + abs(kappa_4) / (kappa_2**2 + N**-2)), math.log2(sr))
        return tau >= 0.15 * N

    def is_random_sign_matrix(M):
        for row in M:
            if not all(x == 1 or x == -1 for x in row):
                return False
        return True

    def is_low_rank_decoy(M, k):
        rank = sum(1 for i in range(len(M)) if any(M[i][j] != 0 for j in range(len(M[0]))))
        return rank <= k

    def is_hadamard_matrix(M):
        N = len(M)
        for i in range(N):
            for j in range(N):
                if M[i][j] not in [1, -1]:
                    return False
        return True

    def compute_metric_value(metric):
        kappa_2 = metric["s2"] - metric["s1"]**2
        kappa_4 = metric["s4"] - 4 * metric["s1"] * metric["s3"] - 2 * metric["s2"]**2 + 10 * metric["s1"]**2 * metric["s2"] - 5 * metric["s1"]**4
        sr = sum(metric["B"][i][i] for i in range(N)) / (sum(sum(M[i][j]**2 for j in range(N)) for i in range(N))**0.5)**2
        tau = min(math.log2(1 + abs(kappa_4) / (kappa_2**2 + N**-2)), math.log2(sr))
        return 0.05 * tau

    def compute_metric_value_upper_bound(N):
        return max(math.ceil(math.log2(N)), math.ceil(math.log2(sum(M[i][j]**2 for i in range(N) for j in range(N))**0.5)))

    def is_valid_instance(M, n):
        if n == 2:
            return generate_disj_matrix(n) == M
        elif n == 3:
            return generate_disj_matrix(n) == M
        elif n == 4:
            return generate_disj_matrix(n) == M
        elif n == 5:
            return generate_disj_matrix(n) == M
        elif n == 6:
            return generate_disj_matrix(n) == M
        elif n == 7:
            return generate_disj_matrix(n) == M
        elif n == 8:
            return generate_disj_matrix(n) == M
        elif n == 9:
            return generate_disj_matrix(n) == M
        else:
            return False

    def is_valid_instance_random_sign(M, N):
        return is_random_sign_matrix(M)

    def is_valid_instance_low_rank_decoy(M, k):
        return is_low_rank_decoy(M, k)

    def is_valid_instance_hadamard(M, N):
        return is_hadamard_matrix(M)

    def run_trial(seed: int) -> dict:
        random.seed(seed)
        results = []
        for n in range(2, 10):
            M_disj = generate_disj_matrix(n)
            metric_disj = compute_metric(M_disj)
            if not check_conjecture(metric_disj):
                return {"seed": seed, "metric_name": "tau", "metric_value": tau_disj, "instances_tested": 1, "conjecture_holds": False, "counterexample": "DISJ_n fails"}
            results.append({"n": n, "M": M_disj, "metric": metric_disj})
        for N in range(4, 513):
            for _ in range(30):
                M_random = generate_random_sign_matrix(N)
                if not is_valid_instance_random_sign(M_random, N):
                    continue
                metric_random = compute_metric(M_random)
                results.append({"n": N, "M": M_random, "metric": metric_random})
        for N in [128]:
            for k in [1, 2, 4, 8, 16, 32]:
                M_decoy = generate_low_rank_decoy(N, k)
                if not is_valid_instance_low_rank_decoy(M_decoy, k):
                    continue
                metric_decoy = compute_metric(M_decoy)
                results.append({"n": N, "M": M_decoy, "metric": metric_decoy})
        for N in [16, 64, 256]:
            M_hadamard = generate_hadamard_matrix(N)
            if not is_valid_instance_hadamard(M_hadamard, N):
                continue
            metric_hadamard = compute_metric(M_hadamard)
            results.append({"n": N, "M": M_hadamard, "metric": metric_hadamard})
        tau_disj_values = [compute_metric_value(metric) for result in results if is_valid_instance(result["M"], result["n"])]
        tau_disj_mean = sum(tau_disj_values) / len(tau_disj_values)
        tau_disj_std = (sum((x - tau_disj_mean)**2 for x in tau_disj_values) / len(tau_disj_values))**0.5
        support_fraction = sum(1 for result in results if compute_metric_value_upper_bound(result["n"]) > 0.05 * compute_metric_value(result["metric"])) / len(results)
        return {"seed": seed, "metric_name": "tau", "metric_value": tau_disj_mean, "instances_tested": len(results), "conjecture_holds": support_fraction >= 0.95 and all(tau >= 0.15 * n for n, tau in zip([2, 3, 4, 5, 6, 7, 8, 9], tau_disj_values)), "counterexample": ""}

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    tau_disj_values = [result["metric_value"] for result in results if "tau" in result]
    tau_disj_mean = sum(tau_disj_values) / len(tau_disj_values)
    tau_disj_std = (sum((x - tau_disj_mean)**2 for x in tau_disj_values) / len(tau_disj_values))**0.5
    support_fraction = sum(1 for result in results if "tau" in result and compute_metric_value_upper_bound(result["n"]) > 0.05 * result["metric_value"]) / len(results)
    if all(tau >= 0.15 * n for n, tau in zip([2, 3, 4, 5, 6, 7, 8, 9], tau_disj_values)):
        print(f"RESULT: SUPPORTED mean={tau_disj_mean} std={tau_disj_std} support_fraction={support_fraction}")
    elif any(tau < 0.15 * n for n, tau in zip([2, 3, 4, 5, 6, 7, 8, 9], tau_disj_values)):
        print(f"RESULT: FALSIFIED counterexample=\"DISJ_n fails\" first_failing_seed={seeds[tau_disj_values.index(min(tau for tau in tau_disj_values if tau < 0.15 * n))]}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")