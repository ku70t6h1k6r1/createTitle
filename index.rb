#!/usr/local/rbenv/versions/2.3.0/bin/ruby
# coding: utf-8

print("

<html>
<head>
<title>TITLE GENERATOR</title>
</head>
<body>
<h1>タイトルジェネレーター</h1>

<p>キーワードから記事のタイトルを考案します。</p>
<p>・キーワードを下のフォームに入力して下さい。</p>
<p>・複数の場合は半角コンマ(\",\")で区切って下さい。</p>
<p>・名詞のみ対応しています。</p>
<form action=\"client.py\" method=\"POST\" >
<input type=\"text\" name=\"senddata\" id = \"form\">
<input type=\"submit\" value=\"生成\" id = \"bottum\">
</form>
<div id = \"label\"> </div>
<script type=\"text/javascript\" src=\"http://ec2-34-230-144-25.compute-1.amazonaws.com/js/createTitle.js\"></script>
</body>
</html>


")
