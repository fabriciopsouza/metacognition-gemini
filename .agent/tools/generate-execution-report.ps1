<#
.SYNOPSIS
Hook Físico: Generate Execution Report

.DESCRIPTION
Este script coleta as saídas validadas de uma sessão do Metacognition Framework e gera um Execution Report físico na pasta de domínio correspondente, pronto para auditoria humana ou arquivamento executivo.

.PARAMETER Domain
O domínio da aplicação (ex: SAP, BI, Engineering). Padrão é 'General'.

.PARAMETER TaskName
O nome humanamente legível da tarefa executada.
#>

param (
    [string]$Domain = "General",
    [string]$TaskName = "Unnamed_Task"
)

$Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$SafeTaskName = $TaskName -replace "[^a-zA-Z0-9_-]", "_"
$ReportsDir = "execution-reports\$Domain"
$FileName = "${Timestamp}_${SafeTaskName}.md"
$FilePath = Join-Path -Path $ReportsDir -ChildPath $FileName

# Garante que o diretório de domínio exista
if (!(Test-Path -Path $ReportsDir)) {
    New-Item -ItemType Directory -Path $ReportsDir -Force | Out-Null
    Write-Host "[INFRA] Pasta de domínio criada: $ReportsDir" -ForegroundColor Cyan
}

# Inicializa o arquivo baseado no template (Simulação de cópia do buffer/template)
$TemplatePath = "execution-reports\00-template.md"
if (Test-Path -Path $TemplatePath) {
    Copy-Item -Path $TemplatePath -Destination $FilePath -Force
    Write-Host "[GERAÇÃO] Execution Report inicializado a partir do template." -ForegroundColor Green
} else {
    Write-Host "[ERRO] Template 00-template.md não encontrado. Criando arquivo em branco." -ForegroundColor Red
    New-Item -ItemType File -Path $FilePath -Force | Out-Null
}

Write-Host "========================================================"
Write-Host "✅ EXECUTION REPORT GERADO"
Write-Host "========================================================"
Write-Host "Arquivo salvo em: $FilePath" -ForegroundColor Yellow
Write-Host "Agente: Por favor, preencha o documento físico gerado com os achados finais da sessão e aguarde revisão humana."
