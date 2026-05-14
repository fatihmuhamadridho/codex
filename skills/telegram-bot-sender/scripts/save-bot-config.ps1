param(
    [Parameter(Mandatory = $true)]
    [string]$Alias,

    [Parameter(Mandatory = $true)]
    [string]$Token,

    [Parameter(Mandatory = $true)]
    [string]$DefaultChatId
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

. "$PSScriptRoot\TelegramBotStore.ps1"

$result = Set-TelegramBotConfig -Alias $Alias -Token $Token -DefaultChatId $DefaultChatId
$result | ConvertTo-Json -Depth 10
