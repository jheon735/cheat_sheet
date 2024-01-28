#simpson 적분

def simp(x, f, n): #x는 x값, f는 y값, n는 갯수
    result = 0.0
    num3 = (n - 1) // 3
    h = x  # df

    result -= f[0]
    for i in range(num3):
        j = 3 * i
        result += 2. * f[j]
        result += 3. * f[j + 1]
        result += 3. * f[j + 2]

    result += f[3 * num3]

    result *= 3. / 8. * h

    if (n - 1) == 3 * num3 + 2:
        result += h / 3. * (f[3 * num3] + 4 * f[3 * num3 + 1] + f[3 * num3 + 2])
    elif (n - 1) == 3 * num3 + 1:
        result += h / 2. * (f[3 * num3] + f[3 * num3 + 1])

    return result