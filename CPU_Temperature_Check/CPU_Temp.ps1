param([System.Management.Automation.PSCredential] $cred, [string] $computer = (Read-host -prompt "Enter Hostname "))
if ($computer -eq '') {
Write-Host "No input is given, checking CPU Temp for current device`n"
$computer = $env:COMPUTERNAME
}
else
{
    $cred = Get-Credential
}
write-host 'Running with full privileges'
Write-Host '----------------------------------------------------------------------------------'
Write-Host "Checking CPU Temp for $computer `n"


$t = Get-WmiObject MSAcpi_ThermalZoneTemperature -Namespace "root/wmi" -ComputerName $computer -Credential $cred
ForEach ($CpuTem in $t){

$InstanceName = $CpuTem.InstanceName -split '\\'
$Temp = $CpuTem.CurrentTemperature/10 -273.15


if ($Temp -lt 40){
$color = 'Green'
}elseif ($Temp -lt 60){
$color = 'Cyan'
}elseif ($Temp -lt 80){
$color = 'Yellow'
}elseif ($Temp -ge 80){
$color = 'Red'}


else {Write-Host $Temp 'deg C'
     Write-Host "Too hot"}



if ( $Temp -gt 30) {
Write-Host $InstanceName[2] 'Temperature : ' -NoNewline
Write-Host $temp 'deg C' -ForegroundColor $color


}
}