package vigenere

func EncryptVigenere(plaintext string, keyword string) string {
	var ciphertext string

	// PUT YOUR CODE HERE

	var i,j int
	i=0
	for j=0; j<len(plaintext);j++{
		var let int
		let=int(plaintext[j])
		if i>=len(keyword){
			i=0
		}
		if (int('A') <= let) && (let <= int('Z')) || (int('a') <= let && let <= int('z')){
			if (int('A') <= int(keyword[i])) && (int(keyword[i])<=int('Z')) {
				let = let + int(keyword[i]) - int('A')
			}else{
				let = let + int(keyword[i]) - int('a')
			}
		}
		if (int('Z')<let) && (int('a')>let) || (int('z')<let){
			let-=26
		}
		i+=1
		ciphertext+=string(let)
	}

	return ciphertext
}

func DecryptVigenere(ciphertext string, keyword string) string {
	var plaintext string

	// PUT YOUR CODE HERE

	var i,j int
	i=0
	for j=0; j<len(ciphertext);j++ {
		var let int
		let = int(ciphertext[j])
		if i >= len(keyword) {
			i = 0
		}
		if (int('A') <= let) && (let <= int('Z')) || (int('a') <= let && let <= int('z')) {
			if (int('A') <= int(keyword[i])) && (int(keyword[i]) <= int('Z')) {
				let = let - int(keyword[i]) + int('A')
			} else {
				let = let - int(keyword[i]) + int('a')
			}
		}
		if (int('Z') < let) && (int('a') > let) || (int('A') > let) {
			let += 26
		}
		i += 1

		plaintext += string(let)
	}
	return plaintext
}
