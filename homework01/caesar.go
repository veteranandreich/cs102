package caesar

func EncryptCaesar(plaintext string, shift int) string {
	var ciphertext string
	var symbol int

	// PUT YOUR CODE HERE
	ciphertext=""
	for i:=0; i<len(plaintext);i++{
		symbol=int(plaintext[i])
		if (int('A')<=symbol)&&(int('Z')>=symbol) || (int('a')<=symbol)&&(int('z')>=symbol){
			symbol+=shift%26
		}
		if (symbol>int('Z')) && (symbol<int('a')) || (symbol>int('z')){
			symbol-=26
		}
		ciphertext+=string(symbol)
	}
	return ciphertext
}

func DecryptCaesar(ciphertext string, shift int) string {
	var plaintext string

	// PUT YOUR CODE HERE

	return plaintext
}