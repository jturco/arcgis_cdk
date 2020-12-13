# Params
$bucket_name = ''
$portal_license = ''
$ags_license = ''
$dsc_username = ''
$dsc_password = ''
$datastore_key = ''
$server_key = ''
$portal_key = ''
$web_adaptor_key = ''
$dsc_key = ''
$trusted_host_ip = '@{TrustedHosts="< ~ IP Address CSV String here ~ > "}'

# Download DSC Files and Add to Path
New-Item -Path "C:\" -Name "Software" -ItemType "directory" -Force
New-Item -Path "C:\" -Name "Deploy" -ItemType "directory" -Force
$url = 'https://github.com/Esri/arcgis-powershell-dsc/archive/master.zip'
$outpath = 'C:\Software\arcgis-powershell-dsc.zip'
Invoke-WebRequest -Uri $url -OutFile $outpath 
Expand-Archive -Path 'C:\Software\arcgis-powershell-dsc.zip' -DestinationPath 'C:\Software\arcgis-powershell-dsc'  -Force
Copy-Item -Path 'C:\Software\arcgis-powershell-dsc\arcgis-powershell-dsc-master\Modules\ArcGIS' -Destination 'C:\Program Files\WindowsPowerShell\Modules' -Force -Recurse

# Set Execution Policy
Set-ExecutionPolicy RemoteSigned -Force
winrm quickconfig -Force

# Create user for WinRM
$secureStringPwd = $dsc_password | ConvertTo-SecureString -AsPlainText -Force
$creds = New-Object System.Management.Automation.PSCredential -ArgumentList $dsc_username, $secureStringPwd
New-LocalUser -Name $creds.Username -Password $creds.Password
Add-LocalGroupMember -Group "Administrators" -Member $dsc_username

# Download software to C:\Software
Read-S3Object -BucketName $bucket_name -Key $ags_license -File "C:\Software\"$ags_license
Read-S3Object -BucketName $bucket_name -Key $portal_license -File "C:\Software\"$portal_license
Read-S3Object -BucketName $bucket_name -Key $datastore_key -File "C:\Software\"$datastore_key
Read-S3Object -BucketName $bucket_name -Key $server_key -File "C:\Software\"$server_key
Read-S3Object -BucketName $bucket_name -Key $portal_key -File "C:\Software\"$portal_key
Read-S3Object -BucketName $bucket_name -Key $web_adaptor_key -File "C:\Software\"$web_adaptor_key
Read-S3Object -BucketName $bucket_name -Key $dsc_key -File "C:\Deploy\"$dsc_key

# Set firewall rules
Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled False
#  Example - winrm s winrm/config/client '@{TrustedHosts="10.0.143.22,10.0.156.232,10.0.149.24,10.0.53.23,10.0.173.116,10.0.141.0,10.0.176.157,10.0.151.89"}'
winrm s winrm/config/client $trusted_host_ip

