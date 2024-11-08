package main

import (
	"log"
	"net/http"
	"net/url"
	"time"
)

func HealthCheck() {
	t := time.NewTicker(time.Second * 20)
	for {
		select {
		case <-t.C:
			log.Println("Starting health check...")
			serverPool.HealthCheck()
			log.Println("Health check completed")
		}
	}
}

func (s *ServerPool) HealthCheck() {
	for _, server := range s.servers {
		status := "up"
		alive := isServerAlive(server.URL)
		server.SetAlive(alive)
		if !alive {
			status = "down"
		}
		log.Printf("%s [%s]\n", server.URL, status)
	}
}

func isServerAlive(u *url.URL) bool {
	resp, err := http.Head(u.String() + "/healthy")
	if err != nil {
		log.Printf("Error checking health: %v", err)
		return false
	}
	if resp.StatusCode != http.StatusOK {
		log.Printf("Status code: %v", resp.StatusCode)
		return false
	}
	return true
}
