from scipy.signal import lfilter

class WallFilter:
    def __init__(self, freq_coefs) -> None:
        # based on frequnecy coefficents find IIR filter coefficients using the Gauss-Newton method
        pass