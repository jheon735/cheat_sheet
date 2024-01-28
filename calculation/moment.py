def moment(freqs, psd, num):
    M0 = simp(freqs, psd, num) #적분, 0차 모멘트
    NM0 = psd / M0
    dope_f = simp(freqs, NM0 * freqs, num)
    width_f = np.sqrt(abs(self.simp(freqs, NM0 * (freqs - dope_f) ** 2, num)))  # 표준편차값임
    skew = simp(freqs, NM0 * (freqs - dope_f) ** 3, num) / width_f ** (3)  # normalized 3rd central moment