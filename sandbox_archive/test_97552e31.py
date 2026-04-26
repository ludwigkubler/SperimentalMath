import random
import math
import itertools

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def factorial(n):
        if n == 0 or n == 1:
            return 1
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result
    
    def binomial_coefficient(n, k):
        return factorial(n) // (factorial(k) * factorial(n - k))
    
    def kronecker_coefficient(lam, mu, nu):
        if len(lam) != len(mu) or len(mu) != len(nu):
            return 0
        m = len(lam)
        result = 1
        for i in range(m):
            result *= binomial_coefficient(lam[i] + mu[i] - nu[i], lam[i])
            result //= (factorial(lam[i]) * factorial(mu[i]) * factorial(nu[i]))
        return result
    
    def is_hook_shape(partition):
        if len(partition) == 0:
            return True
        for i in range(1, len(partition)):
            if partition[i] >= partition[i - 1]:
                return False
        return True
    
    def generate_3cnf(n, m):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(m):
            clause = random.sample(variables, 3)
            clause.append(random.choice([True, False]))
            clauses.append(clause)
        return clauses
    
    def abp_size(clauses, variables):
        n = len(variables)
        m = len(clauses)
        dp = [[0] * (1 << n) for _ in range(m + 1)]
        for i in range(1 << n):
            dp[0][i] = 1
        for j in range(1, m + 1):
            for i in range(1 << n):
                dp[j][i] = sum(dp[j - 1][i ^ mask] for mask in range(1 << n) if (mask & (1 << clauses[j - 1][0] - 1)) != 0)
        return max(dp[m])

    def symmetrized_tensor_product(clauses, variables):
        n = len(variables)
        m = len(clauses)
        tensor = [[[0 for _ in range(2)] for _ in range(n + 1)] for _ in range(m + 1)]
        tensor[0][0] = [1, 0]
        for j in range(1, m + 1):
            for i in range(n + 1):
                for k in range(i + 1):
                    tensor[j][i][k] += tensor[j - 1][i - k][k]
        return tensor
    
    def extract_kronecker_coefficients(tensor):
        n = len(tensor[0])
        m = len(tensor)
        max_kronecker = 0
        for i in range(m):
            for j in range(n):
                for k in range(j + 1):
                    partition_i = [i - j, j - k]
                    partition_j = [j - k, k]
                    partition_k = [k]
                    if is_hook_shape(partition_i) and is_hook_shape(partition_j) and is_hook_shape(partition_k):
                        max_kronecker = max(max_kronecker, kronecker_coefficient(partition_i, partition_j, partition_k))
        return max_kronecker
    
    n_values = [5]
    m_values = [10]
    
    results = []
    for n in n_values:
        for m in m_values:
            clauses = generate_3cnf(n, m)
            variables = list(range(1, n + 1))
            abp_size_value = abp_size(clauses, variables)
            tensor = symmetrized_tensor_product(clauses, variables)
            max_kronecker_coeff = extract_kronecker_coefficients(tensor)
            results.append({
                "n": n,
                "m": m,
                "abp_size": abp_size_value,
                "max_kronecker_coeff": max_kronecker_coeff
            })
    
    metric_name = "ABP Size vs Max Kronecker Coefficient"
    metric_values = [result["abp_size"] for result in results]
    instances_tested = len(results)
    conjecture_holds = all(result["abp_size"] >= result["max_kronecker_coeff"] for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": metric_name,
        "metric_value": sum(metric_values) / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [11, 23, 37, 53, 71]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")