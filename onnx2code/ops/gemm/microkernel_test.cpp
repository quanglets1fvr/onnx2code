template <
    int mv,
    int nu,

    int CStrideRow,
    int CStrideCol>
inline void unit_update(
    const float* __restrict__ a,  // mv
    const float* __restrict__ b,  // nu
    float* __restrict__ C         // mv x nu
) {
    __asm__ __volatile__(
        "vbroadcastss %1, %%ymm0 \n"
        "vmovups %0, %%ymm1 \n"
        "vfmaddps %%ymm0, %2, %%ymm0, %%ymm1 \n"
        "vmovups %%ymm0, %2 \n"
        :        // no output
        :        // inputs
        "m"(a),  // %0
        "m"(b),  // %1
        "m"(C)   // %2
        : "ymm0", "ymm1"
    );
}

template <
    int mr,
    int nr,
    int kc,

    int CStrideRow>
inline void test_microkernel(
    const float* __restrict__ A_kernel,  // (mr x kc) column major
    const float* __restrict__ B_kernel,  // (kc x nr) row major
    float* __restrict__ C                // (mr x nr)
) {
    float AB[mr * nr];  // row major
    memset(AB, 0, mr * nr * sizeof(float));

    constexpr int mv = 8;
    constexpr int nu = 1;

    static_assert(mr % mv == 0, "must be conforming");
    static_assert(nr % nu == 0, "must be conforming");

    for (int k = 0; k < kc; k++) {
        // single outer product
        // en una columna de A y una fila de B (del zigzag)

        // loop tiling
        for (int j = 0; j < nr; j += nu) {
            for (int i = 0; i < mr; i += mv) {
                // unit update (small outer product)
                unit_update<mv, nu, nr, 1>(
                    A_kernel + i,
                    B_kernel + j,

                    AB + j * mr + 
                );
            }
        }

        // advance one row of A and one column of B
        A_kernel += mr;
        B_kernel += nr;
    }

    for (int j = 0; j < nr; j++) {
        for (int i = 0; i < mr; i++) {
            C[i * CStrideRow + j] += AB[mr * j + i];
        }
    }
}
