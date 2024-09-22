$cfiles = [System.Collections.ArrayList]::new()
$unrecognized = [System.Collections.ArrayList]::new()


foreach ($arg in $args) {
    if ($arg -clike "*.c") {
        [void]$cfiles.Add($arg.ToString().Replace(".\", ""))
    }
    else {
        [void]$unrecognized.Add($arg)
    }
}

if ($unrecognized.Count -ne 0) {
    Write-Error "Incompatible files passed for compilation: ${unrecognized}"
    Exit 1
}

$cflags = @(
    "/arch:AVX512",
    "/diagnostics:caret",
    "/DNDEBUG",
    "/D_NDEBUG",
    "/experimental:c11atomics", # need this for <stdatomic.h>
    "/F0x10485100",
    "/favor:INTEL64",
    "/fp:strict",
    "/fpcvt:IA",
    "/GL",
    "/Gw",
    "/MP",
    "/MT", # statically link the multithreaded version of libs
    "/O2",
    "/Ob3",
    "/Oi",
    "/Ot",
    "/Qpar",
    "/std:clatest",
    "/TC",
    "/Wall",
    "/wd4710",      # not inlined
    "/wd4711",      # selected for inlining
    "/wd4820",      # struct padding
    "/Zc:preprocessor",
    "/link /DEBUG:NONE"
)

Write-Host "cl.exe ${cfiles} ${cflags}" -ForegroundColor Cyan
cl.exe $cfiles $cflags

# If cl.exe returned 0, (i.e if the compilation succeeded,)

if ($? -eq $True){
    foreach($file in $cfiles){
        Remove-Item $file.Replace(".c", ".obj") -Force
    }
}
