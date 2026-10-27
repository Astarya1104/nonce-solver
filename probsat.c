// probSAT for k-SAT, DIMACS-free simple format: n m then m lines of k lits
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <time.h>
static unsigned long long s; static inline unsigned long long rnd(){s^=s<<13;s^=s>>7;s^=s<<17;return s;}
static inline double rf(){return (rnd()>>11)*(1.0/9007199254740992.0);}
int main(int argc,char**argv){
 FILE*f=fopen(argv[1],"r"); double cb=argc>2?atof(argv[2]):3.7; s=argc>3?atoll(argv[3]):12345; double tl=argc>4?atof(argv[4]):60; const char*init=argc>5?argv[5]:NULL;
 int n,m,K; if(fscanf(f,"%d %d %d",&n,&m,&K)!=3)return 1;
 int*cl=malloc(sizeof(int)*m*K); for(int i=0;i<m*K;i++) if(fscanf(f,"%d",&cl[i])!=1) return 1;
 int L=2*n+2; int*cnt=calloc(L,4);
 #define IDX(l) ((l)>0?2*(l):-2*(l)+1)
 for(int i=0;i<m*K;i++)cnt[IDX(cl[i])]++;
 int*st=malloc(4*(L+1)); st[0]=0; for(int i=0;i<L;i++)st[i+1]=st[i]+cnt[i];
 int*occ=malloc(4*m*K); int*pos=calloc(L,4); for(int c=0;c<m;c++)for(int j=0;j<K;j++){int x=IDX(cl[c*K+j]); occ[st[x]+pos[x]++]=c;}
 char*a=malloc(n+1); for(int v=1;v<=n;v++) a[v]= init? (init[v-1]=='1') : (rnd()&1);
 int*nt=calloc(m,4); int*crit=calloc(m,4); int*fl=malloc(4*m); int*wh=malloc(4*m); int nf=0;
 double pr[64]; for(int i=0;i<64;i++)pr[i]=pow(cb,-i);
 for(int c=0;c<m;c++){for(int j=0;j<K;j++){int l=cl[c*K+j]; if((l>0)==a[abs(l)]){nt[c]++;crit[c]^=abs(l);}} if(!nt[c]){wh[c]=nf;fl[nf++]=c;}}
 int*brk=calloc(n+1,4); for(int c=0;c<m;c++) if(nt[c]==1) brk[crit[c]]++;
 clock_t t0=clock(); long long flips=0; int best=nf;
 while(nf>0){
  if((flips&0xffff)==0){ if((double)(clock()-t0)/CLOCKS_PER_SEC>tl) break; }
  int c=fl[rnd()%nf]; double p[8],sum=0; for(int j=0;j<K;j++){int v=abs(cl[c*K+j]); int b=brk[v]; p[j]=pr[b<63?b:63]; sum+=p[j];}
  double r=rf()*sum; int j=0; for(;j<K-1;j++){r-=p[j]; if(r<=0)break;}
  int v=abs(cl[c*K+j]); a[v]^=1; flips++;
  int tl_=a[v]? v:-v; // now-true literal
  int x=IDX(tl_); for(int i=st[x];i<st[x+1];i++){int d=occ[i]; nt[d]++; if(nt[d]==1){int q=fl[--nf]; fl[wh[d]]=q; wh[q]=wh[d]; brk[v]++; crit[d]=v;} else if(nt[d]==2){brk[crit[d]]--; crit[d]^=v;} else crit[d]^=v;}
  x=IDX(-tl_); for(int i=st[x];i<st[x+1];i++){int d=occ[i]; nt[d]--; if(nt[d]==0){wh[d]=nf;fl[nf++]=d; brk[v]--; crit[d]=0;} else if(nt[d]==1){crit[d]^=v; brk[crit[d]]++;} else crit[d]^=v;}
  if(nf<best){best=nf;}
 }
 fprintf(stderr,"unsat=%d best=%d flips=%lld time=%.1f\n",nf,best,flips,(double)(clock()-t0)/CLOCKS_PER_SEC);
 if(nf==0){for(int v=1;v<=n;v++)putchar('0'+a[v]);putchar('\n');}
 return nf?1:0;
}
