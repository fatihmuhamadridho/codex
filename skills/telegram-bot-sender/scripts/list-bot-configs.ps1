Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

. "$PSScriptRoot\TelegramBotStore.ps1"

$store = Get-TelegramBotStore
$records = @($store.bots | ForEach-Object {
    ConvertTo-TelegramBotRecord -Bot $_
})

[pscustomobject][ordered]@{
    count = $records.Count
    bots = $records
    store_path = Get-TelegramBotStorePath
} | ConvertTo-Json -Depth 10
