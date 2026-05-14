param(
    [Parameter(Mandatory = $true)]
    [string]$Bot,

    [Parameter(Mandatory = $true)]
    [string]$Message,

    [switch]$DryRun
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

. "$PSScriptRoot\TelegramBotStore.ps1"

$store = Get-TelegramBotStore
$resolvedBot = Get-TelegramBotByAlias -Store $store -Alias $Bot

if ($null -eq $resolvedBot) {
    throw "Telegram bot alias '$Bot' was not found in $(Get-TelegramBotStorePath)."
}

$payload = [ordered]@{
    chat_id = [string]$resolvedBot.default_chat_id
    text = $Message
}

if ($DryRun) {
    [pscustomobject][ordered]@{
        ok = $true
        dry_run = $true
        bot = ConvertTo-TelegramBotRecord -Bot $resolvedBot
        request = $payload
    } | ConvertTo-Json -Depth 10
    exit 0
}

$uri = "https://api.telegram.org/bot$($resolvedBot.token)/sendMessage"

try {
    $response = Invoke-RestMethod -Method Post -Uri $uri -ContentType "application/json" -Body ($payload | ConvertTo-Json -Depth 5)
}
catch {
    if ($_.ErrorDetails.Message) {
        throw "Telegram API request failed: $($_.ErrorDetails.Message)"
    }

    throw
}

[pscustomobject][ordered]@{
    ok = [bool]$response.ok
    dry_run = $false
    bot = ConvertTo-TelegramBotRecord -Bot $resolvedBot
    request = $payload
    response = $response
} | ConvertTo-Json -Depth 20
