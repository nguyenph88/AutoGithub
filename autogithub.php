<?php
$user = "testacc01";
$pass = "1qazxsw2";

$iMessage = "updated by AutoGithub nguyenph88@gmail.com - nguyenphuoc.net";
$iPath = "test.txt";
$iBodyContent = "update";
$iSHA = "87156ad20f45a3a90e01b3b3a65aa8d1252c2b2a";
$iRepo ="testrepo01";



editFileOnRepo($user, $pass, $iMessage, $iPath, $iBodyContent, $iRepo, $iSHA);

//return $this->client->request("/repos/$owner/$repo/readme", 'GET', $data, 200, 'GitHubReadmeContent');

function editFileOnRepo($username, $password, $message, $path, $bodyContent, $repo, $sha){
	$c = curl_init();
	$url = "/repos/:$username/$repo/contents/";

	curl_setopt($c, CURLOPT_VERBOSE, "false"); 
	curl_setopt($c, CURLOPT_HTTPAUTH, CURLAUTH_BASIC); 
	curl_setopt($c, CURLOPT_USERPWD, "$username:$password"); 
	curl_setopt($c, CURLOPT_RETURNTRANSFER, true);
	curl_setopt($c, CURLOPT_USERAGENT, "tan-tan.github-api");
	curl_setopt($c, CURLOPT_HEADER, true);
	curl_setopt($c, CURLOPT_FOLLOWLOCATION, true);
	//PUT /repos/:owner/:repo/contents/:path
			
	
	//curl_setopt($c, CURLOPT_CUSTOMREQUEST, 'PUT');
	//curl_setopt($c, CURLOPT_PUT, true);
	

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

	curl_setopt($c, CURLOPT_CUSTOMREQUEST, "PUT"); 
	curl_setopt($c, CURLOPT_POSTFIELDS,$content);
	//$fileName = tempnam(sys_get_temp_dir(), 'gitPut');
	//file_put_contents($fileName, $content);
	//$f = fopen($fileName, 'rb');
	//echo $f;
	//curl_setopt($c, CURLOPT_INFILE, $f);
	//curl_setopt($c, CURLOPT_INFILESIZE, strlen($content));
	
	error_log($url);


	curl_setopt($c, CURLOPT_URL, $url);
	curl_setopt($c, CURLOPT_SSL_VERIFYHOST, 0);
	curl_setopt($c, CURLOPT_SSL_VERIFYPEER, 0);

	$response = curl_exec($c);
	echo "response:".$response;
	curl_close($c);
}

?>