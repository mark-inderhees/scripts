
# To install this script, run these commands:
# New-Item –Path $Profile –Type File –Force
# ". <path>\env.ps1" | Out-File $Profile

# Write-Output "Sourcing private aliases and functions from $($MyInvocation.MyCommand.Path)"

Set-Alias -Name rescan -Scope global -Value $PSCommandPath
Set-Alias -Name gh -Scope global -Value Get-Help
Set-Alias -Name p -Scope global -Value Pop-Location
Set-Alias -Name pl -Scope global -Value Push-Location

if ($PSVersionTable.PSVersion.Major -ge 6) {
    Set-PSReadlineKeyHandler -Chord Ctrl+Enter -Function PossibleCompletions
    Set-PSReadlineKeyHandler -Chord Tab -Function MenuComplete
    Set-PSReadlineKeyHandler -Chord Ctrl+Spacebar -Function Complete
}

function global:n { & "c:\windows\notepad.exe" $args }
function global:np { & "${env:ProgramFiles}\notepad++\notepad++.exe" $args }
function global:npp { & "${env:ProgramFiles)}\notepad++\notepad++.exe" $args }
function global:putty { & "d:\tools\putty.exe"}
function global:hclient { & "d:\tools\hclient.exe"}
function global:err { & "G:\os\src\utilities\err\amd64\err.exe" $args }

function global:ll($target) {
    if ($target)
    {
        $target = Resolve-Path $target
    }
    else
    {
        $target = Get-Location
    }

    Write-Host "`nDirectory: $target"
    $properties = (
        'Mode',
        @{ Label = 'LastWriteTime'; Alignment = 'Right'; Expression = {
            #$_.LastWriteTime.ToString('MM/dd/yyyy hh:mm tt')
            $_.LastWriteTime.ToString('MMM dd HH:mm')
            }},
        @{ Label = 'Length';        Alignment = 'Right'; Expression = {
            if     ($_ -isnot [System.IO.FileInfo]) { "" }
            elseif ($_.Length -gt 1tb) { "{0:n1}T" -f ($_.Length / 1tb) }
            elseif ($_.Length -gt 1gb) { "{0:n1}G" -f ($_.Length / 1gb) }
            elseif ($_.Length -gt 1mb) { "{0:n1}M" -f ($_.Length / 1mb) }
            elseif ($_.Length -gt 1kb) { "{0:n1}K" -f ($_.Length / 1kb) }
            else                       {    "{0}B" -f  $_.Length }
            }},
        @{ Label = 'Name';          Alignment = 'left'; Expression = {
            if ($_ -is [System.IO.FileInfo])
            {
                switch ($_.Extension)
                {
                    '.exe'      { $color = '92' } # green
                    default     { $color = '0'  } # terminal default color
                }
            }
            elseif ($_ -is [System.IO.DirectoryInfo])
            {
                $color = '36' # cyan
            }
            else
            {
                $color = '0' # terminal default color
            }

            $e = [char]27 # escape character to being VT escape sequence
            "$e[${color}m$($_.Name)$e[0m"
            }}
    )
    Get-ChildItem $target | Format-Table -Property $properties
}

function global:.. {Push-Location ../}
function global:... {Push-Location ../../}
function global:.... {Push-Location ../../../}
function global:..... {Push-Location ../../../../}
function global:dev {Push-Location $PSScriptRoot }
function global:desktop {Join-Path $env:OneDrive "Desktop" | Push-Location}

function global:Get-EnvironmentVariables { Get-ChildItem env:* | Sort-Object Name }
function global:Set-EnvironmentVariable($Variable, $Value) { Set-Item -path env:$Variable -value $Value }
function global:grep { $input | Out-String -Stream | Select-String $args }

function global:f($string, $filenameExtension = $null, [bool]$simple = $false)
{
    $matches = Get-ChildItem -Recurse -Include "*$filenameExtension" | Select-String $string
    foreach($match in $matches)
    {
        $line = ":$($match.Line)"
        if ($simple)
        {
            $line = ""
        }
        Write-Host "$($match.Filename):$($match.LineNumber)$line"
    }
}

function global:Write-Colors
{
    $colors = [System.Enum]::GetValues([System.ConsoleColor])
    foreach ($color in $colors)
    {
        Write-Host $color -ForegroundColor $color
    }
}

function global:Get-ParameterAlias($command)
{
    (Get-Command $command).parameters.values | Select-Object Name, Aliases
}

function global:Get-FriendlySize($bytes)
{
    $sizes='Bytes,KB,MB,GB,TB,PB,EB,ZB' -split ','
    for($i=0; ($bytes -ge 1kb) -and
        ($i -lt $sizes.Count); $i++) {$bytes/=1kb}
    $N=2; if($i -eq 0) {$N=0}
    "{0:N$($N)} {1}" -f $bytes, $sizes[$i]
}

function global:Get-GitBranchFastMark
{
    $old = ""
    $current = Convert-Path $pwd.Path

    if ($current.StartsWith("\\"))
    {
        return $null
    }

    while ($current -ne $old)
    {
        if (Test-Path "$current\.git")
        {
            $head = (Get-Content -Force "$current\.git\HEAD") -replace '^ref: refs\/heads\/',''
            return $head
        }

        $old = $current
        $current = (Resolve-Path "$current\..").Path
    }

    return $null
}

function global:Get-GitBranchesFast
{
    $old = ""
    $current = $pwd.Path
    $branches = @()

    while ($current -ne $old)
    {
        if (Test-Path "$current\.git")
        {
            $remotes = Get-Content -Force "$current\.git\FETCH_HEAD"
            #Find the word branch and create a group for the follow text inside single quotes
            $regex = [regex] "\bbranch\b\s*'(.*?)'"
            $branches = @( $regex.Matches($remotes) | ForEach-Object { $_.Groups[1].Value} )

            $locals = Get-Content -Force "$current\.git\config"
            #Find the word branch and create a group for the follow text inside double quotes
            $regex = [regex] '\bbranch\b\s*"(.*?)"'
            $branches += @( $regex.Matches($locals) | ForEach-Object { $_.Groups[1].Value} )
            $branches = $branches | Select-Object -Unique | Sort-Object

            return $branches
        }

        $old = $current
        $current = (Resolve-Path "$current\..").Path
    }

    return $null
}

function global:prompt
{
    Write-Host "PS " -NoNewline -ForegroundColor DarkGray

    # If inside a git reprository, print the branch name
    $gitBranch = Get-GitBranchFastMark
    if ($gitBranch)
    {
        if ($gitBranch.StartsWith("user/markind") -or $gitBranch.StartsWith("users/markind") -or $gitBranch.StartsWith("official/"))
        {
            $gitBranch = $gitBranch.Substring($gitBranch.LastIndexOf("/") + 1)
        }

        Write-Host "[" -NoNewline -ForegroundColor DarkGray
        Write-Host "$gitBranch" -NoNewline -ForegroundColor DarkCyan
        Write-Host "] " -NoNewline -ForegroundColor DarkGray
    }

    # Print the current location, shortend to 40 characters
    $location = (Get-Location).Path
    $shortened = $false
    $locationLength = 0 # Used to prevent infinite loop for a really long leaf directory name
    while ($location.Length -gt 40 -and $location.Length -ne $locationLength)
    {
        $locationLength = $location.Length
        $location = $location.Substring($location.IndexOf([System.IO.Path]::DirectorySeparatorChar) + 1)
        $shortened = $true
    }

    if ($shortened)
    {
        $location = "\$location"
    }

    Write-Host $location -NoNewline -ForegroundColor DarkCyan
    Write-Host ">" -NoNewline -ForegroundColor DarkGray

    return " " # Prevent powershell from using the default prompt
}

function global:TabExpansion($line, $lastWord)
{
    if ($line.StartsWith("git "))
    {
        $branches = Get-GitBranchesFast
        if ($branches)
        {
            # Filter list to only include matching branches
            return @( $branches | ForEach-Object { if ($_.StartsWith($lastWord, "CurrentCultureIgnoreCase")) { $_ } } )
        }
    }
}
