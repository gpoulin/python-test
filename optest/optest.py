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
    y=int(sys.argv[1])
    times=np.empty((4,y))
    times2=np.empty((4,y))
    name=['np', 'np_savealloc', 'weave', 'c']
    for x in xrange(y):
        arr="np.random.random((512, %d))" % 2**x
        code = "rescale_{0}(a, 10, 3)"
        setup = "import numpy as np; from __main__ import rescale_{0}; a=%s" % arr
        number = 5000
        timer = time.clock
        repeat = 5
        for j in xrange(len(name)):
            c=timeit.repeat(code.format(name[j]), setup=setup.format(name[j]), number=number, timer=timer, repeat=repeat)
            times[j,x] = np.min(c)
            times2[j,x] = np.mean(c)

    import matplotlib.pyplot as plt
    for x in xrange(4):
        plt.plot(2**np.array(range(y)),times[x,:])

    plt.legend(name,loc=2)
    plt.savefig('optest.png')
    np.savetxt('result.csv',times)

    plt.cla()

    for x in xrange(4):
        plt.plot(2**np.array(range(y)),times2[x,:])

    plt.legend(name,loc=2)
    plt.savefig('optest2.png')
    np.savetxt('result2.csv',times)



    a=np.random.random((512, 512, 4))
    x=rescale_np(a,10,3)
    y=rescale_np_savealloc(a,10,3)
    z=rescale_weave(a,10,3)
    w=rescale_c(a,10,3)
    import numpy.testing as t
    t.assert_allclose(x,y)
    t.assert_allclose(x,z)
    t.assert_allclose(x,w)
