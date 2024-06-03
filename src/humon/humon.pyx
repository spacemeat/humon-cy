
from libc.stdlib cimport malloc, free
from libc.string cimport strncpy

cimport chumon as c
from enum import Enum
from pathlib import Path

class Encoding(Enum):
    UTF8 = c.huEncoding.HU_ENCODING_UTF8
    UTF16_BE = c.huEncoding.HU_ENCODING_UTF16_BE
    UTF16_LE = c.huEncoding.HU_ENCODING_UTF16_LE
    UTF32_BE = c.huEncoding.HU_ENCODING_UTF32_BE
    UTF32_LE = c.huEncoding.HU_ENCODING_UTF32_LE
    UNKNOWN = c.huEncoding.HU_ENCODING_UNKNOWN

class NodeKind(Enum):
    NULLNODE = c.huNodeKind.HU_NODEKIND_NULL
    LIST = c.huNodeKind.HU_NODEKIND_LIST
    DICT = c.huNodeKind.HU_NODEKIND_DICT
    VALUE = c.huNodeKind.HU_NODEKIND_VALUE

class WhitespaceFormat(Enum):
    CLONED = c.huWhitespaceFormat.HU_WHITESPACEFORMAT_CLONED
    MINIMAL = c.huWhitespaceFormat.HU_WHITESPACEFORMAT_MINIMAL
    PRETTY = c.huWhitespaceFormat.HU_WHITESPACEFORMAT_PRETTY

class ErrorCode(Enum):
    NOERROR = c.huErrorCode.HU_ERROR_NOERROR                   
    BADENCODING = c.huErrorCode.HU_ERROR_BADENCODING               
    UNFINISHEDQUOTE = c.huErrorCode.HU_ERROR_UNFINISHEDQUOTE           
    UNFINISHEDCSTYLECOMMENT = c.huErrorCode.HU_ERROR_UNFINISHEDCSTYLECOMMENT   
    UNEXPECTEDEOF = c.huErrorCode.HU_ERROR_UNEXPECTEDEOF             
    TOOMANYROOTS = c.huErrorCode.HU_ERROR_TOOMANYROOTS              
    SYNTAXERROR = c.huErrorCode.HU_ERROR_SYNTAXERROR               
    NOTFOUND = c.huErrorCode.HU_ERROR_NOTFOUND                  
    ILLEGAL = c.huErrorCode.HU_ERROR_ILLEGAL                   
    BADPARAMETER = c.huErrorCode.HU_ERROR_BADPARAMETER              
    BADFILE = c.huErrorCode.HU_ERROR_BADFILE                   
    OUTOFMEMORY = c.huErrorCode.HU_ERROR_OUTOFMEMORY               
    TROVEHASERRORS = c.huErrorCode.HU_ERROR_TROVEHASERRORS             

class ErrorResponse(Enum):
    MUM = c.huErrorResponse.HU_ERRORRESPONSE_MUM               
    STDOUT = c.huErrorResponse.HU_ERRORRESPONSE_STDOUT            
    STDERR = c.huErrorResponse.HU_ERRORRESPONSE_STDERR            
    STDOUTANSICOLOR = c.huErrorResponse.HU_ERRORRESPONSE_STDOUTANSICOLOR   
    STDERRANSICOLOR = c.huErrorResponse.HU_ERRORRESPONSE_STDERRANSICOLOR   
    NUMRESPONSES = c.huErrorResponse.HU_ERRORRESPONSE_NUMRESPONSES       

class ColorCode(Enum):
    TOKENSTREAMBEGIN = c.huColorCode.HU_COLORCODE_TOKENSTREAMBEGIN          
    TOKENSTREAMEND = c.huColorCode.HU_COLORCODE_TOKENSTREAMEND            
    TOKENEND = c.huColorCode.HU_COLORCODE_TOKENEND                  
    PUNCLIST = c.huColorCode.HU_COLORCODE_PUNCLIST                  
    PUNCDICT = c.huColorCode.HU_COLORCODE_PUNCDICT                  
    PUNCKEYVALUESEP = c.huColorCode.HU_COLORCODE_PUNCKEYVALUESEP           
    PUNCMETATAG = c.huColorCode.HU_COLORCODE_PUNCMETATAG              
    PUNCMETATAGDICT = c.huColorCode.HU_COLORCODE_PUNCMETATAGDICT          
    PUNCMETATAGKEYVALUESEP = c.huColorCode.HU_COLORCODE_PUNCMETATAGKEYVALUESEP   
    KEY = c.huColorCode.HU_COLORCODE_KEY                       
    VALUE = c.huColorCode.HU_COLORCODE_VALUE                     
    COMMENT = c.huColorCode.HU_COLORCODE_COMMENT                   
    METATAGKEY = c.huColorCode.HU_COLORCODE_METATAGKEY                   
    METATAGVALUE = c.huColorCode.HU_COLORCODE_METATAGVALUE                 
    WHITESPACE = c.huColorCode.HU_COLORCODE_WHITESPACE                
    NUMCOLORS = c.huColorCode.HU_COLORCODE_NUMCOLORS                  

class VectorKind(Enum):
    COUNTING = c.huVectorKind.HU_VECTORKIND_COUNTING         
    PREALLOCATED = c.huVectorKind.HU_VECTORKIND_PREALLOCATED     
    GROWABLE = c.huVectorKind.HU_VECTORKIND_GROWABLE          

class BufferManagement(Enum):
    COPYANDOWN = c.huBufferManagement.HU_BUFFERMANAGEMENT_COPYANDOWN 
    MOVEANDOWN = c.huBufferManagement.HU_BUFFERMANAGEMENT_MOVEANDOWN 
    MOVE = c.huBufferManagement.HU_BUFFERMANAGEMENT_MOVE        

class HumonError(Exception):
    pass

class SerializeError(HumonError):
    pass

class DeserializeError(HumonError):
    pass

cdef str to_pstr_l(const char * cinp, c.huSize_t length):
    return cinp[:length].decode('UTF-8', 'strict')

cdef str to_pstr_l_free(char * cinp, c.huSize_t length):
    try:
        return cinp[:length].decode('UTF-8', 'strict')
    finally:
        free(cinp)

class Error:
    def __init__(self, error_code: ErrorCode, line: int, col: int):
        self.error_code = error_code
        self.line = line
        self.col = col

    def __repr__(self):
        return f'line {self.line}, column {self.col}: {self.error_code.name}'

cdef Trove _make_trove(c.huErrorCode res, c.huTrove * c_trove):
    if res not in [c.HU_ERROR_NOERROR, c.HU_ERROR_TROVEHASERRORS]:
        raise DeserializeError(f'Unable to make trove: {ErrorCode(res).name}')

    cdef const c.huError * c_error
    if res == c.HU_ERROR_TROVEHASERRORS:
        num_errors = c.huGetNumErrors(c_trove)
        errors = []
        for i in range(num_errors):
            c_error = c.huGetError(c_trove, i)
            errors.append(Error(ErrorCode(c_error.errorCode), c_error.line, c_error.col))
        raise DeserializeError(f'Trove has syntax errors:\n{errors}')
    t = Trove()
    t._c_trove = c_trove;
    return t

def from_string(code: str, tab_size: int = 4) -> Trove:
    if not isinstance(code, str):
        raise TypeError(code)
    if not isinstance(tab_size, int):
        raise TypeError(tab_size)
    cdef const char * ccode
    bcode = code.encode('utf-8')
    ccode, len_ccode = bcode, len(bcode)
    cdef c.huDeserializeOptions opts
    c.huInitDeserializeOptions(& opts, c.HU_ENCODING_UTF8, False, tab_size, NULL,
                                  c.HU_BUFFERMANAGEMENT_COPYANDOWN)
    cdef c.huTrove * c_trove
    cdef c.huErrorCode res
    res = c.huDeserializeTroveN(& c_trove, ccode, len_ccode, & opts, c.HU_ERRORRESPONSE_MUM)
    return _make_trove(res, c_trove)

def from_file(path: str | Path, encoding: Encoding = Encoding.UNKNOWN, tab_size: int = 4) -> Trove:
    if not isinstance(path, (str, Path)):
        raise TypeError(path)
    if not isinstance(encoding, Encoding):
        raise TypeError(encoding)
    if not isinstance(tab_size, int):
        raise TypeError(tab_size)
    cdef const char * cpath
    bpath = str(path).encode('utf-8')
    cpath, len_cpath = bpath, len(bpath)
    cdef c.huDeserializeOptions opts
    c.huInitDeserializeOptions(& opts, encoding.value, False, tab_size, NULL,
                                  c.HU_BUFFERMANAGEMENT_COPYANDOWN)
    cdef c.huTrove * c_trove
    cdef c.huErrorCode res
    mpath = <char *> malloc((len_cpath + 1) * sizeof(char))
    try:
        strncpy(mpath, cpath, len_cpath)
        mpath[len_cpath] = 0
        res = c.huDeserializeTroveFromFile(& c_trove, mpath, & opts, c.HU_ERRORRESPONSE_MUM)
        return _make_trove(res, c_trove)
    finally:
        free(mpath)

ctypedef c.huStringView[<c.huSize_t> c.huColorCode.HU_COLORCODE_NUMCOLORS] c_color_table_t

cdef class Trove:
    cdef c.huTrove * _c_trove

    def __cinit__(self):
        self._c_trove = NULL

    def __dealloc__(self):
        c.huDestroyTrove(self._c_trove)

    def _arrange_color_table(self, color_table: dict | list | None) -> list[bytes]:
        arr = []
        if isinstance(color_table, dict):
            arr.append(color_table.get(ColorCode.TOKENSTREAMBEGIN, '').encode('utf-8')) 
            arr.append(color_table.get(ColorCode.TOKENSTREAMEND, '').encode('utf-8')) 
            arr.append(color_table.get(ColorCode.TOKENEND, '').encode('utf-8')) 
            arr.append(color_table.get(ColorCode.PUNCLIST, '').encode('utf-8')) 
            arr.append(color_table.get(ColorCode.PUNCDICT, '').encode('utf-8')) 
            arr.append(color_table.get(ColorCode.PUNCKEYVALUESEP, '').encode('utf-8')) 
            arr.append(color_table.get(ColorCode.PUNCMETATAG, '').encode('utf-8')) 
            arr.append(color_table.get(ColorCode.PUNCMETATAGDICT, '').encode('utf-8')) 
            arr.append(color_table.get(ColorCode.PUNCMETATAGKEYVALUESEP, '').encode('utf-8')) 
            arr.append(color_table.get(ColorCode.KEY, '').encode('utf-8')) 
            arr.append(color_table.get(ColorCode.VALUE, '').encode('utf-8')) 
            arr.append(color_table.get(ColorCode.COMMENT, '').encode('utf-8')) 
            arr.append(color_table.get(ColorCode.METATAGKEY, '').encode('utf-8')) 
            arr.append(color_table.get(ColorCode.METATAGVALUE, '').encode('utf-8')) 
            arr.append(color_table.get(ColorCode.WHITESPACE, '').encode('utf-8')) 
        elif isinstance(color_table, list):
            assert len(color_table) == ColorCode.NUMCOLORS.value
            arr = [ce.encode('utf-8') for ce in color_table if isinstance(ce, str)]
        else:
            arr = [b''] * ColorCode.NUMCOLORS.value
        return arr

    cdef void _make_serialize_options(self, c.huSerializeOptions * opts,
                                      whitespace_format: WhitespaceFormat,
                                      indent_size: int, indent_with_tabs: bool,
                                      use_colors: bool, make_ansi_colors: bool, 
                                      b_color_table: list[bytes],
                                      c.huStringView * c_color_table,
                                      print_comments: bool, const char * cnewline,
                                      len_cnewline: int,
                                      print_bom: bool):
        cdef c.huStringView * pcolor_table = NULL
        if use_colors:
            pcolor_table = & c_color_table[0]
            if make_ansi_colors:
                c.huFillAnsiColorTable(c_color_table)
            else:
                for i in range(<int> c.huColorCode.HU_COLORCODE_NUMCOLORS):
                    c_color_table[i].ptr, c_color_table[i].size = (
                            b_color_table[i], len(b_color_table[i]))
        wsf = whitespace_format.value
        c.huInitSerializeOptionsN(opts, wsf, indent_size, indent_with_tabs,
                                  use_colors, pcolor_table,
                                  print_comments, cnewline, len_cnewline, c.HU_ENCODING_UTF8, 
                                  print_bom)

    def to_string(self, whitespace_format: WhitespaceFormat = WhitespaceFormat.PRETTY,
                  indent_size: int = 4, indent_with_tabs: bool = False,
                  use_colors: bool = False, color_table: dict | list | None = None,
                  print_comments: bool = True, newline = "\n",
                  print_bom: bool = False) -> str:
        cdef c.huSerializeOptions opts
        cdef const char * cnewline
        bnewline = newline.encode('utf-8')
        cnewline, len_cnewline = bnewline, len(bnewline)
        b_color_table = self._arrange_color_table(color_table)
        cdef c.huStringView[<c.huSize_t> c.huColorCode.HU_COLORCODE_NUMCOLORS] c_color_table
        self._make_serialize_options(& opts, whitespace_format, indent_size, indent_with_tabs,
                                     use_colors, use_colors and color_table is None,
                                     b_color_table, c_color_table, print_comments, cnewline,
                                     len_cnewline, print_bom)
        cdef c.huErrorCode res
        cdef c.huSize_t size = 0
        cdef char * humon_string = NULL
        res = c.huSerializeTrove(self._c_trove, humon_string, & size, & opts)
        if res != c.huErrorCode.HU_ERROR_NOERROR:
            raise SerializeError(f'Error code: {ErrorCode(res).name}')
        humon_string = <char *> malloc((size + 1) * sizeof(char))
        try:
            if humon_string == NULL:
                raise MemoryError()
            res = c.huSerializeTrove(self._c_trove, humon_string, & size, & opts)
            if res != c.huErrorCode.HU_ERROR_NOERROR:
                raise SerializeError(f'Error code: {ErrorCode(res).name}')
        except Exception as e:
            free(humon_string)
            raise e
        return to_pstr_l_free(humon_string, size)

    def to_file(self, path: Path, whitespace_format: WhitespaceFormat = WhitespaceFormat.PRETTY,
                indent_size: int = 4, indent_with_tabs: bool = False,
                use_colors: bool = False, color_table: dict | list | None = None,
                print_comments: bool = True, newline = "\n",
                print_bom: bool = False) -> ErrorCode:
        cdef c.huSerializeOptions opts
        cdef const char * cnewline
        bnewline = newline.encode('utf-8')
        cnewline, len_cnewline = bnewline, len(bnewline)
        b_color_table = self._arrange_color_table(color_table)
        cdef c.huStringView[<c.huSize_t> c.huColorCode.HU_COLORCODE_NUMCOLORS] c_color_table
        self._make_serialize_options(& opts, whitespace_format, indent_size, indent_with_tabs,
                                     use_colors, use_colors and color_table is None,
                                     b_color_table, c_color_table, print_comments, cnewline,
                                     len_cnewline, print_bom)
        cdef c.huErrorCode res
        cdef const char * cpath
        bpath = str(path).encode('utf-8')
        cpath, len_cpath = bpath, len(bpath)
        mpath = <char *> malloc((len_cpath + 1) * sizeof(char))
        try:
            strncpy(mpath, cpath, len_cpath)
            mpath[len_cpath] = 0
            res = c.huSerializeTroveToFile(self._c_trove, mpath, NULL, & opts)
            if res != c.huErrorCode.HU_ERROR_NOERROR:
                raise SerializeError(f'Error code: {ErrorCode(res).name}')
        finally:
            free(mpath)
        return res

    @property
    def num_nodes(self) -> int:
        return c.huGetNumNodes(self._c_trove)

    @property
    def root(self) -> Node | None:
        return Node().c(c.huGetRootNode(self._c_trove))

    def get_node(self, idx: int | str) -> Node | None:
        cdef char * caddr = NULL
        if isinstance(idx, str):
            bidx = idx.encode('utf-8')
            caddr, len_caddr = bidx, len(bidx)
            return Node().c(c.huGetNodeByAddressN(self._c_trove, caddr, len_caddr))
        elif isinstance(idx, int):
            return Node().c(c.huGetNodeByIndex(self._c_trove, idx))
        else:
            raise TypeError(idx)

    @property
    def source_text(self) -> str | None:
        st = c.huGetTroveSourceText(self._c_trove)
        return to_pstr_l(st.ptr, st.size)

    @property
    def metatags(self) -> dict[str, str]:
        metatags = {}
        cdef int num_metatags = c.huGetNumTroveMetatags(self._c_trove)
        cdef const c.huMetatag * cmetatag
        cdef const c.huToken * tk
        cdef const c.huToken * tv
        cdef const c.huStringView * ak
        cdef const c.huStringView * av
        for i in range(num_metatags):
            cmetatag = c.huGetTroveMetatag(self._c_trove, i)
            tk, tv = cmetatag.key, cmetatag.value
            ak, av = c.huGetString(tk), c.huGetString(tv)
            pak = to_pstr_l(ak.ptr, ak.size)
            pav = to_pstr_l(av.ptr, av.size)
            metatags[pak] = pav
        return metatags


cdef class Node:
    cdef const c.huNode * _c_node

    def __cinit__(self):
        _c_node = NULL

    cdef Node c(self, const c.huNode * c_node):
        if c_node == NULL:
            return None
        self._c_node = c_node
        return self

    @property
    def isnull(self) -> bool:
        return self._c_node == NULL

    @property
    def kind(self) -> NodeKind:
        if self.isnull:
            return NodeKind.NULLNODE
        return NodeKind(c.huGetNodeKind(self._c_node))

    @property
    def parent(self) -> Node | None:
        if self.isnull:
            return None
        return Node().c(c.huGetParent(self._c_node))

    @property
    def num_children(self) -> Node | None:
        if self.isnull:
            return None
        return c.huGetNumChildren(self._c_node)

    @property
    def node_index(self) -> int:
        if self.isnull:
            return -1
        return c.huGetNodeIndex(self._c_node)

    @property
    def child_index(self) -> int:
        if self.isnull:
            return -1
        return c.huGetChildIndex(self._c_node)

    def __eq__(self, rhs: Node):
        cdef const c.huNode * pn = rhs._c_node
        return self._c_node == pn

    def __getitem__(self, idx: str | int | tuple[str, int]) -> Node | None:
        if self.isnull:
            return None
        cdef const char * ckey
        cdef const c.huNode * cnn
        if isinstance(idx, str):
            bidx = idx.encode('utf-8')
            ckey, len_ckey = bidx, len(bidx)
            return Node().c(c.huGetChildByKeyN(self._c_node, ckey, len_ckey))
        elif isinstance(idx, tuple):
            bkey = idx[0].encode('utf-8')
            ckey, len_ckey = bkey, len(bkey)
            cidx = idx[1]
            cnn = c.huGetFirstChildWithKeyN(self._c_node, ckey, len_ckey)
            for i in range(cidx):
                cnn = c.huGetNextSiblingWithKeyN(cnn, ckey, len_ckey)
            return Node().c(cnn)
        return Node().c(c.huGetChildByIndex(self._c_node, idx))

    def get_node(self, idx: int | str) -> Node | None:
        if self.isnull:
            return None
        cdef char * caddr = NULL
        if isinstance(idx, str):
            bidx = idx.encode('utf-8')
            caddr, len_caddr = bidx, len(bidx)
            return Node().c(c.huGetNodeByRelativeAddressN(self._c_node, caddr, len_caddr))
        elif isinstance(idx, int):
            return Node().c(c.huGetChildByIndex(self._c_node, idx))
        else:
            raise TypeError(idx)

    def get_sibling(self, key: str | None = None) -> Node | None:
        if self.isnull:
            return None
        if c.huGetParent(self._c_node) == NULL:
            return None
        if key is None:
            return Node().c(c.huGetNextSibling(self._c_node))
        cdef char * ckey = NULL
        if isinstance(key, str):
            bkey = key.encode('utf-8')
            ckey, len_ckey = bkey, len(bkey)
            return Node().c(c.huGetNextSiblingWithKeyN(self._c_node, ckey, len_ckey))
        else:
            raise TypeError(key)

    @property
    def address(self) -> str | None:
        if self.isnull:
            return None
        cdef c.huSize_t size = 0
        cdef char * addr = NULL
        c.huGetAddress(self._c_node, addr, & size)
        addr = <char *> malloc((size + 1) * sizeof(char))
        if addr == NULL:
            raise MemoryError()
        c.huGetAddress(self._c_node, addr, & size)
        return to_pstr_l_free(addr, size)

    @property
    def key(self) -> str | None:
        if self.isnull:
            return None
        cdef const c.huToken * kt = c.huGetKey(self._c_node)
        if kt == NULL:
            return None
        ks = c.huGetString(kt)
        return to_pstr_l(ks.ptr, ks.size)

    @property
    def value(self) -> str | None:
        if self.isnull:
            return None
        cdef const c.huToken * vt = c.huGetValue(self._c_node)
        if vt == NULL:
            return None
        vs = c.huGetString(vt)
        return to_pstr_l(vs.ptr, vs.size)

    @property
    def source_text(self) -> str | None:
        if self.isnull:
            return None
        st = c.huGetSourceText(self._c_node)
        return to_pstr_l(st.ptr, st.size)

    @property
    def metatags(self) -> dict[str, str] | None:
        if self.isnull:
            return None
        metatags = {}
        cdef int num_metatags = c.huGetNumMetatags(self._c_node)
        cdef const c.huMetatag * cmetatag
        cdef const c.huToken * tk
        cdef const c.huToken * tv
        cdef const c.huStringView * ak
        cdef const c.huStringView * av
        for i in range(num_metatags):
            cmetatag = c.huGetMetatag(self._c_node, i)
            tk, tv = cmetatag.key, cmetatag.value
            ak, av = c.huGetString(tk), c.huGetString(tv)
            pak = to_pstr_l(ak.ptr, ak.size)
            pav = to_pstr_l(av.ptr, av.size)
            metatags[pak] = pav
        return metatags
