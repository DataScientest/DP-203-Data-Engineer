# Purpose of the file
Write-Host "Importing CSV!!"

# Name of the CSV with email and passwords
$csvFile = 'user_to_deploy.csv'

# The ID of the DP203 session AD group
$TenantId = "79b1cadf-573c-4d97-95d0-00fb5675ff07"

# CSV import
## Inspiration: https://techexpert.tips/powershell/powershell-read-lines-from-csv-file/
Write-Host "Reading the CSV... "
$CSV = Import-Csv $csvFile

# Displaying the results
Write-Host "Here is the data: "
$CSV | Format-Table

foreach($LINE in $CSV)
{
    # starting the process
    "Starting with The ID: $($LINE.email), Name: $($LINE.password) and Tenant ID: $($TenantId)"

    # Creating ressourcess
    ./dp-203-setup.ps1 $TenantId $LINE.email $LINE.password

    # End of the process
    "Done with The ID: $($LINE.email), Name: $($LINE.password) and Tenant ID: $($TenantId)!!!!!"

    # cleaning
    Remove-Item -path ./azcopy_linux_amd64_10.16.* -Recurse
    Remove-Item -path ./azCopy.tar.gz

    # printing
    "Done! "
}

# cleaning
Write-Host "A Little cleaning..."
Remove-Item -path ./azcopy_linux_amd64_10.16.* -Recurse
Remove-Item -path ./azCopy.tar.gz
Write-Host "Done deal!!"