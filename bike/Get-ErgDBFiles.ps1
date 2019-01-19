<#
.Synopsis
    Download ERG DB files
.PARAMETER StartId
    The first ID to download
.PARAMETER EndId
    The last ID to download
.PARAMETER FTP
    FTP value in watts
.PARAMETER Destination
    Where to save the files to
.Example
    Download fitness routine

    .\Get-ErgDBFiles.ps1 -StartId 3778 -EndId 3796 -FTP 273 -Destination 273fitness
.Example
    Download climbs routine

    .\Get-ErgDBFiles.ps1 -StartId 3797 -EndId 3822 -FTP 273 -Destination 273climbs
.Example
    Download flats routine

    .\Get-ErgDBFiles.ps1 -StartId 3823 -EndId 3848 -FTP 273 -Destination 273flats
#>

Param(
    [Parameter(Mandatory = $True)][int] $StartId,
    [Parameter(Mandatory = $True)][int] $EndId,
    [Parameter(Mandatory = $True)][int] $FTP,
    [string] $Destination = ""
)

$destinationPath = Convert-Path .
if ($Destination -ne "")
{
    if (-not (Test-Path $Destination))
    {
        New-Item -ItemType Directory -Path $Destination | Out-Null
    }

    $destinationPath = Convert-Path $Destination
}

Write-Host "Downloading files ..."

for ($i = $StartId; $i -le $EndId; $i++)
{
    # Download the file
    $url = "http://73summits.com/ergdb/workout.php?recoveryftp=45&maxftp=125&type=5&ftp=$FTP&id=$i"
    $response = Invoke-WebRequest -Uri $url
    if ($response.StatusCode -ne 200)
    {
        Write-Error "Failed to download $url"
        Write-Error $response
        exit -1
    }

    # Get the target file name
    $index = $response.RawContent.IndexOf("filename=") + "filename=".Length
    $filename = $response.RawContent.SubString($index)
    $filenameLength = $filename.IndexOf("`n")
    $filename = $filename.SubString(0, $filenameLength).trim()
    $filePath = Join-Path -Path $destinationPath -ChildPath $filename

    # Save the file
    [System.IO.File]::WriteAllBytes($filePath, $response.Content)
    Write-Host $filePath
}

Write-Host "Done!"
