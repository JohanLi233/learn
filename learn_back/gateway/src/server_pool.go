package main

import (
	"net/http/httputil"
	"net/url"
)

type ServerPool struct {
	servers []*Server
	current int
}

func NewServerPool() *ServerPool {
	return &ServerPool{}
}

func (s *ServerPool) AddServer(serverUrl *url.URL, proxy *httputil.ReverseProxy) {
	s.servers = append(s.servers, &Server{
		URL:          serverUrl,
		Alive:        true,
		ReverseProxy: proxy,
	})
}

func (s *ServerPool) NextIndex() int {
	return (s.current + 1) % len(s.servers)
}

func (s *ServerPool) GetNextPeer() *Server {
	next := s.NextIndex()
	l := len(s.servers) + next
	for i := next; i < l; i++ {
		idx := i % len(s.servers)
		if s.servers[idx].IsAlive() {
			if i != next {
				s.current = idx
			}
			return s.servers[idx]
		}
	}
	return nil
}

func (s *ServerPool) MarkServerStatus(url *url.URL, alive bool) {
	for _, server := range s.servers {
		if server.URL.String() == url.String() {
			server.SetAlive(alive)
			break
		}
	}
}
