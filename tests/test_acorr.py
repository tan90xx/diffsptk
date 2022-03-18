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

import numpy as np
import pytest
import torch

import diffsptk
from tests.utils import call
from tests.utils import check


def test_compatibility(M=3, L=14, B=2):
    acorr = diffsptk.AutocorrelationAnalysis(M, L).double()
    x = torch.from_numpy(call(f"nrand -l {B*L}", double=True).reshape(-1, L))
    y = acorr.forward(x).cpu().numpy()

    y_ = call(f"nrand -l {B*L} | acorr -l {L} -m {M}").reshape(-1, M + 1)
    assert np.allclose(y, y_)


@pytest.mark.parametrize("device", ["cpu", "cuda"])
def test_differentiable(device, M=3, L=14, B=2):
    if device == "cuda" and not torch.cuda.is_available():
        return

    acorr = diffsptk.AutocorrelationAnalysis(M, L)
    x = torch.randn(B, L, requires_grad=True, device=device)
    check(acorr, x)
