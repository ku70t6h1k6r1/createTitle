require 'mysql2'
require 'sqlite3'
require 'matrix'


#######################


class SqlSet
	def initialize()
		@db = SQLite3::Database.new 'word2vec.db'
	end
	def select107
		result = []
		@db.execute('select * from sample_107 ') do |row|
			result.push(row)
		end
		return result
	end
	def select622
		result = []
		@db.execute('select * from sample_622 ') do |row|
			result.push(row)
		end
		return result
	end
end


#######################

class Title
	def initialize()
		@random = Random.new
		@kigo_a = ["!","?","!?","…"]	
		word_a = []
		pos_a = []

		@sql = SqlSet.new
		@result_a = @sql.select622
		@result2_a = @sql.select107
	end
	def create
		tmpTitle = @result_a[@random.rand(0..(@result_a.length - 1))]
		if tmpTitle[11] == 1064 then
			@title = [tmpTitle[2], tmpTitle[3], tmpTitle[4], tmpTitle[5], "…"]
			@titlePos = [tmpTitle[6], tmpTitle[7], tmpTitle[8], tmpTitle[9], "記号"]
		else
			@title = [tmpTitle[2], tmpTitle[3], tmpTitle[4],@kigo_a[@random.rand(0..3)]]
			@titlePos = [tmpTitle[6], tmpTitle[7], tmpTitle[8],"記号"]
		end

		tmpTitle2 = @result2_a[@random.rand(0..(@result2_a.length - 1))]
		case tmpTitle2[11]
		when 537 then
                        @title2 = [tmpTitle2[2], tmpTitle2[3], tmpTitle2[4], "x_doushi"]
                        @titlePos2 = [tmpTitle2[6], tmpTitle2[7], tmpTitle2[8], "x_doushi"]
		when 543 then
                        @title2 = [tmpTitle2[2], tmpTitle2[3], tmpTitle2[4],@kigo_a[@random.rand(0..3)]]
                        @titlePos2 = [tmpTitle2[6], tmpTitle2[7], tmpTitle2[8],"記号"]
		when 539 then
                        @title2 = [tmpTitle2[2], tmpTitle2[3], tmpTitle2[4], tmpTitle2[5] ,"x_mesihi"]
                        @titlePos2 = [tmpTitle2[6], tmpTitle2[7], tmpTitle2[8], tmpTitle[9],"x_meishi"]
		when  536 then
                        @title2 = [tmpTitle2[2], tmpTitle2[3], tmpTitle2[4], tmpTitle2[5], "…"]
                        @titlePos2 = [tmpTitle2[6], tmpTitle2[7], tmpTitle2[8], tmpTitle2[9], "記号"]
		when 535 then
			@title2 = [tmpTitle2[2], tmpTitle2[3], tmpTitle2[4],tmpTitle2[5]]
                        @titlePos2 = [tmpTitle2[6], tmpTitle2[7], tmpTitle2[8],tmpTitle2[9]]	
		when 542 then
                        @title2 = [tmpTitle2[2], tmpTitle2[3], tmpTitle2[4], tmpTitle2[5], "…"]
                        @titlePos2 = [tmpTitle2[6], tmpTitle2[7], tmpTitle2[8], tmpTitle2[9], "記号"]
		when 534 then
                        @title2 = [tmpTitle2[2], tmpTitle2[3], tmpTitle2[4],tmpTitle2[5], @kigo_a[@random.rand(0..3)]]
                        @titlePos2 = [tmpTitle2[6], tmpTitle2[7], tmpTitle2[8],tmpTitle2[9], "記号"]
                when 544 then
                        @title2 = [tmpTitle2[2], tmpTitle2[3], tmpTitle2[4], tmpTitle2[5], "…"]
                        @titlePos2 = [tmpTitle2[6], tmpTitle2[7], tmpTitle2[8], tmpTitle2[9], "記号"]
		when 538 then
                        @title2 = [tmpTitle2[2], tmpTitle2[3], tmpTitle2[4],"x_meishi"]
                        @titlePos2 = [tmpTitle2[6], tmpTitle2[7], tmpTitle2[8],"x_meishi"]
		else
			@title2 = [tmpTitle2[2], tmpTitle2[3], tmpTitle2[4],tmpTitle2[5]]
                        @titlePos2 = [tmpTitle2[6], tmpTitle2[7], tmpTitle2[8],tmpTitle2[9]]
		end
	end
	def title
		output = @title.join("/") + "/ / " + @title2.join("/") 
		return output
	end
	
	def titlePos
		output = @titlePos.join("/") + "/ /" + @titlePos2.join("/")
		return output
	end

	#def totalPageRank
	#	output =  ( Vector.elements(@pagerank)  / @pagerank.length ).to_a 
	#	return output.inject(:+) 
	#end

	def titlePosA
		return @titlePos.concat([" "]).concat(@titlePos2)
	end

	def titleA
		return @title.concat([" "]).concat(@title2)
	end
end

#test = Title.new
#100.times{
#	test.create
#	puts "######"
#	puts test.title
#	puts test.titlePos
#}
