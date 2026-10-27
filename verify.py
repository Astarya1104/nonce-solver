import sys
cnf,sol=sys.argv[1],sys.argv[2]
L=open(cnf).read().split("\n"); n,m,K=map(int,L[0].split()); a=open(sol).read().strip()
assert len(a)==n and set(a)<=set("01")
for l in L[1:m+1]:
    if not any((int(x)>0)==(a[abs(int(x))-1]=="1") for x in l.split()): sys.exit(1)
print("VERIFIED")
