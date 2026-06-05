param()

Write-Host "[HOOK: FEATURE-PLAN] Ativando Skill Architect..." -ForegroundColor Cyan

$planFile = "implementation_plan.md"

if (Test-Path $planFile) {
    Write-Host "[INFO] Plano de implementacao já existe. Use implement.ps1 para aprovar." -ForegroundColor Yellow
    exit 0
}

$planContent = @"
# Goal Description
[Breve descricao]

## Proposed Changes
[Lista de modificacoes separadas por arquivos]

## Verification Plan
[Testes a executar]
"@
Set-Content -Path $planFile -Value $planContent
Write-Host "[SUCESSO] Artefato implementation_plan.md criado na raiz. Edite-o e aguarde aprovação antes de executar o codigo." -ForegroundColor Green
