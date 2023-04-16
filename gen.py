# from random import randint
# alph = "qwertyuiopasdfghjklzxcvbnm"
# for i in range(50):
#     print(f"{randint(0, 30) * alph[randint(0, len(alph)-1)]}", end='')

from random import randint
alph = "01234566789ABCDEF"
for i in range(100):
    print(f"{alph[randint(0, len(alph)-1)]}{alph[randint(0, len(alph)-1)]}" * randint(1, 8), end='')