Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$Script:TelegramBotStorePath = "C:\Users\fatih\.codex\.sandbox-secrets\telegram-bots.json"

function Get-TelegramBotStorePath {
    return $Script:TelegramBotStorePath
}

function Ensure-TelegramBotStoreDirectory {
    $directory = Split-Path -Path $Script:TelegramBotStorePath -Parent
    if (-not (Test-Path -LiteralPath $directory)) {
        New-Item -ItemType Directory -Path $directory -Force | Out-Null
    }
}

function Get-TelegramBotStore {
    Ensure-TelegramBotStoreDirectory

    if (-not (Test-Path -LiteralPath $Script:TelegramBotStorePath)) {
        return [ordered]@{
            bots = @()
        }
    }

    $raw = Get-Content -LiteralPath $Script:TelegramBotStorePath -Raw
    if ([string]::IsNullOrWhiteSpace($raw)) {
        return [ordered]@{
            bots = @()
        }
    }

    try {
        $parsed = $raw | ConvertFrom-Json
    }
    catch {
        throw "Telegram bot store is invalid JSON: $Script:TelegramBotStorePath"
    }

    if ($null -eq $parsed.bots) {
        $parsed | Add-Member -NotePropertyName bots -NotePropertyValue @()
    }

    return $parsed
}

function Save-TelegramBotStore {
    param(
        [Parameter(Mandatory = $true)]
        [object]$Store
    )

    Ensure-TelegramBotStoreDirectory
    $json = $Store | ConvertTo-Json -Depth 10
    Set-Content -LiteralPath $Script:TelegramBotStorePath -Value $json
}

function Normalize-TelegramBotAlias {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Alias
    )

    $normalized = $Alias.Trim().ToLowerInvariant()
    $normalized = [regex]::Replace($normalized, "\s+", " ")
    return $normalized
}

function Get-TelegramBotAliasVariants {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Alias
    )

    $normalized = Normalize-TelegramBotAlias -Alias $Alias
    $variants = New-Object System.Collections.Generic.HashSet[string]
    $null = $variants.Add($normalized)

    if ($normalized -match '^bot\s+(\d+)$') {
        $number = [int]$Matches[1]
        $null = $variants.Add("bot $number")

        $ordinals = @{
            1 = "pertama"
            2 = "kedua"
            3 = "ketiga"
            4 = "keempat"
            5 = "kelima"
            6 = "keenam"
            7 = "ketujuh"
            8 = "kedelapan"
            9 = "kesembilan"
            10 = "kesepuluh"
        }

        if ($ordinals.ContainsKey($number)) {
            $null = $variants.Add("bot $($ordinals[$number])")
        }
    }

    $values = foreach ($value in $variants) {
        $value
    }

    return @($values | Sort-Object)
}

function Mask-TelegramBotToken {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Token
    )

    if ($Token.Length -le 10) {
        return ("*" * $Token.Length)
    }

    $prefix = $Token.Substring(0, 6)
    $suffix = $Token.Substring($Token.Length - 4, 4)
    return "$prefix...$suffix"
}

function ConvertTo-TelegramBotRecord {
    param(
        [Parameter(Mandatory = $true)]
        [object]$Bot
    )

    return [ordered]@{
        alias = $Bot.alias
        display_name = $Bot.display_name
        default_chat_id = $Bot.default_chat_id
        masked_token = Mask-TelegramBotToken -Token $Bot.token
        alias_variants = @($Bot.alias_variants)
        created_at = $Bot.created_at
        updated_at = $Bot.updated_at
    }
}

function Get-TelegramBotByAlias {
    param(
        [Parameter(Mandatory = $true)]
        [object]$Store,

        [Parameter(Mandatory = $true)]
        [string]$Alias
    )

    $requested = Normalize-TelegramBotAlias -Alias $Alias
    $matches = @()

    foreach ($bot in @($Store.bots)) {
        $variants = @($bot.alias_variants)
        if ($variants.Count -eq 0) {
            $variants = Get-TelegramBotAliasVariants -Alias $bot.alias
        }

        $normalizedVariants = @($variants | ForEach-Object {
            Normalize-TelegramBotAlias -Alias $_
        })

        if ($normalizedVariants -contains $requested) {
            $matches += $bot
        }
    }

    if ($matches.Count -gt 1) {
        throw "Alias '$Alias' matched multiple Telegram bot configs."
    }

    if ($matches.Count -eq 0) {
        return $null
    }

    return $matches[0]
}

function Set-TelegramBotConfig {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Alias,

        [Parameter(Mandatory = $true)]
        [string]$Token,

        [Parameter(Mandatory = $true)]
        [string]$DefaultChatId
    )

    $store = Get-TelegramBotStore
    $normalizedAlias = Normalize-TelegramBotAlias -Alias $Alias
    $variants = Get-TelegramBotAliasVariants -Alias $Alias
    $timestamp = (Get-Date).ToString("o")
    $existing = Get-TelegramBotByAlias -Store $store -Alias $Alias

    if ($null -eq $existing) {
        $record = [pscustomobject][ordered]@{
            alias = $normalizedAlias
            display_name = $Alias.Trim()
            token = $Token.Trim()
            default_chat_id = $DefaultChatId.Trim()
            alias_variants = $variants
            created_at = $timestamp
            updated_at = $timestamp
        }
        $store.bots = @($store.bots) + $record
        $action = "created"
        $saved = $record
    }
    else {
        $existing.alias = $normalizedAlias
        $existing.display_name = $Alias.Trim()
        $existing.token = $Token.Trim()
        $existing.default_chat_id = $DefaultChatId.Trim()
        $existing.alias_variants = $variants
        $existing.updated_at = $timestamp
        if ([string]::IsNullOrWhiteSpace([string]$existing.created_at)) {
            $existing.created_at = $timestamp
        }
        $action = "updated"
        $saved = $existing
    }

    Save-TelegramBotStore -Store $store

    return [pscustomobject][ordered]@{
        action = $action
        bot = ConvertTo-TelegramBotRecord -Bot $saved
        store_path = $Script:TelegramBotStorePath
    }
}
