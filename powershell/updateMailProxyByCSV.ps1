#Check account exist or not
function checkExist($account) {
    if ( [String]::IsNullOrEmpty($account)) {
        Write-Host "Param account is null or empty."
        return false;
    } else {
        Get-ADUser $account
        #True/False
        return $?
    }
}

#Change AD account mail proxy
function updateMailProxy($id,$s_mail,$s_mail_intl) {
    Set-MailContact -identity $id -externalemailaddress "$s_mail"
    New-TransportRule -Name "SH INTL Auto Forwarding $id" -SentTo $s_mail -RedirectMessageTo $s_mail_intl
}

#==============Main==================

#fetch current user
$curUser = $env:UserName;
Write-Host "Current User:$curUser";
$csvPath = "C:\Users\$curUser\Desktop\User_List.csv";
Write-Host "account file require: $csvPath";

#check file exist
if (-not(Test-Path $csvPath)) {
    Write-Host "Required File Not Exist, Task Abort!"
    return
}

#read csv file
$csvData = Import-Csv "$csvPath"

foreach ($result in $csvdata) {
    #match title
    $id=$result.id
    $name=$result.name
    $s_mail=$result.s_mail
    $s_int_mail=$result.s_int_mail


    #for test
    if($id -ne "lmaneneurrestara"){
        continue
    }

    Write-Host $id ---> $name $s_mail $s_int_mail

    $sourceExist = (checkExist $id);
    if (!$sourceExist) {
        Write-Host "Target account is not exist: $id,continue..."
        continue;
    }

    updateMailProxy $id $s_mail $s_int_mail
}
