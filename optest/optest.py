import time, timeit, numpy as np
from scipy import weave
from _pure_c import rescale_c

def rescale_np(data, scale, offset):
    return (data - offset) * scale

def rescale_np_savealloc(data, scale, offset):
    aux = data - offset
    aux *= scale # reuses the first array
    return aux

def rescale_weave(data, scale, offset): # basically copied from rescaleData
    size = data.size
    input = np.ascontiguousarray(data)
    output = np.empty(data.shape, dtype=data.dtype)
    code = r"""
        for (int i = 0; i < size; ++i) {
            output[i] = ((double)input[i] - offset) * scale;
        }"""
    weave.inline(code, ["input", "size", "output", "offset", "scale"], compiler="gcc",extra_compile_args=['-march=native -mtune=native -O3' ])
    return output

if __name__ == "__main__":
    import sys
    arr="np.random.random((512, %s))" % sys.argv[1]
    code = "rescale_{0}(%s, 10, 3)"%arr
    setup = "import numpy as np; from __main__ import rescale_{0}; " + code
    number = 5000
    timer = time.clock
    ti=np.mean(timeit.repeat(arr, setup="import numpy as np",
                        number=number, timer=timer))
    print(np.mean(np.array(timeit.repeat(code.format("np"), setup=setup.format("np"),
                        number=number, timer=timer))-ti))
    print(np.mean(np.array(timeit.repeat(code.format("np_savealloc"), setup=setup.format("np_savealloc"),
                        number=number, timer=timer))-ti))
    print(np.mean(np.array(timeit.repeat(code.format("c"), setup=setup.format("c"),
                        number=number, timer=timer))-ti))
    print(np.mean(np.array(timeit.repeat(code.format("weave"), setup=setup.format("weave"),
                        number=number, timer=timer))-ti))
    a=np.random.random((512, 512, 4))
    x=rescale_np(a,10,3)
    y=rescale_np_savealloc(a,10,3)
    z=rescale_weave(a,10,3)
    w=rescale_c(a,10,3)
    import numpy.testing as t
    t.assert_allclose(x,y)
    t.assert_allclose(x,z)
    t.assert_allclose(x,w)
