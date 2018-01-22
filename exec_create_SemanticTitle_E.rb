#!/usr/local/rbenv/versions/2.3.0/bin/ruby


require 'matrix'
require './calcCosSim_E.rb'
require './create_title_pos_E.rb'
require 'cgi'

print("Content-type: text/html\n\n")
print("<title>TITLE GENERATOR</title>")

input = CGI.new
inputdata = input["senddata"]

#INPUT WORD
@word = inputdata.split(",")
#ARGV.each_with_index do |arg, i|
#    @word.push(arg)
#end

@filename = "titles_" + @word.join('＆') +".csv" 

#GET RELATED WORDS
relatedWords  = RelatedWords.new
word_id = relatedWords.wordsToIndex(@word)
titlePosObj = Title.new

@random = Random.new

#@csv = CSV.open('test.csv','w', :encoding => "utf-8")

outTitles = {}
titleNo = 1
20.times{
	titlePosObj.create
	titlePos = titlePosObj.titlePosA
	titleWords = titlePosObj.titleA

	#名詞変換
	meishiIndex = []
	meishiWords = []
	defaultIndex = [0,2]

	@meishi_x = [defaultIndex[@random.rand(0..(defaultIndex.length - 1))]]
	@doushi_x = -1

	i = 0
	titlePos.each do |pos|
		if  pos == "名詞" then
			meishiIndex.push(i)
		elsif pos == "x_meishi" then
			@meishi_x.push(i)
		elsif pos == "x_doushi" then
			@doushi_x  = i
		end
		i += 1	
	end

	meishiIndex.each do |idx|
		meishiWords.push(titleWords[idx])
	end

	begin
		print("###############<br />")
		#meishi
        	resultWord = relatedWords.getWords(meishiWords ,@word , "meishi", @meishi_x.length )
		
		j = 0
		@meishi_x.each do |idx|
	        	titleWords[idx] = resultWord[j]
			j += 1
		end

		#doushi
		if @doushi_x > -1 then
			resultWord2 = relatedWords.getWords(meishiWords ,@word, "doushi", 1)		
			titleWords[@doushi_x] = resultWord2[0]
		end
 		#puts titlePos.join(' ')
	        print(titleWords.join(' '))
		print("<br />")
		outTitles[titleNo.to_s] = titleWords.join(' ').to_s
	rescue => e
		print("error")
		print("<br />")
		outTitles[titleNo.to_s] = "*******"
	end
	titleNo += 1
}

#puts outTitles

#CSV.open(@filename,'w', :encoding => "utf-8") do |csv|
#	outTitles.each do |title|
#		csv << title
#	end
#end

