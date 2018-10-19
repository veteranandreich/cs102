package rsa

import (
    "errors"
    "math"
    "math/big"
    "math/rand"
)

type Key struct {
    key int
    n int
}

type KeyPair struct {
    Private Key
    Public Key
}

func isPrime(n int) bool {
    f:=int(math.Sqrt(float64(n))+1)
    for i:=2; i<f; i++{
        if (n%i==0){
            return false
        }
    }
    return true
}


func gcd(a int, b int) int {
    for (a!=0) && (b!=0) {
        if (a > b) {
            a = a % b
        } else {
            b = b % a
        }
    }
    c:=a+b
    return c
}


func multiplicativeInverse(e int, phi int) int {
    var tabl [][]int
    row := []int{phi, e, phi % e, phi / e, -1, -1}
    tabl=append(tabl,row)
    for i:=1;phi%e!=0;i++{
        c:=phi%e
        phi=e
        e=c
        row := []int{phi, e, phi % e, phi / e, -1, -1}
        tabl=append(tabl,row)
    }
    tabl[len(tabl)-1][4]=0
    tabl[len(tabl)-1][5]=1
    for i := len(tabl)-2; i >= 0; i-- {
        tabl[i][4] = tabl[i+1][5]
        tabl[i][5] = tabl[i+1][4] - tabl[i+1][5]*tabl[i][3]
    }
    d:=tabl[0][5]%tabl[0][0]
    if d<0{
        d+=tabl[0][0]
    }
    return d
}


func GenerateKeypair(p int, q int) (KeyPair, error) {
    if !isPrime(p) || !isPrime(q) {
        return KeyPair{}, errors.New("Both numbers must be prime.")
    } else if  p == q {
        return KeyPair{}, errors.New("p and q can't be equal.")
    }
    n:=p*q
    phi:= (p-1)*(q-1)
    e := rand.Intn(phi - 1) + 1
    g := gcd(e, phi)
    for g != 1 {
        e = rand.Intn(phi - 1) + 1
        g = gcd(e, phi)
    }

    d := multiplicativeInverse(e, phi)
    return KeyPair{Key{e, n}, Key{d, n}}, nil
}


func Encrypt(pk Key, plaintext string) []int {
    cipher := []int{}
    n := new(big.Int)
    for _, ch := range plaintext {
        n = new(big.Int).Exp(
            big.NewInt(int64(ch)), big.NewInt(int64(pk.key)), nil)
        n = new(big.Int).Mod(n, big.NewInt(int64(pk.n)))
        cipher = append(cipher, int(n.Int64()))
    }
    return cipher
}


func Decrypt(pk Key, cipher []int) string {
    plaintext := ""
    n := new(big.Int)
    for _, ch := range cipher {
        n = new(big.Int).Exp(
            big.NewInt(int64(ch)), big.NewInt(int64(pk.key)), nil)
        n = new(big.Int).Mod(n, big.NewInt(int64(pk.n)))
        plaintext += string(rune(int(n.Int64())))
    }
    return plaintext
}