package vigenere


func EncryptVigenere(plaintext string, keyword string) string {
	var ciphertext string

	var i,j int
	i=0
	for j=0; j<len(plaintext);j++{
		let:=int(plaintext[j])
		comp:=int(plaintext[j])
		if i>=len(keyword){
			i=0
		}
		if (int('A') <= let) && (let <= int('Z')) || ((int('a') <= let) && (let <= int('z'))) {
			if (int('A') <= int(keyword[i])) && (int(keyword[i]) <= int('Z')) {
				let = let + int(keyword[i]) - int('A')
			}
			if (int('a') <= int(keyword[i])) && (int(keyword[i]) <= int('z')) {
				let = let + int(keyword[i]) - int('a')
			}
		}
			if (int('A') <= comp) && (comp <= int('Z') && (int('Z') < let)) || (int('a') <= comp) && (comp <= int('z') && (int('z') < let)){
				let-=26
			}
		i+=1
		ciphertext+=string(let)
	}

	return ciphertext
}

func DecryptVigenere(ciphertext string, keyword string) string {
	var plaintext string

	var i,j int
	i=0
	for j=0; j<len(ciphertext);j++ {
		let := int(ciphertext[j])
		comp := int(ciphertext[j])
		if (int('A') <= let) && (let <= int('Z')) || (int('a') <= let && let <= int('z')) {
			if i >= len(keyword) {
				i = 0
			}
			if (int('A') <= int(keyword[i])) && (int(keyword[i]) <= int('Z')) {
				let = let - int(keyword[i]) + int('A')
			}
			if (int('a') <= int(keyword[i])) && (int(keyword[i]) <= int('z')) {
				let = let - int(keyword[i]) + int('a')
			}
			if (int('A') <= comp) && (comp <= int('Z') && (int('A') > let)) || (int('a') <= comp) && (comp <= int('z') && (int('a') > let)) {
				let += 26
			}
		}
		i += 1

		plaintext += string(let)
	}
	return plaintext
}