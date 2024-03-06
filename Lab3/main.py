import math


def fermat(n):
    # Dismiss negative or null values
    if n <= 0:
        print(n)
        return
    # Dismiss even numbers
    if n % 2 == 0:
        print(str(n // 2) + ", 2")
        return
    k = 1
    found = 0
    while 1:
        # Compute [sqrt(k*n)]
        t, _ = divmod(math.sqrt(k * n), 1)
        t = int(t)
        # Dismiss perfect roots when k = 1
        if t * t == n and k == 1:
            print(str(t) + ", " + str(t))
            return
        t0 = t
        # t0 + 1
        t += 1
        # B = 10
        while t != t0 + 10:
            # t^2 - n
            b1 = t * t - k * n
            b, _ = divmod(math.sqrt(b1), 1)
            b = int(b)
            # check if t^2 - k * n is perfect root, else continue
            if b * b == b1:
                found = 1
                break
            else:
                # t0 + ...
                t += 1
        if found == 1:
            break
        k += 1
    if (t - b) > (t + b):
        print(str((t - b) // k) + ", " + str(t + b))
    else:
        print(str(t - b) + ", " + str((t + b) // k))


if __name__ == '__main__':
    value = input("Please enter a value: ")
    print("These are the factors of the given value:")
    fermat(int(value))
