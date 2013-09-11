#include <Python.h>
#include <numpy/arrayobject.h>

//Header (.h)
static PyObject *rescale_c(PyObject *self, PyObject *args);

//Doc of the module
static char module_docstring[] ="Just a test";

//Doc of the functions
static char rescale_c_docstring[] = "Just a test";

//Definition of the function see by python
static PyMethodDef module_methods[] = {
  {"rescale_c",rescale_c, METH_VARARGS,rescale_c_docstring},
  {NULL,NULL,0,NULL}
};

#if PY_MAJOR_VERSION >= 3
#define IS_PY3K
static struct PyModuleDef _pure_c_module = {
   PyModuleDef_HEAD_INIT,
   "_pure_c",   /* name of module */
   module_docstring, /* module documentation, may be NULL */
   -1,       /* size of per-interpreter state of the module,
                or -1 if the module keeps state in global variables. */
   module_methods
};

PyMODINIT_FUNC PyInit__pure_c(void)
{
    import_array();
    return PyModule_Create(&_pure_c_module);
}

#else
PyMODINIT_FUNC init_pure_c(void)
{
  PyObject *m = Py_InitModule3("_pure_c", module_methods, module_docstring);
  if (m==NULL)
    return;
  import_array()
}
#endif

static PyObject *rescale_c(PyObject *self, PyObject *args)
{
  PyObject *data, *output;
  PyArrayObject *data_array;
  double offset, scale, *datad, *out;
  unsigned int l, i;

  //Extract argument
  if (!PyArg_ParseTuple(args, "Odd", &data, &scale, &offset)) return NULL;
  data_array = (PyArrayObject*)PyArray_FROM_OTF(data, NPY_DOUBLE, NPY_ARRAY_CARRAY_RO);

  //Size of the array
  l=(int)PyArray_SIZE(data_array);

  //Create an array to store the result
  output=PyArray_EMPTY(PyArray_NDIM(data_array),PyArray_SHAPE(data_array),NPY_DOUBLE,0);

  //Do the calcul
  datad=(double*)PyArray_DATA(data_array);
  out=(double*)PyArray_DATA(output);
  for (i=0; i<l; ++i){
    out[i]=(datad[i]-offset)*scale;
  }

  Py_DECREF(data_array);

  //return Value
  return (PyObject*) output;
}
