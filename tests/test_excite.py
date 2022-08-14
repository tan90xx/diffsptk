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
import tests.utils as U


@pytest.mark.parametrize("device", ["cpu", "cuda"])
def test_compatibility(device, P=80):
    if device == "cuda" and not torch.cuda.is_available():
        return

    excite = diffsptk.ExcitationGeneration(P).to(device)

    def eq(y_hat, y):
        return np.allclose(y_hat[0, :P], y[..., :P])

    # Note there is no complete compatibility with SPTK4.
    U.check_compatibility(
        device,
        excite,
        [],
        f"step -v {P//2} -l 4",
        f"excite -p {P} -n",
        [],
        dx=2,
        eq=eq,
    )

    cmd = "x2x +sd tools/SPTK/asset/data.short | "
    cmd += f"pitch -s 16 -p {P} -o 0 -a 1 > excite.tmp1"
    U.call(cmd, get=False)

    cmd = "x2x +sd tools/SPTK/asset/data.short | "
    cmd += f"frame -p {P} -l 400 | window -l 400 -L 512 | "
    cmd += "mgcep -l 512 -m 24 -a 0.42 > excite.tmp2"
    U.call(cmd, get=False)

    pitch = U.call("cat excite.tmp1")
    e = excite(torch.from_numpy(pitch).to(device))
    e.cpu().numpy().tofile("excite.tmp3")

    cmd = f"mglsadf -m 24 -a 0.42 -P 7 -p {P} excite.tmp2 < excite.tmp3 | "
    cmd += f"pitch -s 16 -p {P} -o 0 -a 1"
    pitch2 = U.call(cmd)

    vuv_error = 0
    for p, q in zip(pitch, pitch2):
        if p != 0 and q != 0:
            assert np.abs(p - q) < 10
        elif not (p == 0 and q == 0):
            vuv_error += 1
            assert vuv_error < 10

    U.call("rm -f excite.tmp?", get=False)