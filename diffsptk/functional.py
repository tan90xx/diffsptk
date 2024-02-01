# ------------------------------------------------------------------------ #
# Copyright 2022 SPTK Working Group                                        #
#                                                                          #
# Licensed under the Apache License, Version 2.0 (the "License");          #
# you may not use this file except in compliance with the License.         #
# You may obtain a copy of the License at                                  #
#                                                                          #
#     http://www.apache.org/licenses/LICENSE-2.0                           #
#                                                                          #
# Unless required by applicable law or agreed to in writing, software      #
# distributed under the License is distributed on an "AS IS" BASIS,        #
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. #
# See the License for the specific language governing permissions and      #
# limitations under the License.                                           #
# ------------------------------------------------------------------------ #

from . import modules as nn


def decimate(x, period=1, start=0, dim=-1):
    """Decimate signal.

    Parameters
    ----------
    x : Tensor [shape=(..., T, ...)]
        Signal.

    period : int >= 1
        Decimation period, :math:`P`.

    start : int >= 0
        Start point, :math:`S`.

    dim : int
        Dimension along which to decimate the tensors.

    Returns
    -------
    Tensor [shape=(..., T/P-S, ...)]
        Decimated signal.

    """
    return nn.Decimation._forward(x, period=period, start=start, dim=dim)


def delay(x, start=0, keeplen=False, dim=-1):
    """Delay signal.

    Parameters
    ----------
    x : Tensor [shape=(..., T, ...)]
        Signal.

    start : int
        Start point, :math:`S`. If negative, advance signal.

    keeplen : bool
        If True, output has the same length of input.

    dim : int
        Dimension along which to shift the tensors.

    Returns
    -------
    Tensor [shape=(..., T-S, ...)] or [shape=(..., T, ...)]
        Delayed signal.

    """
    return nn.Delay._forward(x, start=start, keeplen=keeplen, dim=dim)


def dequantize(y, abs_max=1, n_bit=8, quantizer="mid-rise"):
    """Dequantize input.

    Parameters
    ----------
    y : Tensor [shape=(...,)]
        Quantized input.

    abs_max : float > 0
        Absolute maximum value of input.

    n_bit : int >= 1
        Number of quantization bits.

    quantizer : ['mid-rise', 'mid-tread']
        Quantizer.

    Returns
    -------
    Tensor [shape=(...,)]
        Dequantized input.

    """
    return nn.InverseUniformQuantization._forward(
        y, abs_max=abs_max, n_bit=n_bit, quantizer=quantizer
    )


def gnorm(x, gamma=0):
    """Perform cepstrum gain normalization.

    Parameters
    ----------
    x : Tensor [shape=(..., M+1)]
        Generalized cepstrum.

    Parameters
    ----------
    gamma : float in [-1, 1]
        Gamma, :math:`\\gamma`.

    Returns
    -------
    Tensor [shape=(..., M+1)]
        Normalized generalized cepstrum.

    """
    return nn.GeneralizedCepstrumGainNormalization._forward(x, gamma=gamma)


def grpdelay(b=None, a=None, *, fft_length=512, alpha=1, gamma=1, **kwargs):
    """Compute group delay.

    Parameters
    ----------
    b : Tensor [shape=(..., M+1)] or None
        Numerator coefficients.

    a : Tensor [shape=(..., N+1)] or None
        Denominator coefficients.

    fft_length : int >= 2
        Number of FFT bins, :math:`L`.

    alpha : float > 0
        Tuning parameter, :math:`\\alpha`.

    gamma : float > 0
        Tuning parameter, :math:`\\gamma`.

    Returns
    -------
    Tensor [shape=(..., L/2+1)]
        Group delay or modified group delay function.

    """
    return nn.GroupDelay._forward(
        b, a, fft_length=fft_length, alpha=alpha, gamma=gamma, **kwargs
    )


def ignorm(y, gamma=0):
    """Perform cepstrum inverse gain normalization.

    Parameters
    ----------
    y : Tensor [shape=(..., M+1)]
        Normalized generalized cepstrum.

    gamma : float in [-1, 1]
        Gamma, :math:`\\gamma`.

    Returns
    -------
    x : Tensor [shape=(..., M+1)]
        Generalized cepstrum.

    """
    return nn.GeneralizedCepstrumInverseGainNormalization._forward(y, gamma=gamma)


def interpolate(x, period=1, start=0, dim=-1):
    """Interpolate signal.

    Parameters
    ----------
    x : Tensor [shape=(..., T, ...)]
        Signal.

    period : int >= 1
        Interpolation period, :math:`P`.

    start : int >= 0
        Start point, :math:`S`.

    dim : int
        Dimension along which to interpolate the tensors.

    Returns
    -------
    Tensor [shape=(..., TxP+S, ...)]
        Interpolated signal.

    """
    return nn.Interpolation._forward(x, period=period, start=start, dim=dim)


def linear_intpl(x, upsampling_factor=1):
    """Interpolate filter coefficients.

    Parameters
    ----------
    x : Tensor [shape=(B, N, D) or (N, D) or (N,)]
        Filter coefficients.

    upsampling_factor : int >= 1
        Upsampling factor, :math:`P`.

    Returns
    -------
    y : Tensor [shape=(B, NxP, D) or (NxP, D) or (NxP,)]
        Upsampled filter coefficients.

    """
    return nn.LinearInterpolation_.forward(x, upsampling_factor=upsampling_factor)


def magic_intpl(x, magic_number=0):
    """Interpolate magic number.

    Parameters
    ----------
    x : Tensor [shape=(B, N, D) or (N, D) or (N,)]
        Data containing magic number.

    magic_number : float or Tensor
        Magic number.

    Returns
    -------
    Tensor [shape=(B, N, D) or (N, D) or (N,)]
        Data after interpolation.

    Examples
    --------
    >>> x = torch.tensor([0, 1, 2, 0, 4, 0]).float()
    >>> x
    tensor([0., 1., 2., 0., 4., 0.])
    >>> magic_intpl = diffsptk.MagicNumberInterpolation(0)
    >>> y = magic_intpl(x)
    >>> y
    tensor([1., 1., 2., 3., 4., 4.])

    """
    return nn.MagicNumberInterpolation._forward(x, magic_number=magic_number)


def phase(b=None, a=None, *, fft_length=512, unwrap=False):
    """Compute phase spectrum.

    Parameters
    ----------
    b : Tensor [shape=(..., M+1)] or None
        Numerator coefficients.

    a : Tensor [shape=(..., N+1)] or None
        Denominator coefficients.

    fft_length : int >= 2
        Number of FFT bins, :math:`L`.

    unwrap : bool
        If True, perform phase unwrapping.

    Returns
    -------
    Tensor [shape=(..., L/2+1)]
        Phase spectrum [:math:`\\pi` rad].

    """
    return nn.Phase._forward(b, a, fft_length=fft_length, unwrap=unwrap)


def quantize(x, abs_max=1, n_bit=8, quantizer="mid-rise"):
    """Quantize input.

    Parameters
    ----------
    x : Tensor [shape=(...,)]
        Input.

    abs_max : float > 0
        Absolute maximum value of input.

    n_bit : int >= 1
        Number of quantization bits.

    quantizer : ['mid-rise', 'mid-tread']
        Quantizer.

    Returns
    -------
    Tensor [shape=(...,)]
        Quantized input.

    """
    return nn.UniformQuantization._forward(
        x, abs_max=abs_max, n_bit=n_bit, quantizer=quantizer
    )


def spec(
    b=None, a=None, *, fft_length=512, eps=0, relative_floor=None, out_format="power"
):
    """Compute spectrum.

    Parameters
    ----------
    b : Tensor [shape=(..., M+1)] or None
        Numerator coefficients.

    a : Tensor [shape=(..., N+1)] or None
        Denominator coefficients.

    fft_length : int >= 2
        Number of FFT bins, :math:`L`.

    eps : float >= 0
        A small value added to power spectrum.

    relative_floor : float < 0 or None
        Relative floor in decibels.

    out_format : ['db', 'log-magnitude', 'magnitude', 'power']
        Output format.

    Returns
    -------
    Tensor [shape=(..., L/2+1)]
        Spectrum.

    """
    return nn.Spectrum._forward(
        b,
        a,
        fft_length=fft_length,
        eps=eps,
        relative_floor=relative_floor,
        out_format=out_format,
    )
