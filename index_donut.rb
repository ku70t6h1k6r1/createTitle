#!/usr/local/rbenv/versions/2.3.0/bin/ruby
# coding: utf-8

print("

<html>
<head>
<title>COMMENT GENERATOR</title>
</head>
<body>
<h1></h1>

<p>ニュースを下のフォームに入力してください。</p>
<p>AIがコメントします。</p>

<form action=\"donuts_client.py\" method=\"POST\" >
<!-- <input type=\"text\" name=\"senddata\" id = \"form\"> -->
<textarea type=\"text\" name=\"senddata\" id = \"form\" onkeyup=\"onkeyupEvent()\;\" cols=\"80\" rows=\"15\"></textarea></p>

<input type=\"submit\" value=\"投稿\" id = \"bottum\">
</form>
<div id = \"label\"> </div>
<script type=\"text/javascript\" src=\"http://ec2-34-230-144-25.compute-1.amazonaws.com/js/donut.js\"></script>
</body>
</html>


")
