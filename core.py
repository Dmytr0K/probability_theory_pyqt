def sochetanie(m,n):
    return razmeshenie(m, n)//fact(m)


def sochetanie_s_povtoretiem(m,n):
    return sochetanie(m, n+m-1)


def razmeshenie (m,n):
    temp = n-m
    res = 1
    for i in range(temp + 1, n + 1):
        res *= i
    return res


def razmeschenie_s_povtoreniem(m,n):
    return n**m


def perestanovka (n):
    return fact(n)


def perestanovka_s_povtoreniem(n, a_list):
    nk = 1;
    for i in a_list:
        nk *= fact(i)
    return fact(n)//nk


def fact(N):
    if N < 0:
        return 0
    elif N == 0:
        return 1
    else:
        return N*fact(N-1)