#DSC Run
$username = '.\arcgis_service'
$password = '1qaz!QAZ2wsx@WSX'
$secureStringPwd = $password | ConvertTo-SecureString -AsPlainText -Force
$creds = New-Object System.Management.Automation.PSCredential -ArgumentList $username, $secureStringPwd
Invoke-ArcGISConfiguration -ConfigurationParametersFile C:\Deploy\DSCConfigurations.json -Mode InstallLicenseConfigure -Credential $creds
