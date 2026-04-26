# Roda OPTIC dentro do container azathoth/pddl em cada problema do cenario.
# Cada problema usa um container --rm separado: simples, sem estado.

param([switch]$Optimize)

$scriptDir = (Resolve-Path $PSScriptRoot).Path
$opticArgs = if ($Optimize) { @() } else { @("-N") }
$exitCode = 0

foreach ($p in @("problem1","problem2","problem3","problem4")) {
    Write-Host ""
    Write-Host "=== $p ==="
    docker run --rm `
        --entrypoint /root/planners/optic-clp `
        -v "${scriptDir}:/x" `
        azathoth/pddl `
        $opticArgs `
        /x/domain.pddl /x/$p.pddl

    if ($LASTEXITCODE -ne 0) {
        $exitCode = $LASTEXITCODE
    }
}

exit $exitCode
