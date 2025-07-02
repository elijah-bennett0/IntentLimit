banned_functions = [
    # Dangerous string functions
    "strcpy", "strcpyA", "strcpyW", "wcscpy", "_tcscpy", "_mbscpy", "StrCpy", "StrCpyA", "StrCpyW",
    "lstrcpy", "lstrcpyA", "lstrcpyW", "_tccpy", "_mbccpy", "_ftcscpy",
    "strcat", "strcatA", "strcatW", "wcscat", "_tcscat", "_mbscat", "StrCat", "StrCatA", "StrCatW",
    "lstrcat", "lstrcatA", "lstrcatW", "StrCatBuff", "StrCatBuffA", "StrCatBuffW", "StrCatChainW",
    "_tccat", "_mbccat", "_ftcscat",

    # sprintf-style (format string) functions
    "sprintf", "sprintfA", "sprintfW", "swprintf", "_stprintf", "wsprintf", "wsprintfA", "wsprintfW",
    "vsprintf", "vswprintf", "_vstprintf", "wvsprintf", "wvsprintfA", "wvsprintfW",

    # strncpy-style functions
    "strncpy", "wcsncpy", "_tcsncpy", "_mbsncpy", "_mbsnbcpy", "StrCpyN", "StrCpyNA", "StrCpyNW",
    "StrNCpy", "strcpynA", "StrNCpyA", "StrNCpyW", "lstrcpyn", "lstrcpynA", "lstrcpynW",

    # strncat-style functions
    "strncat", "wcsncat", "_tcsncat", "_mbsncat", "_mbsnbcat", "StrCatN", "StrCatNA", "StrCatNW",
    "StrNCat", "StrNCatA", "StrNCatW", "lstrncat", "lstrcatn", "lstrcatnA", "lstrcatnW",

    # Memory functions
    "memcpy", "RtlCopyMemory", "CopyMemory", "wmemcpy",

    # Dangerous input
    "gets", "_getts", "_gettws", "scanf", "wscanf", "_tscanf", "sscanf", "swscanf", "_stscanf",
    "snscanf", "snwscanf", "_sntscanf",

    # Deprecated tokenizers
    "strtok", "_tcstok", "wcstok", "_mbstok",

    # Path functions
    "makepath", "_makepath", "_tmakepath", "_wmakepath", "_splitpath", "_tsplitpath", "_wsplitpath",

    # Dangerous pointer checks
    "IsBadWritePtr", "IsBadHugeWritePtr", "IsBadReadPtr", "IsBadHugeReadPtr", "IsBadCodePtr", "IsBadStringPtr",

    # Dangerous numeric conversions
    "_itoa", "_itow", "_i64toa", "_i64tow", "_ui64toa", "_ui64tot", "_ui64tow", "_ultoa", "_ultot", "_ultow",

    # OEM conversions
    "CharToOem", "CharToOemA", "CharToOemW", "OemToChar", "OemToCharA", "OemToCharW",
    "CharToOemBuffA", "CharToOemBuffW",

    # Stack allocation
    "alloca", "_alloca",

    # WinAPI-specific (may still apply)
    "ChangeWindowMessageFilter",

    # Other sprintf-style variants
    "wnsprintf", "wnsprintfA", "wnsprintfW", "_snwprintf", "_snprintf", "_sntprintf",
    "_vsnprintf", "vsnprintf", "_vsnwprintf", "_vsntprintf", "wvnsprintf", "wvnsprintfA", "wvnsprintfW",

    # Length functions
    "lstrlen",
]
