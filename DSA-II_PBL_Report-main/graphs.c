#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
#define V 5
#define INF 99999

struct Node { int dest; struct Node* next; };
struct AdjList { struct Node* head; };

struct Node* createNode(int d){
    struct Node* n = (struct Node*)malloc(sizeof(struct Node));
    n->dest = d; n->next = NULL; return n;
}
void addEdge(struct AdjList adj[], int s, int t){
    struct Node* n = createNode(t); n->next = adj[s].head; adj[s].head = n;
    n = createNode(s); n->next = adj[t].head; adj[t].head = n;
}
void dfsRec(struct AdjList adj[], int visited[], int s){
    visited[s] = 1; printf("%d ", s);
    for (struct Node* c = adj[s].head; c; c = c->next)
        if (!visited[c->dest]) dfsRec(adj, visited, c->dest);
}
void bfs(struct AdjList adj[], int s){
    int visited[10] = {0}, q[10], f = 0, r = 0;
    visited[s] = 1; q[r++] = s;
    while (f < r){
        int u = q[f++]; printf("%d ", u);
        for (struct Node* c = adj[u].head; c; c = c->next)
            if (!visited[c->dest]){ visited[c->dest] = 1; q[r++] = c->dest; }
    }
}
/* connected components using DFS */
int components(struct AdjList adj[], int n){
    int visited[10] = {0}, count = 0;
    for (int i = 0; i < n; i++)
        if (!visited[i]){ dfsRec(adj, visited, i); count++; printf("| "); }
    return count;
}

/* weighted graph, 5 vertices A..E */
int w[V][V] = {
    {0, 2, 0, 6, 0},
    {2, 0, 3, 8, 5},
    {0, 3, 0, 0, 7},
    {6, 8, 0, 0, 9},
    {0, 5, 7, 9, 0}};

int find(int p[], int x){ return p[x]==x ? x : (p[x]=find(p,p[x])); }
void kruskal(){
    int eu[20], ev[20], ew[20], m = 0, p[V];
    for (int i=0;i<V;i++) for (int j=i+1;j<V;j++) if (w[i][j]){ eu[m]=i; ev[m]=j; ew[m]=w[i][j]; m++; }
    for (int i=0;i<m;i++) for (int j=i+1;j<m;j++) if (ew[j]<ew[i]){
        int t; t=ew[i];ew[i]=ew[j];ew[j]=t; t=eu[i];eu[i]=eu[j];eu[j]=t; t=ev[i];ev[i]=ev[j];ev[j]=t; }
    for (int i=0;i<V;i++) p[i]=i;
    int total=0, cnt=0;
    for (int i=0;i<m && cnt<V-1;i++){
        int a=find(p,eu[i]), b=find(p,ev[i]);
        if (a!=b){ p[a]=b; total+=ew[i]; cnt++; printf("  %c-%c (%d)\n", 'A'+eu[i], 'A'+ev[i], ew[i]); }
        else printf("  %c-%c (%d) skipped, forms a cycle\n", 'A'+eu[i], 'A'+ev[i], ew[i]);
    }
    printf("  total = %d\n", total);
}
void prim(){
    int in[V]={0}, key[V], par[V], total=0;
    for (int i=0;i<V;i++){ key[i]=INF; par[i]=-1; }
    key[0]=0;
    for (int c=0;c<V;c++){
        int u=-1;
        for (int i=0;i<V;i++) if(!in[i] && (u==-1 || key[i]<key[u])) u=i;
        in[u]=1; total+=key[u];
        if (par[u]!=-1) printf("  %c-%c (%d)\n", 'A'+par[u], 'A'+u, key[u]);
        for (int v=0;v<V;v++) if (w[u][v] && !in[v] && w[u][v]<key[v]){ key[v]=w[u][v]; par[v]=u; }
    }
    printf("  total = %d\n", total);
}
void dijkstra(int s){
    int d[V], done[V]={0};
    for (int i=0;i<V;i++) d[i]=INF;
    d[s]=0;
    for (int c=0;c<V;c++){
        int u=-1;
        for (int i=0;i<V;i++) if(!done[i] && (u==-1 || d[i]<d[u])) u=i;
        done[u]=1;
        for (int v=0;v<V;v++) if (w[u][v] && d[u]+w[u][v]<d[v]) d[v]=d[u]+w[u][v];
    }
    for (int i=0;i<V;i++) printf("  A to %c = %d\n", 'A'+i, d[i]);
}
void bellman(){
    /* directed graph with a negative edge, no negative cycle */
    int eu[]={0,0,1,1,1,3,3,4}, ev[]={1,2,2,3,4,2,1,3}, ew[]={6,7,8,5,-4,-3,-2,7};
    int E=8, d[V];
    for (int i=0;i<V;i++) d[i]=INF;
    d[0]=0;
    for (int i=1;i<V;i++)
        for (int e=0;e<E;e++) if (d[eu[e]]!=INF && d[eu[e]]+ew[e]<d[ev[e]]) d[ev[e]]=d[eu[e]]+ew[e];
    int neg=0;
    for (int e=0;e<E;e++) if (d[eu[e]]!=INF && d[eu[e]]+ew[e]<d[ev[e]]) neg=1;
    for (int i=0;i<V;i++) printf("  A to %c = %d\n", 'A'+i, d[i]);
    printf("  negative cycle: %s\n", neg?"yes":"no");
}
void floyd(){
    int g[4][4]={{0,3,INF,7},{8,0,2,INF},{5,INF,0,1},{2,INF,INF,0}};
    for (int k=0;k<4;k++) for (int i=0;i<4;i++) for (int j=0;j<4;j++)
        if (g[i][k]+g[k][j]<g[i][j]) g[i][j]=g[i][k]+g[k][j];
    for (int i=0;i<4;i++){ printf("  "); for (int j=0;j<4;j++) printf("%3d ", g[i][j]); printf("\n"); }
}

int main(){
    struct AdjList adj[V];
    for (int i=0;i<V;i++) adj[i].head=NULL;
    int edges[][2]={{1,2},{1,0},{2,0},{2,3},{2,4}};
    for (int i=0;i<5;i++) addEdge(adj, edges[i][0], edges[i][1]);
    printf("DFS from 1: "); int vis[V]={0}; dfsRec(adj, vis, 1); printf("\n");
    printf("BFS from 1: "); bfs(adj, 1); printf("\n");

    struct AdjList g3[6];
    for (int i=0;i<6;i++) g3[i].head=NULL;
    addEdge(g3,0,1); addEdge(g3,0,2); addEdge(g3,1,3); addEdge(g3,1,4); addEdge(g3,2,5);
    printf("Second graph, DFS from 0: "); int v3[10]={0}; dfsRec(g3, v3, 0); printf("\n");
    printf("Second graph, BFS from 0: "); bfs(g3, 0); printf("\n");

    struct AdjList g2[6];
    for (int i=0;i<6;i++) g2[i].head=NULL;
    addEdge(g2,0,1); addEdge(g2,1,2); addEdge(g2,3,4);
    printf("Components (6 vertices, edges 0-1,1-2,3-4): ");
    int c = components(g2, 6); printf("\ncount = %d\n", c);

    printf("Kruskal:\n"); kruskal();
    printf("Prim from A:\n"); prim();
    printf("Dijkstra from A:\n"); dijkstra(0);
    printf("Bellman-Ford from A:\n"); bellman();
    printf("Floyd-Warshall:\n"); floyd();
    return 0;
}
