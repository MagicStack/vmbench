// Taken from https://gist.github.com/paulsmith/775764#file-echo-go

package main

import (
    "net"
    "strconv"
    "fmt"
)

const PORT = 25000

func main() {
    server, err := net.Listen("tcp", ":" + strconv.Itoa(PORT))
    if server == nil {

        panic("couldn't start listening: " + err.Error())
    }
    conns := clientConns(server)
    for {
        go handleConn(<-conns)
    }
}

func clientConns(listener net.Listener) chan net.Conn {
    ch := make(chan net.Conn)
    i := 0
    go func() {
        for {
            client, err := listener.Accept()
            if client == nil {
                fmt.Printf("couldn't accept: " + err.Error())
                continue
            }
            i++
            fmt.Printf("%d: %v <-> %v\n", i, client.LocalAddr(), client.RemoteAddr())
            ch <- client
        }
    }()
    return ch
}

func handleConn(client net.Conn) {
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
