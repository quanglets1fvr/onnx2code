template<
    int mv,
    int nu,

    int CStrideRow,
    int CStrideCol
>
inline void unit_update(
    const float* __restrict__ a, // mv
    const float* __restrict__ b, // nu
    float* __restrict__ C // mv x nu
) {
    for (int i = 0; i < mv; i++) {
        for (int j = 0; j < nu; j++) {
            C[j * CStrideRow + i * CStrideCol] += a[i] * b[j];
        }
    }
}

template<
    int mr,
    int nr,
    int kc,

    int CStrideRow
>
inline void test_microkernel(
    const float* __restrict__ A_kernel,  // (mr x kc) column major
    const float* __restrict__ B_kernel,  // (kc x nr) row major
    float* __restrict__ C // (mr x nr)
) {
    float AB[mr * nr]; // row major
    memset(AB, 0, mr * nr * sizeof(float));

    constexpr int mv = 1;
    constexpr int nu = 1;

    static_assert(mr % mv == 0, "must be conforming");
    static_assert(nr % nu == 0, "must be conforming");

    for (int k = 0; k < kc; k++) {
        // single outer product
        // en una columna de A y una fila de B (del zigzag)

        // loop tiling
        for (int i = 0; i < mr; i += mv) {
            for (int j = 0; j < nr; j += nu) {
                // unit update (small outer product)
                unit_update<mv, nu, nr, 1>(
                    A_kernel + j * mr + i,
                    B_kernel + i * nr + j,

                    AB + i * nr + j
                );
            }
        }

        A_kernel += mr * kc;
        B_kernel += nr * kc;
    }

    for (int j = 0; j < nr; j++) {
        for (int i = 0; i < mr; i++) {
            C[i * CStrideRow + j] += AB[mr * j + i];
        }
    }
}