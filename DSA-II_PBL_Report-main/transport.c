#include <stdio.h>
#include <string.h>
#define N 8
#define INF 9999
#define MAX(a,b) ((a)>(b)?(a):(b))

const char *name[N] = {"Central Station","Bus Depot","City Mall","Hospital",
                       "University","Airport","Industrial Area","Hill Colony"};
/* travel time in minutes between stops that have a direct road link, 0 = no link */
int t[N][N];
void link(int a,int b,int m){ t[a][b]=t[b][a]=m; }

void dfs(int u,int vis[]){
    vis[u]=1; printf("%s%s", name[u], ""); printf(" > ");
    for (int v=0;v<N;v++) if (t[u][v] && !vis[v]) dfs(v,vis);
}
void components(){
    int vis[N]={0}, c=0;
    for (int i=0;i<N;i++) if(!vis[i]){ c++; printf("  group %d: ",c); dfs(i,vis); printf("\n"); }
    printf("  %d separate groups of stops\n", c);
}
void bfs_hops(int s){
    int d[N], q[N], f=0, r=0;
    for (int i=0;i<N;i++) d[i]=-1;
    d[s]=0; q[r++]=s;
    while (f<r){ int u=q[f++];
        for (int v=0;v<N;v++) if (t[u][v] && d[v]<0){ d[v]=d[u]+1; q[r++]=v; } }
    for (int i=0;i<N;i++){
        if (d[i]<0) printf("  %-16s not reachable\n", name[i]);
        else printf("  %-16s %d stops away\n", name[i], d[i]);
    }
}
int find(int p[],int x){ return p[x]==x?x:(p[x]=find(p,p[x])); }
void kruskal(){
    int eu[40],ev[40],ew[40],m=0,p[N];
    for (int i=0;i<N;i++) for (int j=i+1;j<N;j++) if(t[i][j]){eu[m]=i;ev[m]=j;ew[m]=t[i][j];m++;}
    for (int i=0;i<m;i++) for (int j=i+1;j<m;j++) if(ew[j]<ew[i]){
        int x; x=ew[i];ew[i]=ew[j];ew[j]=x; x=eu[i];eu[i]=eu[j];eu[j]=x; x=ev[i];ev[i]=ev[j];ev[j]=x; }
    for (int i=0;i<N;i++) p[i]=i;
    int total=0;
    for (int i=0;i<m;i++){
        int a=find(p,eu[i]), b=find(p,ev[i]);
        if (a!=b){ p[a]=b; total+=ew[i]; printf("  %s - %s (%d min)\n", name[eu[i]], name[ev[i]], ew[i]); }
    }
    printf("  total link time = %d min\n", total);
}
void dijkstra(int s){
    int d[N], par[N], done[N]={0};
    for (int i=0;i<N;i++){ d[i]=INF; par[i]=-1; }
    d[s]=0;
    for (int c=0;c<N;c++){
        int u=-1;
        for (int i=0;i<N;i++) if(!done[i] && (u==-1||d[i]<d[u])) u=i;
        if (d[u]==INF) break;
        done[u]=1;
        for (int v=0;v<N;v++) if (t[u][v] && d[u]+t[u][v]<d[v]){ d[v]=d[u]+t[u][v]; par[v]=u; }
    }
    for (int i=0;i<N;i++){
        if (d[i]==INF){ printf("  %-16s unreachable\n", name[i]); continue; }
        int path[N], k=0;
        for (int x=i;x!=-1;x=par[x]) path[k++]=x;
        printf("  %-16s %2d min  via ", name[i], d[i]);
        for (int j=k-1;j>=0;j--) printf("%d%s", path[j], j?"-":"");
        printf("\n");
    }
}
void floyd(){
    int g[N][N];
    for (int i=0;i<N;i++) for (int j=0;j<N;j++) g[i][j]= i==j?0:(t[i][j]?t[i][j]:INF);
    for (int k=0;k<N;k++) for (int i=0;i<N;i++) for (int j=0;j<N;j++)
        if (g[i][k]+g[k][j]<g[i][j]) g[i][j]=g[i][k]+g[k][j];
    printf("      ");
    for (int j=0;j<7;j++) printf("%4d", j);
    printf("\n");
    for (int i=0;i<7;i++){ printf("  %3d ", i); for (int j=0;j<7;j++) printf("%4d", g[i][j]); printf("\n"); }
}
/* resource allocation: buses to routes */
void buses(){
    int P=3,R=5;
    int pr[3][6]={{0,200,380,540,640,700},{0,150,300,420,500,540},{0,250,400,500,560,600}};
    int dp[4][6], ch[4][6];
    for (int r=0;r<=R;r++) dp[0][r]=0;
    for (int p=1;p<=P;p++) for (int r=0;r<=R;r++){
        dp[p][r]=-1;
        for (int k=0;k<=r;k++){ int v=dp[p-1][r-k]+pr[p-1][k]; if(v>dp[p][r]){dp[p][r]=v;ch[p][r]=k;} }
    }
    int r=R, give[4];
    for (int p=P;p>=1;p--){ give[p]=ch[p][r]; r-=give[p]; }
    printf("  most passengers per hour = %d\n  Route 1: %d buses, Route 2: %d buses, Route 3: %d buses\n", dp[P][R], give[1], give[2], give[3]);
}
/* knapsack: choose new routes within a monthly budget (in lakh) */
void routes_budget(){
    const char *rn[]={"Central-Airport express","University loop","Hill Colony feeder","Industrial shuttle","Mall night service"};
    int cost[]={4,3,2,5,3}, riders[]={900,600,250,700,400}, n=5, B=9, c[6][10];
    for (int i=0;i<=n;i++) for (int w=0;w<=B;w++){
        if (!i||!w) c[i][w]=0;
        else if (cost[i-1]<=w) c[i][w]=MAX(riders[i-1]+c[i-1][w-cost[i-1]], c[i-1][w]);
        else c[i][w]=c[i-1][w];
    }
    printf("  budget %d lakh, best daily riders = %d, routes:\n", B, c[n][B]);
    int w=B;
    for (int i=n;i>0;i--) if (c[i][w]!=c[i-1][w]){ printf("    %s\n", rn[i-1]); w-=cost[i-1]; }
}
void lcs(char *x,char *y){
    int n=strlen(x), m=strlen(y), L[20][20];
    for (int i=0;i<=n;i++) for (int j=0;j<=m;j++){
        if (!i||!j) L[i][j]=0;
        else if (x[i-1]==y[j-1]) L[i][j]=1+L[i-1][j-1];
        else L[i][j]=MAX(L[i-1][j],L[i][j-1]);
    }
    char o[20]; int k=L[n][m]; o[k]=0; int i=n,j=m;
    while(i>0&&j>0){
        if (x[i-1]==y[j-1]){o[--k]=x[i-1];i--;j--;}
        else if (L[i-1][j]>=L[i][j-1]) i--; else j--;
    }
    printf("  route X: %s\n  route Y: %s\n  common stops in order: %s (%d)\n", x, y, o, L[n][m]);
}
int main(){
    link(0,1,6); link(0,2,4); link(0,3,7); link(1,2,5);
    link(2,4,8); link(3,4,3); link(4,5,12); link(2,5,15); link(3,6,9); link(5,6,6);
    /* stop 7 (Hill Colony) has no direct link yet */
    printf("Stops that can be reached from each other (DFS):\n"); components();
    printf("Fewest stops from Central Station (BFS):\n"); bfs_hops(0);
    printf("Cheapest set of links that keeps the connected stops joined (Kruskal):\n"); kruskal();
    printf("Fastest travel time from Central Station (Dijkstra):\n"); dijkstra(0);
    printf("All-pairs travel time in minutes (Floyd-Warshall), stops 0-6:\n"); floyd();
    printf("Buses for 3 routes, 5 buses available (resource allocation DP):\n"); buses();
    printf("New routes within budget (0/1 knapsack):\n"); routes_budget();
    printf("Shared stops between two routes (LCS), stops as letters:\n"); lcs("CBMHUA","CMUHA");
    return 0;
}
