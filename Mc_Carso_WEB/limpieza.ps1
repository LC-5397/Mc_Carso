$paths = @(
    ".\.web",
    ".\.next",
    ".\.reflex",
    ".\__pycache__",
    ".\node_modules"
)

foreach ($path in $paths) {
    $fullPath = Join-Path -Path (Get-Location) -ChildPath $path
    if (Test-Path $fullPath) {
        try {
            Remove-Item -Path $fullPath -Recurse -Force -ErrorAction Stop
            Write-Host "Eliminado: $fullPath"
        } catch {
            Write-Host "No se pudo eliminar: $fullPath"
        }
    } else {
        Write-Host "No existe: $fullPath"
    }
}

Write-Host "Limpieza completada."
