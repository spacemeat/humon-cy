cdef extern from "humon/humon.h":

    ctypedef long huLine_t
    ctypedef long huCol_t
    ctypedef long huSize_t
    ctypedef bint bool

    cdef enum huEncoding_tag:
        HU_ENCODING_UTF8
        HU_ENCODING_UTF16_BE
        HU_ENCODING_UTF16_LE
        HU_ENCODING_UTF32_BE
        HU_ENCODING_UTF32_LE
        HU_ENCODING_UNKNOWN
    ctypedef huEncoding_tag huEncoding

    cdef enum huTokenKind_tag:
        HU_TOKENKIND_NULL
        HU_TOKENKIND_EOF
        HU_TOKENKIND_STARTLIST
        HU_TOKENKIND_ENDLIST
        HU_TOKENKIND_STARTDICT
        HU_TOKENKIND_ENDDICT
        HU_TOKENKIND_KEYVALUESEP
        HU_TOKENKIND_METATAG
        HU_TOKENKIND_WORD
        HU_TOKENKIND_COMMENT
    ctypedef huTokenKind_tag huTokenKind

    cdef enum huNodeKind_tag:
        HU_NODEKIND_NULL
        HU_NODEKIND_LIST
        HU_NODEKIND_DICT
        HU_NODEKIND_VALUE
    ctypedef huNodeKind_tag huNodeKind

    cdef enum huWhitespaceFormat_tag:
        HU_WHITESPACEFORMAT_CLONED
        HU_WHITESPACEFORMAT_MINIMAL
        HU_WHITESPACEFORMAT_PRETTY
    ctypedef huWhitespaceFormat_tag huWhitespaceFormat

    cdef enum huErrorCode_tag:
        HU_ERROR_NOERROR                   
        HU_ERROR_BADENCODING               
        HU_ERROR_UNFINISHEDQUOTE           
        HU_ERROR_UNFINISHEDCSTYLECOMMENT   
        HU_ERROR_UNEXPECTEDEOF             
        HU_ERROR_TOOMANYROOTS              
        HU_ERROR_SYNTAXERROR               
        HU_ERROR_NOTFOUND                  
        HU_ERROR_ILLEGAL                   
        HU_ERROR_BADPARAMETER              
        HU_ERROR_BADFILE                   
        HU_ERROR_OUTOFMEMORY               
        HU_ERROR_TROVEHASERRORS             
    ctypedef huErrorCode_tag huErrorCode

    cdef enum huErrorResponse_tag:
        HU_ERRORRESPONSE_MUM               
        HU_ERRORRESPONSE_STDOUT            
        HU_ERRORRESPONSE_STDERR            
        HU_ERRORRESPONSE_STDOUTANSICOLOR   
        HU_ERRORRESPONSE_STDERRANSICOLOR   
        HU_ERRORRESPONSE_NUMRESPONSES       
    ctypedef huErrorResponse_tag huErrorResponse

    cdef enum huColorCode_tag:
        HU_COLORCODE_TOKENSTREAMBEGIN          
        HU_COLORCODE_TOKENSTREAMEND            
        HU_COLORCODE_TOKENEND                  
        HU_COLORCODE_PUNCLIST                  
        HU_COLORCODE_PUNCDICT                  
        HU_COLORCODE_PUNCKEYVALUESEP           
        HU_COLORCODE_PUNCMETATAG              
        HU_COLORCODE_PUNCMETATAGDICT          
        HU_COLORCODE_PUNCMETATAGKEYVALUESEP   
        HU_COLORCODE_KEY                       
        HU_COLORCODE_VALUE                     
        HU_COLORCODE_COMMENT                   
        HU_COLORCODE_METATAGKEY                   
        HU_COLORCODE_METATAGVALUE                 
        HU_COLORCODE_WHITESPACE                
        HU_COLORCODE_NUMCOLORS                  
    ctypedef huColorCode_tag huColorCode

    cdef enum huVectorKind_tag:
        HU_VECTORKIND_COUNTING
        HU_VECTORKIND_PREALLOCATED
        HU_VECTORKIND_GROWABLE
    ctypedef huVectorKind_tag huVectorKind

    cdef enum huBufferManagement_tag:
        HU_BUFFERMANAGEMENT_COPYANDOWN
        HU_BUFFERMANAGEMENT_MOVEANDOWN
        HU_BUFFERMANAGEMENT_MOVE
    ctypedef huBufferManagement_tag huBufferManagement

    cdef struct huAllocator_tag:
        pass
    ctypedef huAllocator_tag huAllocator

    cdef struct huVector_tag:
        pass
    ctypedef huVector_tag huVector

    cdef struct huStringView_tag:
        const char * ptr
        huSize_t size
    ctypedef huStringView_tag huStringView

    cdef struct huToken_tag:
        pass
    ctypedef huToken_tag huToken

    cdef struct huMetatag_tag:
        const huToken * key
        const huToken * value
    ctypedef huMetatag_tag huMetatag

    cdef struct huComment_tag:
        pass
    ctypedef huComment_tag huComment

    cdef struct huError_tag:
        huErrorCode errorCode
        huLine_t line
        huCol_t col
    ctypedef huError_tag huError

    cdef struct huDeserializeOptions_tag:
        pass
    ctypedef huDeserializeOptions_tag huDeserializeOptions

    void huInitDeserializeOptions(huDeserializeOptions * params, huEncoding encoding,
        bool strictUnicode, huCol_t tabSize, const huAllocator * allocator,
        huBufferManagement bufferManagement);

    cdef struct huSerializeOptions_tag:
        pass
    ctypedef huSerializeOptions_tag huSerializeOptions

    void huInitSerializeOptionsN(huSerializeOptions * params, huWhitespaceFormat whitespaceFormat,
        huCol_t indentSize, bool indentWithTabs, bool usingColors, const huStringView * colorTable,
        bool printComments, const char * newline, huSize_t newlineSize, huEncoding encoding, bool printBom)

    cdef struct huNode_tag:
        pass
    ctypedef huNode_tag huNode

    cdef struct huTrove_tag:
        pass
    ctypedef huTrove_tag huTrove

    huTokenKind huGetTokenKind(const huToken * token)
    const huStringView * huGetString(const huToken * token)

    huNodeKind huGetNodeKind(const huNode * node)
    huSize_t huGetNodeIndex(const huNode * node)
    huSize_t huGetChildIndex(const huNode * node)
    const huNode * huGetParent(const huNode * node)
    huSize_t huGetNumChildren(const huNode * node)
    const huNode * huGetChildByIndex(const huNode * node, huSize_t childIndex)
    const huNode * huGetChildByKeyZ(const huNode * node, const char * key)
    const huNode * huGetChildByKeyN(const huNode * node, const char * key, huSize_t keyLen)
    const huNode * huGetFirstChild(const huNode * node)
    const huNode * huGetNextSibling(const huNode * node)
    const huNode * huGetFirstChildWithKeyZ(const huNode * node, const char * key)
    const huNode * huGetFirstChildWithKeyN(const huNode * node, const char * key, huSize_t keyLen)
    const huNode * huGetNextSiblingWithKeyZ(const huNode * node, const char * key)
    const huNode * huGetNextSiblingWithKeyN(const huNode * node, const char * key, huSize_t keyLen)
    const huNode * huGetNodeByRelativeAddressZ(const huNode * node, const char * address)
    const huNode * huGetNodeByRelativeAddressN(const huNode * node, const char * address, huSize_t addressLen)
    void huGetAddress(const huNode * node, char * address, huSize_t * addressLen)
    bool huHasKey(const huNode * node)
    const huToken * huGetKey(const huNode * node)
    const huToken * huGetValue(const huNode * node)
    huStringView huGetSourceText(const huNode * node)
    huSize_t huGetNumMetatags(const huNode * node)
    const huMetatag * huGetMetatag(const huNode * node, huSize_t annotationIdx)
    bool huHasMetatagWithKeyZ(const huNode * node, const char * key)
    bool huHasMetatagWithKeyN(const huNode * node, const char * key, huSize_t keyLen)
    const huToken * huGetMetatagWithKeyZ(const huNode * node, const char * key)
    const huToken * huGetMetatagWithKeyN(const huNode * node, const char * key, huSize_t keyLen)
    huSize_t huGetNumMetatagsWithValueZ(const huNode * node, const char * value)
    huSize_t huGetNumMetatagsWithValueN(const huNode * node, const char * value, huSize_t valueLen)
    const huToken * huGetMetatagWithValueZ(const huNode * node, const char * value, huSize_t * cursor)
    const huToken * huGetMetatagWithValueN(const huNode * node, const char * value, huSize_t valueLen, huSize_t * cursor)
    huSize_t huGetNumComments(const huNode * node)
    const huToken * huGetComment(const huNode * node, huSize_t commentIdx)
    bool huHasCommentsContainingZ(const huNode * node, const char * containedText)
    bool huHasCommentsContainingN(const huNode * node, const char * containedText, huSize_t containedTextLen)
    huSize_t huGetNumCommentsContainingZ(const huNode * node, const char * containedText)
    huSize_t huGetNumCommentsContainingN(const huNode * node, const char * containedText, huSize_t containedTextLen)
    const huToken * huGetCommentsContainingZ(const huNode * node, const char * containedText, huSize_t * cursor)
    const huToken * huGetCommentsContainingN(const huNode * node, const char * containedText, huSize_t containedTextLen, huSize_t * cursor)

    huErrorCode huDeserializeTroveZ(huTrove ** trove, const char * data, huDeserializeOptions * deserializeOptions, huErrorResponse errorResponse)
    huErrorCode huDeserializeTroveN(huTrove ** trove, const char * data, huSize_t dataLen, huDeserializeOptions * deserializeOptions, huErrorResponse errorResponse)
    huErrorCode huDeserializeTroveFromFile(huTrove ** trove, const char * path, huDeserializeOptions * deserializeOptions, huErrorResponse errorResponse)
    void huDestroyTrove(huTrove * trove)
    huSize_t huGetNumTokens(const huTrove * trove)
    const huToken * huGetToken(const huTrove * trove, huSize_t tokenIdx)
    huSize_t huGetNumNodes(const huTrove * trove)
    const huNode * huGetRootNode(const huTrove * trove)
    const huNode * huGetNodeByIndex(const huTrove * trove, huSize_t nodeIdx)
    const huNode * huGetNodeByAddressZ(const huTrove * trove, const char * address)
    const huNode * huGetNodeByAddressN(const huTrove * trove, const char * address, huSize_t addressLen)
    huSize_t huGetNumErrors(const huTrove * trove)
    const huError * huGetError(const huTrove * trove, huSize_t errorIdx)
    huSize_t huGetNumTroveMetatags(const huTrove * trove)
    const huMetatag * huGetTroveMetatag(const huTrove * trove, huSize_t annotationIdx)
    bool huTroveHasMetatagWithKeyZ(const huTrove * trove, const char * key)
    bool huTroveHasMetatagWithKeyN(const huTrove * trove, const char * key, huSize_t keyLen)
    const huToken * huGetTroveMetatagWithKeyZ(const huTrove * trove, const char * key)
    const huToken * huGetTroveMetatagWithKeyN(const huTrove * trove, const char * key, huSize_t keyLen)
    huSize_t huGetNumTroveMetatagsWithValueZ(const huTrove * trove, const char * value)
    huSize_t huGetNumTroveMetatagsWithValueN(const huTrove * trove, const char * value, huSize_t valueLen)
    const huToken * huGetTroveMetatagWithValueZ(const huTrove * trove, const char * value, huSize_t * cursor)
    const huToken * huGetTroveMetatagWithValueN(const huTrove * trove, const char * value, huSize_t valueLen, huSize_t * cursor)
    huSize_t huGetNumTroveComments(const huTrove * trove)
    const huToken * huGetTroveComment(const huTrove * trove, huSize_t commentIdx)
    const huNode * huFindNodesWithMetatagKeyZ(const huTrove * trove, const char * key, huSize_t * cursor)
    const huNode * huFindNodesWithMetatagKeyN(const huTrove * trove, const char * key, huSize_t keyLen, huSize_t * cursor)
    const huNode * huFindNodesWithMetatagValueZ(const huTrove * trove, const char * value, huSize_t * cursor)
    const huNode * huFindNodesWithMetatagValueN(const huTrove * trove, const char * value, huSize_t valueLen, huSize_t * cursor)
    const huNode * huFindNodesWithMetatagKeyValueZZ(const huTrove * trove, const char * key, const char * value, huSize_t * cursor)
    const huNode * huFindNodesWithMetatagKeyValueNZ(const huTrove * trove, const char * key, huSize_t keyLen, const char * value, huSize_t * cursor)
    const huNode * huFindNodesWithMetatagKeyValueZN(const huTrove * trove, const char * key, const char * value, huSize_t valueLen, huSize_t * cursor)
    const huNode * huFindNodesWithMetatagKeyValueNN(const huTrove * trove, const char * key, huSize_t keyLen, const char * value, huSize_t valueLen, huSize_t * cursor)
    const huNode * huFindNodesByCommentContainingZ(const huTrove * trove, const char * containedText, huSize_t * cursor)
    const huNode * huFindNodesByCommentContainingN(const huTrove * trove, const char * containedText, huSize_t containedTextLen, huSize_t * cursor)
    huStringView huGetTroveSourceText(const huTrove * trove)
    huErrorCode huSerializeTrove(const huTrove * trove, char * dest, huSize_t * destLength, huSerializeOptions * serializeOptions)
    huErrorCode huSerializeTroveToFile(const huTrove * trove, const char * path, huSize_t * destLength, huSerializeOptions * serializeOptions)
    void huFillAnsiColorTable(huStringView table[])

