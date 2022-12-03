︠532abfc9-6239-4eb0-b416-4aa77cf8fd99s︠
F = FiniteField(0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F)
C = EllipticCurve([F(0), F(7)])
G = C.lift_x(0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798)
N = FiniteField(C.order())
n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
d = 2196
Q = d*G

def sign(z):
    r = 0
    s = 0
    while s == 0:
        k = 1
        while r == 0:
            k = N.random_element()
            (x1, y1) = (int(k)*G).xy()
            r = x1
        s = k^(-1)*(z+N(r)*d)
    print(f'random k: {k}')
    return r, s

def verify(z, r, s):
    w = N(s) ^ (-1)
    u1 = int(z * w); u2 = int(N(r) * w)
    (x1, y1) = (u1*G + u2*Q).xy()
    return r == x1

e = 0x000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f
z = 0x000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f

r, s = sign(z)
print(f'r: {r}\ns: {s}')
print(verify(z, r, s))
︡50a0d66a-14ee-4b5f-9fb7-638095198db0︡{"stdout":"random k: 109740109892235532878306356133800093045252333191458370520279557037312996874868\n"}︡{"stdout":"r: 70000326365577208095100227701225545430768716907230157761227603089793312808504\ns: 71612401756312716822803358871590990690042855586470157310817110099955546623103\n"}︡{"stdout":"True\n"}︡{"done":true}









