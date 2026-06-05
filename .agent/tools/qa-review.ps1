param()

Write-Host "[HOOK: QA-REVIEW] Ativando Validacao Adversarial..." -ForegroundColor Cyan

# Verifica obrigatoriedade de Logging Duplo
$logsFolder = "01_Logs"
if (!(Test-Path $logsFolder)) {
    Write-Host "[ERRO] QA FAILED: O diretório de Logging Duplo (01_Logs) nao existe. O desenvolvedor violou a regra." -ForegroundColor Red
    exit 1
}

Write-Host "[SUCESSO] Padroes fisicos estao ok. QA isolado devera validar premissas e calculos agora." -ForegroundColor Green
