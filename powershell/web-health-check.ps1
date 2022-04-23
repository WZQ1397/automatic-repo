$url_list=@('https://gateway.suncashlending.com/','https://manage-center.suncashlending.com/')

foreach($url in $url_list)
{
# First we create the request.
$HTTP_Request = [System.Net.WebRequest]::Create($url)

# We then get a response from the site.
$HTTP_Response = $HTTP_Request.GetResponse()

# We then get the HTTP code as an integer.
$HTTP_Status = [int]$HTTP_Response.StatusCode

If ($HTTP_Status -eq 200) {
    Write-Host $url " is OK!"
}
Else {
    Write-Host $url " may be down, please check!"
}

# Finally, we clean up the http request by closing it.
If ($HTTP_Response -eq $null) { } 
Else { $HTTP_Response.Close() }
}