def sieve_of_eratosthenes(n):
    # let prime_list be an array of boolean values, indexed by integers up to n, initially all set to true
    prime_list = [True for _ in range(n+1)]
    p = 2
    while p * p <= n:
        # if prime_list[p] is not 1 and True, it is prime
        if prime_list[p]:
            for i in range(p * p, n + 1, p):
                # if prime_list[i] is a multiple of prime_list[p], set to false
                prime_list[i] = False
        p = p + 1
    # print all prime numbers less or equal to n
    for i in range(2, n+1):
        if prime_list[i]:
            print(i)


if __name__ == '__main__':
    value = input("Please enter a value: ")
    print("These are the prime numbers less or equal to the value you entered:")
    sieve_of_eratosthenes(int(value))
