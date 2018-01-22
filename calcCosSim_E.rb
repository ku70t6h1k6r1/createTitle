require 'sqlite3'
require 'matrix'

class Matrix
  def []=(i,j,x)
    @rows[i][j]=x
  end
end

class RelatedWords
	def initialize()
		@db = SQLite3::Database.new 'word2vec.db'
		@random = Random.new
		vec_a = []
		temp_a = []
		@words_a = []

		@db.execute('select word_id, x, val  from articles_meishi order by word_id, x') do |row|
		 	if  row[1] < 199 then
				vec_a.push(row[2])	
			else
				vec_a.push(row[2])
				temp_a.push(vec_a)
				@words_a.push(row[0])
				vec_a = []
			end
		end

		vec2_a = []
                temp2_a = []
                @words2_a = []
                @db.execute('select word_id, x, val  from articles_doushi order by word_id, x') do |row|
                        if  row[1] < 199 then
                                vec2_a.push(row[2])
                        else
                                vec2_a.push(row[2])
                                temp2_a.push(vec2_a)
                                @words2_a.push(row[0])
                                vec2_a = []
                        end
                end

		@wsVec = Matrix.rows(temp_a, true)
		@wsVec2 = Matrix.rows(temp2_a, true)

		#puts "VECTRISE COMPLETED"
	end
	def get(wi, outn)
		#wiVec = Matrix.row_vector(@wsVec[wi])
		wiScore = Matrix.row_vector(@wsVec.row(@words_a.find_index(wi)).to_a) * @wsVec.t
		
		wiScoreA = []
		wiScore.each do |num|
			wiScoreA.push(num)
		end
		
		wiScoreSortedA = wiScoreA.sort{|a, b| b <=> a }
		
		i = 0
		
		output_w = []
		output_score = []
		output = {}
		loop{ 
			if wiScoreSortedA[outn] <= wiScoreA[i] then
				output_w.push(@words_a[i]) 
				output_score.push(wiScoreA[i])
			end
			
			i += 1
                        if output.length == outn || i >= wiScoreA.length then
                        	break
                        end	
		}
		output["words"] = output_w
		output["scores"]= output_score
		return output
	end
	def get_FromVec(wsVec, words_a, vec, outn)
		wiScore = Matrix.row_vector(vec) * wsVec.t

                wiScoreA = []
                wiScore.each do |num|
                        wiScoreA.push(num)
                end

                wiScoreSortedA = wiScoreA.sort{|a, b| b <=> a }

                i = 0

		output_w = []
		output_score = []
		output = {}
                loop{
                        if wiScoreSortedA[outn] <= wiScoreA[i] then
				output_w.push(words_a[i]) 
				output_score.push(wiScoreA[i])
                        end

                        i += 1
                        if output.length == outn || i >= wiScoreA.length then
                                break
                        end
                }
		output["words"] = output_w
		output["scores"]= output_score
		return output
	end
	def subtract(wi1_a, wi2_a, w1_a, w2_a)

		i = 0
		wi1_a.each do |wi1|
			if defined?(@vec_p) then 
				@vec_p = @vec_p + w1_a[i] * @wsVec.row(@words_a.find_index(wi1))
			else
				@vec_p = w1_a[i] * @wsVec.row(@words_a.find_index(wi1))
			end
			i += 1
		end

		i = 0
                wi2_a.each do |wi2|
                        if defined?(@vec_m) then
                                @vec_m = @vec_m + w2_a[i] * @wsVec.row(@words_a.find_index(wi2))
                        else
                                @vec_m = w2_a[i] * @wsVec.row(@words_a.find_index(wi2))
                        end
                        i += 1
                end

		vec  = @vec_p  - @vec_m
		vec_norm = vec.normalize		
		return vec_norm.to_a
	end
	def add(wi_a,  weight_a)		
		i = 0
		wi_a.each do |wi|
			if defined?(@vec) then 
				@vec = @vec + weight_a[i] * @wsVec.row(@words_a.find_index(wi))
			else
				@vec = weight_a[i] * @wsVec.row(@words_a.find_index(wi))
			end
			i += 0
		end
		vec_norm = @vec.normalize		
		return vec_norm.to_a
	end
	def add_vec(wi, vec, weight)
		sum_vec = Vector.elements(weight * @wsVec.row(@words_a.find_index(wi)).to_a ) + Vector.elements(vec)
		return sum_vec.normalize.to_a
	end
	def add_vecvec(vec1, vec2)
		sumvec = Vector.elements(vec1) + Vector.elements(vec2)
		return sumvec.normalize.to_a 
	end
	def wi2vec(wi)
		return (@wsVec.row(@words_a.find_index(wi))).to_a
	end
	def add_noize(vec)
		noize = Matrix.zero(vec.length)
		i = 0
		vec.length.times{
			noize[i,i] = @random.rand(0..1).to_f 
			i += 1
		}
		vec_w_noize = (Matrix.row_vector(vec) * noize).row(0).to_a
		return Vector.elements(vec_w_noize).normalize.to_a
	end
	def indexToWord(wi)
		@db.execute("select word from articles_vocab_control where word_id == #{wi}") do |row|
			@word  = row[0]
		end
		return @word
	end
	def indexToWords(wi_a)
                words = []
                wi_a.each do |w|
                        words.push(indexToWord(w))
                end
                return words
	end
        def wordToIndex(w)
                @db.execute("select word_id from articles_vocab_control where word == \"#{w}\"") do |row|
                        @index = row[0]
                end
                return @index
        end
	def wordsToIndex(w_a)
		index = []
		w_a.each do |w|
			index.push(wordToIndex(w))
		end
		return index
	end

####
	def getWords(preWs_a, inputWs_a, pos, n)
		preWs_a = wordsToIndex(preWs_a)
		inputWs_a = wordsToIndex(inputWs_a)
		inputWsVec_a = add(inputWs_a, Array.new(inputWs_a.length, 1.0))
				

		preW = Array.new(preWs_a.length, 0.2)
		inW = Array.new(inputWs_a.length, 1.0)
		weight_a = preW.concat(inW)
		#subVec = subtract([wordToIndex(preW)], wordsToIndex(preWs_a), [1], weight_a)
		sumWs = preWs_a
		sumWs.concat(inputWs_a)
		addVec = add(sumWs,weight_a )
		outputVec = add_vecvec( addVec, add_noize( inputWsVec_a  ) )
		if pos == "meishi" then
			outputWords = get_FromVec(@wsVec, @words_a, outputVec, 20)
		elsif pos == "doushi" then
			outputWords = get_FromVec(@wsVec2, @words2_a, outputVec, 40)
		else
			outputWords =Array.new(20,"" )
		end
		outputWords = outputWords["words"]
		return indexToWords(outputWords.sample(n))
		
	end
	
end





#test = RelatedWords.new

#INPUT WORD
#input = []
#ARGV.each_with_index do |arg, i|
#    input.push(arg)
#end

#tmpVec = test.add([test.wordToIndex(input[0]) , test.wordToIndex(input[1])] ,[1,1])
##noizeVec = test.add_vec(@random.rand(1..100000), tmpVec, 1.0)
#tmpVec2 = test.add_vecvec(tmpVec, test.add_noize(test.wi2vec(test.wordToIndex(input[3]))))
#result = test.get_FromVec(tmpVec, 10)

#result["words"].each do |wi|
#	puts test.indexToWord(wi)
#end

#result["scores"].each do |val|
#        puts val.to_f
#end

#puts "#### SUB ####"

#tmpVec = test.subtract([test.wordToIndex(input[0])], [test.wordToIndex(input[1])] ,[1],[input[2].to_i])
#result = test.get_FromVec(tmpVec, 10)

#result.each do |wi|
#	puts test.indexToWord(wi)
#end

#puts "#### ADD ####"
#tmpVec = test.add([test.wordToIndex(input[0]), test.wordToIndex(input[1])] ,[1,input[2].to_i])
#result = test.get_FromVec(tmpVec, 10)

#result.each do |wi|
#        puts test.indexToWord(wi)
#end
