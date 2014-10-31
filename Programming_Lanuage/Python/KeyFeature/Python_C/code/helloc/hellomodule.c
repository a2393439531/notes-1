/* 
* @Author: joshua
* @Date:   2014-10-24 12:52:42
* @Last Modified by:   Joshua
* @Last Modified time: 2014-10-24 14:45:12
*/

#include <Python.h>

static PyObject* say_hello(PyObject* self, PyObject* args)
{
    const char* name;

    if (!PyArg_ParseTuple(args, "s", &name))
        return NULL;

    printf("Hello %s\n", name);

    Py_RETURN_NONE;
}

static PyMethodDef helloMethods[] = 
{
    {"say_hello", say_hello, METH_VARARGS, "Greet somebody."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef hellomodule = {
    PyModuleDef_HEAD_INIT,
    "hello",
    NULL,
    -1,
    helloMethods
};

PyMODINIT_FUNC PyInit_hello(void)
{
    return PyModule_Create(&hellomodule);
}
