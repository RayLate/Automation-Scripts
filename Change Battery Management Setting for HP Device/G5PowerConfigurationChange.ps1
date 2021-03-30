$hostname = Get-Content -Path C:\Temp\G5Hostlist.txt #get hostnames from text document

$cred = Get-Credential # get your adminstrative credential

$hostname | ForEach-Object -Process {

    If (Test-Connection $_ -Count 3 -ErrorAction SilentlyContinue){ # test if the hostname is online

        $result = Invoke-Command -Credential $cred -ComputerName $_ -ScriptBlock {
        $bios = Get-WmiObject -Namespace root/hp/instrumentedBIOS -Class HP_BIOSSettingInterface
        $bios.SetBIOSSetting("Battery Health Manager","Maximize my battery health").return} # $bios.SetBIOSSetting("<name of the setting>","<change to>") $result stores return code
        if ($result -eq 0) # return code = 0 means change is completed successfully
        {
            Write-Host $_ 'change success'
            Add-Content -Value $_ -Path C:\TEMP\Battery-Configure-change-success.txt
        }
        else
        {
            Write-Host $_ 'change fail' -ForegroundColor Red
            Add-Content -Value $_ -Path C:\TEMP\Battery-Configure-change-fail.txt
        }
    }
    else
    {
        Write-Host $_ 'is offline' -ForegroundColor blue
        Add-Content -Value $_ -Path C:\TEMP\Battery-Configure-device-offline.txt
    }
}
