// Taken from https://gist.github.com/paulsmith/775764#file-echo-go

package main

import (
	"fmt"
	"net"
	"strconv"
)

const PORT = 25000

func main() {
	server, err := net.Listen("tcp", ":"+strconv.Itoa(PORT))
	if server == nil {
		panic("couldn't start listening: " + err.Error())
	}
	i := 0
	for {
		client, err := server.Accept()
		if client == nil {
			fmt.Printf("couldn't accept: " + err.Error())
			continue
		}
		i++
		fmt.Printf("%d: %v <-> %v\n", i, client.LocalAddr(), client.RemoteAddr())
		go handleConn(client)
	}
}

func handleConn(client net.Conn) {
    defer client.Close()
	buf := make([]byte, 102400)
	for {
		reqLen, err := client.Read(buf)
		if err != nil {
			break
		}
		if reqLen > 0 {
			client.Write(buf[:reqLen])
		}
	}
}
