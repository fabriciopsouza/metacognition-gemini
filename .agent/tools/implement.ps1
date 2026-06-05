param()

Write-Host "[HOOK: IMPLEMENT] Ativando Skill Developer..." -ForegroundColor Cyan

$planFile = "implementation_plan.md"

if (!(Test-Path $planFile)) {
    Write-Host "[ERRO] Arquitetura bloqueada. Crie e aprove um implementation_plan.md primeiro rodando feature-plan.ps1." -ForegroundColor Red
    exit 1
}

# (Exemplo de bloqueio simples para validacao futura - na pratica o Agente checa aprovacao do usuario)
Write-Host "[SUCESSO] Plano localizado. Permissao concedida para o Agente efetuar modificacoes de codigo e criar walkthrough.md." -ForegroundColor Green
