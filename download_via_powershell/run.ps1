#Given a file named $filePath, the program processes its content in chunks of 50 lines each. 
#It appends a "/" to the end of every line within the chunk and combines them into a link. 
#This link is then added to the end of a baseUrl. 
#The resulting link is automatically opened in the Microsoft Edge browser at specified intervals.
#MAKE SURE YOU ARE SIGNED INTO SALESFORCE IN EDGE 
#Result is a bunch of 50 files in a .ZIP

# Path to the file
$filePath = "INPUT DIRECTORY TO TEXT FILE HERE"

# URL
$prefix = "ADD SALESFORCE PREFIX HERE"
$baseUrl = -join("https://", $prefix, ".lightning.force.com/sfc/servlet.shepherd/document/download/")

$SleepTime = 0.5


$chuckSize = 50
$lines = Get-Content $filePath
$chunks = [System.Collections.Generic.List[string]]::new()
for ($i = 0; $i -lt $lines.Count; $i += $chuckSize) {
    $chunks.Add($lines[$i..($i + $chuckSize - 1)] -join "/")
}
$counter = 0
foreach ($chunk in $chunks) {
    $url = $baseUrl + $chunk
    Write-Host  $counter
    Start-Process -FilePath "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" -ArgumentList $url
    Start-Sleep -Seconds $SleepTime
}
