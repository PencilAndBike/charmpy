import sys
import platform
from cffi import FFI
ffibuilder = FFI()


if platform.system() == 'Darwin':
    extra_link_args=["-Wl,-rpath,@loader_path/../.libs"]
else:
    extra_link_args=["-Wl,-rpath,$ORIGIN/../.libs"]


ffibuilder.set_source("charmpy.charmlib._charmlib_cffi",
   r""" // passed to the real C compiler
        #include "charm.h"
        #include "spanningTree.h"

        // import reduction structures defined on Charm side

        struct CkReductionTypesExt {
          int nop;
          int sum_char;
          int sum_short;
          int sum_int;
          int sum_long;
          int sum_long_long;
          int sum_uchar;
          int sum_ushort;
          int sum_uint;
          int sum_ulong;
          int sum_ulong_long;
          int sum_float;
          int sum_double;
          int product_char;
          int product_short;
          int product_int;
          int product_long;
          int product_long_long;
          int product_uchar;
          int product_ushort;
          int product_uint;
          int product_ulong;
          int product_ulong_long;
          int product_float;
          int product_double;
          int max_char;
          int max_short;
          int max_int;
          int max_long;
          int max_long_long;
          int max_uchar;
          int max_ushort;
          int max_uint;
          int max_ulong;
          int max_ulong_long;
          int max_float;
          int max_double;
          int min_char;
          int min_short;
          int min_int;
          int min_long;
          int min_long_long;
          int min_uchar;
          int min_ushort;
          int min_uint;
          int min_ulong;
          int min_ulong_long;
          int min_float;
          int min_double;
          int external_py;
        };

        extern struct CkReductionTypesExt charm_reducers;
        struct CkReductionTypesExt *getReducersStruct() {
          return &charm_reducers;
        }

        extern const char* const CmiCommitID;
        const char* get_charm_commit_id() {
          return CmiCommitID;
        }

        struct ContributeInfo {
          int cbEpIdx;            // index of entry point at reduction target
          int fid;                // future ID (used when reduction target is a future)
          void *data;             // data contributed for reduction
          int numelems;           // number of elements in data
          int dataSize;           // size of data in bytes
          int redType;            // type of reduction (ReducerTypes)
          int id;                 // ID of the contributing array/group
          int *idx;               // index of the contributing chare array/group element
          int ndims;              // number of dimensions in index
          int contributorType;    // type of contributor
        };

    """,
    libraries=['charm'],
    include_dirs=['charm_src/charm/include'],
    library_dirs=['charmpy/.libs'],
    extra_compile_args=['-g0', '-O3'],
    extra_link_args=extra_link_args)

ffibuilder.cdef("""
    void StartCharmExt(int argc, char **argv);
    int CkMyPeHook();
    int CkNumPesHook();
    void realCkExit(int exitcode);
    void CmiAbort(const char *);
    void CmiPrintf(const char *);
    void LBTurnInstrumentOn();
    void LBTurnInstrumentOff();
    void free(void *ptr);
    void getPETopoTreeEdges(int pe, int rootPE, int *pes, int numpes, unsigned int bfactor,
                            int *parent, int *child_count, int **children);

    struct CkReductionTypesExt {
        int nop;
        int sum_char;
        int sum_short;
        int sum_int;
        int sum_long;
        int sum_long_long;
        int sum_uchar;
        int sum_ushort;
        int sum_uint;
        int sum_ulong;
        int sum_ulong_long;
        int sum_float;
        int sum_double;
        int product_char;
        int product_short;
        int product_int;
        int product_long;
        int product_long_long;
        int product_uchar;
        int product_ushort;
        int product_uint;
        int product_ulong;
        int product_ulong_long;
        int product_float;
        int product_double;
        int max_char;
        int max_short;
        int max_int;
        int max_long;
        int max_long_long;
        int max_uchar;
        int max_ushort;
        int max_uint;
        int max_ulong;
        int max_ulong_long;
        int max_float;
        int max_double;
        int min_char;
        int min_short;
        int min_int;
        int min_long;
        int min_long_long;
        int min_uchar;
        int min_ushort;
        int min_uint;
        int min_ulong;
        int min_ulong_long;
        int min_float;
        int min_double;
        int external_py;
        ...;
    };

    struct ContributeInfo {
      int cbEpIdx;            // index of entry point at reduction target
      int fid;                // future ID (used when reduction target is a future)
      void *data;             // data contributed for reduction
      int numelems;           // number of elements in data
      int dataSize;           // size of data in bytes
      int redType;            // type of reduction (ReducerTypes)
      int id;                 // ID of the contributing array/group
      int *idx;               // index of the contributing chare array/group element
      int ndims;              // number of dimensions in index
      int contributorType;    // type of contributor
      ...;
    };

    void *getReducersStruct();

    const char* get_charm_commit_id();

    void CkRegisterReadonlyExt(const char *name, const char *type, size_t msgSize, char *msg);
    void CkRegisterMainChareExt(const char *s, int numEntryMethods, int *chareIdx, int *startEpIdx);
    void CkRegisterGroupExt(const char *s, int numEntryMethods, int *chareIdx, int *startEpIdx);
    void CkRegisterArrayExt(const char *s, int numEntryMethods, int *chareIdx, int *startEpIdx);
    void CkRegisterArrayMapExt(const char *s, int numEntryMethods, int *chareIdx, int *startEpIdx);

    int CkCreateGroupExt(int cIdx, int eIdx, int num_bufs, char **bufs, int *buf_sizes);
    int CkCreateArrayExt(int cIdx, int ndims, int *dims, int eIdx, int num_bufs, char **bufs, int *buf_sizes, int map_gid);
    void CkInsertArrayExt(int aid, int ndims, int *index, int epIdx, int onPE, int num_bufs, char **bufs, int *buf_sizes);
    void CkArrayDoneInsertingExt(int aid);
    void CkMigrateExt(int aid, int ndims, int *index, int toPe);

    void CkChareExtSend(int onPE, void *objPtr, int epIdx, char *msg, int msgSize);
    void CkChareExtSend_multi(int onPE, void *objPtr, int epIdx, int num_bufs, char **bufs, int *buf_sizes);
    void CkGroupExtSend(int gid, int pe, int epIdx, char *msg, int msgSize);
    void CkGroupExtSend_multi(int gid, int pe, int epIdx, int num_bufs, char **bufs, int *buf_sizes);
    void CkArrayExtSend(int aid, int *idx, int ndims, int epIdx, char *msg, int msgSize);
    void CkArrayExtSend_multi(int aid, int *idx, int ndims, int epIdx, int num_bufs, char **bufs, int *buf_sizes);

    void registerCkRegisterMainModuleCallback(void (*cb)());
    void registerMainchareCtorExtCallback(void (*cb)(int, void*, int, int, char **));
    void registerReadOnlyRecvExtCallback(void (*cb)(int, char*));
    void registerChareMsgRecvExtCallback(void (*cb)(int, void*, int, int, char*, int));
    void registerGroupMsgRecvExtCallback(void (*cb)(int, int, int, char *, int));
    void registerArrayMsgRecvExtCallback(void (*cb)(int, int, int *, int, int, char *, int));
    void registerArrayElemLeaveExtCallback(int (*cb)(int, int, int *, char**, int));
    void registerArrayElemJoinExtCallback(void (*cb)(int, int, int *, int, char*, int));
    void registerArrayResumeFromSyncExtCallback(void (*cb)(int, int, int *));
    void registerCreateReductionTargetMsgExtCallback(void (*cb)(void*, int, int, int, char**, int*));
    void registerPyReductionExtCallback(int (*cb)(char**, int*, int, char**));
    void registerArrayMapProcNumExtCallback(int (*cb)(int, int, const int *));

    void CkExtContributeToChare(struct ContributeInfo* contribute_params, int onPE, void* objPtr);
    void CkExtContributeToGroup(struct ContributeInfo* contribute_params, int gid, int pe);
    void CkExtContributeToArray(struct ContributeInfo* contribute_params, int aid, int* idx, int ndims);

    // callbacks to python
    extern "Python" void registerMainModule(void);
    extern "Python" void recvReadOnly_py2(int, char*);
    extern "Python" void recvReadOnly_py3(int, char*);
    extern "Python" void buildMainchare(int, void*, int, int, char **);
    extern "Python" void recvChareMsg_py2(int, void*, int, int, char*, int);
    extern "Python" void recvChareMsg_py3(int, void*, int, int, char*, int);
    extern "Python" void recvGroupMsg_py2(int, int, int, char *, int);
    extern "Python" void recvGroupMsg_py3(int, int, int, char *, int);
    extern "Python" void recvArrayMsg_py2(int, int, int *, int, int, char *, int);
    extern "Python" void recvArrayMsg_py3(int, int, int *, int, int, char *, int);
    extern "Python" int  arrayElemLeave(int, int, int *, char**, int);
    extern "Python" void arrayElemJoin_py2(int, int, int *, int, char*, int);
    extern "Python" void arrayElemJoin_py3(int, int, int *, int, char*, int);
    extern "Python" void resumeFromSync(int, int, int *);
    extern "Python" void createReductionTargetMsg_py2(void*, int, int, int, char**, int*);
    extern "Python" void createReductionTargetMsg_py3(void*, int, int, int, char**, int*);
    extern "Python" int pyReduction_py2(char**, int*, int, char**);
    extern "Python" int pyReduction_py3(char**, int*, int, char**);
    extern "Python" int arrayMapProcNum(int, int, const int*);

""")

if __name__ == "__main__":
    ffibuilder.compile()
