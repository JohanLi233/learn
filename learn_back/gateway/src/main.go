package main

import (
	"log"
	"net/http"
	"net/url"
)

var serverPool *ServerPool

func main() {
	serverPool = NewServerPool()

	// 初始化服务器池
	serverList := []string{
		"http://localhost:1234",
	}
	for _, s := range serverList {
		serverUrl, err := url.Parse(s)
		if err != nil {
			log.Fatal(err)
		}

		proxy := CreateReverseProxy(serverUrl)
		serverPool.AddServer(serverUrl, proxy)
		log.Printf("Configured server: %s\n", serverUrl)
	}

	log.Printf("Serving on http://localhost:3000\n")

	// 设置路由
	http.HandleFunc("/", lb)

	// 启动健康检查
	go HealthCheck()

	// 启动服务器
	log.Fatal(http.ListenAndServe(":3000", nil))
}

func lb(w http.ResponseWriter, r *http.Request) {
	attempts := GetAttemptsFromContext(r)
	if attempts > 3 {
		log.Printf("%s(%s) Max attempts reached, terminating\n", r.RemoteAddr, r.URL.Path)
		http.Error(w, "Service not available", http.StatusServiceUnavailable)
		return
	}

	peer := serverPool.GetNextPeer()
	if peer != nil {
		peer.ReverseProxy.ServeHTTP(w, r)
		return
	}
	http.Error(w, "Service not available", http.StatusServiceUnavailable)
}
