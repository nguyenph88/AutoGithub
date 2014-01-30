<?php
$user = "yourusername";
$pass = "yourpassword";

$iMessage = "updated by AutoGithub nguyenph88@gmail.com - nguyenphuoc.net";
$iPath = "test.txt";
$iBodyContent = "dXBkYXRl";
$iSHA = "4f8a0fd8ab3537b85a64dcffa1487f4196164d78";
$iRepo ="yourrepo";



editFileOnRepo($user, $pass, $iMessage, $iPath, $iBodyContent, $iRepo, $iSHA);

//return $this->client->request("/repos/$owner/$repo/readme", 'GET', $data, 200, 'GitHubReadmeContent');

function editFileOnRepo($username, $password, $message, $path, $bodyContent, $repo, $sha){
	$c = curl_init();
	$url = "/repos/$username/$repo/contents/$path";
	//PUT /repos/:owner/:repo/contents/:path

	echo $url."\n";
	curl_setopt($c, CURLOPT_VERBOSE, "false"); 
	curl_setopt($c, CURLOPT_HTTPAUTH, CURLAUTH_BASIC); 
	curl_setopt($c, CURLOPT_USERPWD, "$username:$password"); 
	curl_setopt($c, CURLOPT_RETURNTRANSFER, true);
	curl_setopt($c, CURLOPT_USERAGENT, "testacc01");
	curl_setopt($c, CURLOPT_HEADER, true);
	curl_setopt($c, CURLOPT_FOLLOWLOCATION, true);
	
	curl_setopt($c, CURLOPT_CUSTOMREQUEST, 'PUT');
	curl_setopt($c, CURLOPT_PUT, true);
	
	$data = array();
	$data['path'] = $path;
	$data['message'] = $message;
	$data['content'] = $bodyContent;
	$data['sha'] = $sha;

	$content = json_encode($data, JSON_FORCE_OBJECT);

	$headers = array(
		'X-HTTP-Method-Override: PUT', 
		'Content-type: application/json',
		'Content-Length: ' . strlen($content)
	);
	curl_setopt($c, CURLOPT_HTTPHEADER, $headers);
	
	echo $content;

	
	$fp = fopen('php://temp/maxmemory:256000', 'w');
	if (!$fp) {
	    die('could not open temp memory data');
	}
	fwrite($fp, $content);
	fseek($fp, 0); 

	echo $fp;

	curl_setopt($c, CURLOPT_BINARYTRANSFER, true);
	curl_setopt($c, CURLOPT_INFILE, $fp); // file pointer
	curl_setopt($c, CURLOPT_INFILESIZE, strlen($content));   
	
	error_log($url);

	curl_setopt($c, CURLOPT_URL, $url);
	curl_setopt($c, CURLOPT_SSL_VERIFYHOST, 0);
	curl_setopt($c, CURLOPT_SSL_VERIFYPEER, 0);

	$response = curl_exec($c);
	echo "\nresponse:".$response;
	curl_close($c);
}

?>
