#include <bits/stdc++.h>
#include <signal.h>

using namespace std;

void segfault_sigaction(int signal, siginfo_t *si, void *arg)
{
    printf("Caught segfault at address %p\n", si->si_addr);
    exit(0);
}

int main() {
    long n;
    long m;
    long max = 0;
    long *arf;
    
    struct sigaction sa;

    memset(&sa, 0, sizeof(struct sigaction));
    sigemptyset(&sa.sa_mask);

    sa.sa_sigaction = segfault_sigaction;
    sa.sa_flags   = SA_SIGINFO;

    sigaction(SIGSEGV, &sa, NULL);
    cin >> n >> m;

    arf = (long*)malloc (sizeof(long) * n);
    memset(arf, 0, sizeof(long) * n);
    
    for(long a0 = 0; a0 < m; a0++)
    {
        long a;
        long b;
        long k;
        cin >> a >> b >> k;
        try
        {
            for (long j = a-1; j <= b-1; j++)
            {
                arf [j]  += k;
            }
        }
        catch (exception &e)
        {
            cerr << "Exception catched : " << e.what() << endl;
            break;
        }
    }
    
    for (long g = 0; g < n ; g++)
        if (arf[g] > max)
            max = arf[g];
    cout << max;
    
    return 0;
}