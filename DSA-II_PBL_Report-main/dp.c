#include <stdio.h>
#include <string.h>
#define MAX(a,b) ((a)>(b)?(a):(b))

void knapsack(int W, int n, int wt[], int val[]){
    int c[10][20];
    for (int i=0;i<=n;i++) for (int w=0;w<=W;w++){
        if (i==0||w==0) c[i][w]=0;
        else if (wt[i-1]<=w) c[i][w]=MAX(val[i-1]+c[i-1][w-wt[i-1]], c[i-1][w]);
        else c[i][w]=c[i-1][w];
    }
    for (int i=0;i<=n;i++){ printf("  "); for (int w=0;w<=W;w++) printf("%2d ", c[i][w]); printf("\n"); }
    printf("  max value = %d, items taken:", c[n][W]);
    int w=W; for (int i=n;i>0;i--) if (c[i][w]!=c[i-1][w]){ printf(" %d", i); w-=wt[i-1]; }
    printf("\n");
}
void lcs(char *x, char *y){
    int n=strlen(x), m=strlen(y), L[20][20];
    for (int i=0;i<=n;i++) for (int j=0;j<=m;j++){
        if (i==0||j==0) L[i][j]=0;
        else if (x[i-1]==y[j-1]) L[i][j]=1+L[i-1][j-1];
        else L[i][j]=MAX(L[i-1][j], L[i][j-1]);
    }
    char out[20]; int k=L[n][m]; out[k]='\0';
    int i=n, j=m;
    while (i>0&&j>0){
        if (x[i-1]==y[j-1]){ out[--k]=x[i-1]; i--; j--; }
        else if (L[i-1][j]>=L[i][j-1]) i--; else j--;
    }
    printf("  %s and %s -> length %d, one LCS = %s\n", x, y, L[n][m], out);
}
int m[10][10], s[10][10];
void paren(int i,int j){
    if (i==j) printf("%c",'A'+i-1);
    else { printf("("); paren(i,s[i][j]); paren(s[i][j]+1,j); printf(")"); }
}
void mcm(int p[], int n){
    for (int i=1;i<=n;i++) m[i][i]=0;
    for (int d=1; d<n; d++)
        for (int i=1;i<=n-d;i++){
            int j=i+d; m[i][j]=1<<30;
            for (int k=i;k<j;k++){
                int q=m[i][k]+m[k+1][j]+p[i-1]*p[k]*p[j];
                if (q<m[i][j]){ m[i][j]=q; s[i][j]=k; }
            }
        }
    printf("  minimum multiplications = %d, order = ", m[1][n]); paren(1,n); printf("\n");
}
void resource(int P, int R, int profit[][10]){
    /* profit[p][r] = profit of project p given r units */
    int dp[10][10], ch[10][10];
    for (int r=0;r<=R;r++) dp[0][r]=0;
    for (int p=1;p<=P;p++) for (int r=0;r<=R;r++){
        dp[p][r]=-1;
        for (int k=0;k<=r;k++){
            int v=dp[p-1][r-k]+profit[p-1][k];
            if (v>dp[p][r]){ dp[p][r]=v; ch[p][r]=k; }
        }
    }
    printf("  max profit = %d, units given to projects:", dp[P][R]);
    int r=R; int give[10];
    for (int p=P;p>=1;p--){ give[p]=ch[p][r]; r-=give[p]; }
    for (int p=1;p<=P;p++) printf(" P%d=%d", p, give[p]);
    printf("\n");
}
int main(){
    printf("Knapsack, slide example (W=5):\n");
    int wt1[]={2,3,4,5}, v1[]={3,4,5,6}; knapsack(5,4,wt1,v1);
    printf("Knapsack, W=8:\n"); knapsack(8,4,wt1,v1);
    printf("LCS:\n");
    lcs("BCDAACD","ACDBAC"); lcs("STONE","LONGEST");
    printf("Matrix chain:\n");
    int p1[]={10,30,5,60,8}; mcm(p1,4);
    int p2[]={5,4,6,2,7}; mcm(p2,4);
    printf("Resource allocation (3 projects, 5 units):\n");
    int pr[3][10]={{0,2,4,6,7,8},{0,1,3,5,6,7},{0,3,5,6,7,9}}; resource(3,5,pr);
    return 0;
}
