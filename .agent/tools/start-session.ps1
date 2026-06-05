param()

Write-Host "[HOOK: START-SESSION] Inicializando roteamento..." -ForegroundColor Cyan

# Verifica integridade dos artefatos base
$pmoSkillPath = ".agent/skills/pmo/SKILL.md"
$briefingPath = "docs/briefing.md"

if (!(Test-Path $pmoSkillPath)) {
    Write-Host "[ERRO] Arquivo de Roteamento $pmoSkillPath nao encontrado." -ForegroundColor Red
    exit 1
}

if (!(Test-Path $briefingPath)) {
    Write-Host "[ERRO] Arquivo de Contexto $briefingPath nao encontrado." -ForegroundColor Red
    exit 1
}

# Inicializa o checklist do PMO
$taskFile = "task.md"
if (!(Test-Path $taskFile)) {
    $taskContent = @"
# PMO Checklist - Estado Inicial
- [ ] Ler $briefingPath
- [ ] Executar .agent/tools/feature-plan.ps1
"@
    Set-Content -Path $taskFile -Value $taskContent
    Write-Host "[SUCESSO] Sessão iniciada. task.md criado na raiz." -ForegroundColor Green
} else {
    Write-Host "[INFO] task.md já existe. Sessão ativa." -ForegroundColor Yellow
}

# Verificacao mandatoria de cross-pollination (Option A+)
$ConfigPath = ".agent\cross-ai-repos.json"
$ProcessedJsonPath = "output\processed.json"

if (Test-Path $ConfigPath) {
    Write-Host "[SYNC] Configuração Cross-AI localizada." -ForegroundColor Green
    $Config = Get-Content $ConfigPath | ConvertFrom-Json
    $ClaudePath = $Config.claude.local_path
    $ClaudeReports = Join-Path -Path $ClaudePath -ChildPath $Config.claude.reports_subpath
    
    if (Test-Path $ClaudePath) {
        Write-Host "[SYNC] Repositório do Claude ($ClaudePath) acessível fisicamente." -ForegroundColor Green
        
        if (Test-Path $ClaudeReports) {
            Write-Host "`n[ALERTA CRÍTICO DE CROSS-POLLINATION]" -ForegroundColor Magenta
            Write-Host "[ALERTA] Varrendo a pasta $ClaudeReports em busca de inovações." -ForegroundColor Yellow
            Write-Host "[INFRA] Agente, você deve isolar IDs não presentes em processed.json, checar 'analyzed_reports' para loops, e processar via matriz de vereditos (ACEITO|REJEITADO|DEFERIDO)." -ForegroundColor Magenta
        } else {
            Write-Host "[AVISO EXPLÍCITO] A subpasta de relatórios do Claude ($ClaudeReports) não existe. Nenhuma nova integração pendente." -ForegroundColor Yellow
        }
    } else {
        Write-Host "[AVISO EXPLÍCITO] O Path do repositório do Claude definido no config não foi encontrado na máquina física. O Claude não poderá enviar relatórios automaticamente." -ForegroundColor Red
    }
} else {
    Write-Host "[AVISO EXPLÍCITO] Configuração cross-ai-repos.json não encontrada. Modo isolado puro operando." -ForegroundColor Yellow
}
