# 检查三个 apkg 的 media 索引，看音频/图片文件的实际差异
$ErrorActionPreference = 'Stop'

$updated = [System.IO.File]::ReadAllText((Resolve-Path 'updated\media'), [System.Text.Encoding]::UTF8)

# upstream/media 是 zstd 压缩，需要用 zstd 解压。先检查系统是否有 zstd
$zstdCmd = Get-Command zstd -ErrorAction SilentlyContinue
if ($zstdCmd) {
    Write-Host "zstd found at: $($zstdCmd.Source)"
    & zstd -d -c upstream\media > upstream_media.json 2>$null
    $upstream = [System.IO.File]::ReadAllText((Resolve-Path 'upstream_media.json'), [System.Text.Encoding]::UTF8)
} else {
    Write-Host "zstd NOT installed; skipping upstream decode"
    $upstream = $null
}

Write-Host "===== 检查 updated/media ====="
Write-Host "length: $($updated.Length)"
foreach ($kw in @('どんどん','おじいさん','ojiisan','dondon','DONDON','Ojiisan')) {
    $idx = $updated.IndexOf($kw)
    Write-Host ("[{0}] index={1}" -f $kw, $idx)
    if ($idx -ge 0) {
        $s = [Math]::Max(0, $idx-60)
        $len = [Math]::Min(200, $updated.Length - $s)
        Write-Host ("  context: " + $updated.Substring($s, $len))
    }
}

if ($upstream) {
    Write-Host ""
    Write-Host "===== 检查 upstream/media ====="
    Write-Host "length: $($upstream.Length)"
    foreach ($kw in @('どんどん','おじいさん','ojiisan','dondon','DONDON','Ojiisan')) {
        $idx = $upstream.IndexOf($kw)
        Write-Host ("[{0}] index={1}" -f $kw, $idx)
        if ($idx -ge 0) {
            $s = [Math]::Max(0, $idx-60)
            $len = [Math]::Min(200, $upstream.Length - $s)
            Write-Host ("  context: " + $upstream.Substring($s, $len))
        }
    }
}
