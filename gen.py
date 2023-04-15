from random import randint
alph = "qwertyuiopasdfghjklzxcvbnm"
for i in range(50):
    print(f"{randint(0, 30) * alph[randint(0, len(alph)-1)]}", end='')