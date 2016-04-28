package main

import (
    "fmt"
    "net/http"
    "strconv"
    "strings"

    "github.com/golang/groupcache/lru"
)

var cache *lru.Cache

func handler(w http.ResponseWriter, r *http.Request) {
    var resp string

    respSize := r.URL.Path[1:]
    s, err := strconv.Atoi(respSize)
    if err != nil {
        s = 1024
    }

    val, ok := cache.Get(s)
    if ok {
        resp = val.(string)
    } else {
        resp = strings.Repeat("X", s)
        cache.Add(s, resp)
    }

    fmt.Fprintf(w, resp)
}

func main() {
    cache = lru.New(10)
    http.HandleFunc("/", handler)
    fmt.Println("Serving on :25000")
    http.ListenAndServe(":25000", nil)
}
