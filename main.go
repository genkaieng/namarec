package main

import (
	"bufio"
	"context"
	"fmt"
	"io"
	"net/http"
	"os"
	"os/exec"
	"os/signal"
	"regexp"
	"strconv"
	"strings"
	"syscall"
	"time"

	"github.com/gorilla/websocket"
)

const version = "v0.1.1"

func main() {
	args := os.Args
	if len(args) < 2 {
		fmt.Println("引数に生放送IDを指定してください")
		fmt.Println("namarec", "lv123456789")
		return
	}
	if args[1] == "-version" {
		fmt.Println("namarec", version, "Copyright (c) 2024 genkaieng")
		return
	}

	var lvid string
	if strings.HasPrefix(args[1], "lv") {
		lvid = args[1]
	}
	if len(lvid) == 0 {
		fmt.Println("生放送IDが不正")
		fmt.Println("namarec", "lv123456789")
		return
	}

	session := os.Getenv("SESSION")
	html, err := get(lvid, session)
	if err != nil {
		panic(err)
	}

	matches := regexp.MustCompile(`wss://[\w./?=+\-&#%]+`).FindAll(html, -1)
	wsUri := strings.TrimSuffix(string(matches[0]), "&quot")
	fmt.Println("DEBUG", "ws_uri:", wsUri)

	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	ctrlC := make(chan os.Signal, 1)
	defer close(ctrlC)
	signal.Notify(ctrlC, os.Interrupt, syscall.SIGINT, syscall.SIGTERM)
	go func() {
		<-ctrlC
		cancel()
	}()

	hlsUri, err := connect(ctx, wsUri)
	if err != nil {
		panic(err)
	}

	cmd := exec.Command("ffmpeg", "-y", "-i", string(hlsUri), "-acodec", "copy", "-vcodec", "copy", "-bsf:a", "aac_adtstoasc", lvid+".mp4")
	stdout, _ := cmd.StdoutPipe()
	go func() {
		scanner := bufio.NewScanner(stdout)
		for scanner.Scan() {
			fmt.Println("INFO", "FFmpeg:", scanner.Text())
		}
	}()
	stderr, _ := cmd.StderrPipe()
	go func() {
		scanner := bufio.NewScanner(stderr)
		for scanner.Scan() {
			fmt.Println("INFO", "FFmpeg:", scanner.Text())
		}
	}()

	if err := cmd.Run(); err != nil {
		fmt.Println("ERROR", "FFmpeg:", err)
	}
}

func get(lvid string, session string) ([]byte, error) {
	url := fmt.Sprintf("https://live.nicovideo.jp/watch/%s", lvid)

	req, err := http.NewRequest("GET", url, nil)
	if err != nil {
		return nil, err
	}
	if session != "" {
		req.AddCookie(&http.Cookie{
			Name:  "user_session",
			Value: session,
		})
	}

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("url: %s; StatusCode: %d", url, resp.StatusCode)
	}

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, err
	}

	return body, nil
}

func connect(ctx context.Context, uri string) ([]byte, error) {
	c, _, err := websocket.DefaultDialer.Dial(uri, nil)
	if err != nil {
		return nil, err
	}

	msgStream := make(chan []byte)
	keepIntervalSec := make(chan uint64)

	hlsUri := make(chan []byte)
	defer close(hlsUri)

	go func() {
		defer c.Close()
		defer close(keepIntervalSec)

	loop:
		for {
			select {
			case <-ctx.Done():
				break loop
			case msg := <-msgStream:
				fmt.Println("INFO", "ws: ⇓", string(msg))
				matches := regexp.MustCompile(`"type":"(\w+)"`).FindSubmatch(msg)
				if len(matches) == 0 {
					continue loop
				}
				msgType := string(matches[1])

				switch msgType {
				case "ping":
					c.WriteMessage(websocket.TextMessage, []byte(`{"type":"pong"}`))
					fmt.Println("INFO", "ws: ⇑", `{"type":"pong"}`)
					continue loop
				case "seat":
					interval := regexp.MustCompile(`"keepIntervalSec":(\d+)`).FindSubmatch(msg)[1]
					num, err := strconv.ParseUint(string(interval), 10, 64)
					if err != nil {
						fmt.Println(err)
						continue loop
					}
					keepIntervalSec <- num
				case "stream":
					uri := regexp.MustCompile(`"uri":"([^"]+)"`).FindSubmatch(msg)[1]
					hlsUri <- uri
				default:
					continue loop
				}
			}
		}
	}()
	go func() {
		sec := <-keepIntervalSec
		ticker := time.NewTicker(time.Duration(sec) * time.Second)
		defer ticker.Stop()

	keepSeat:
		for {
			select {
			case <-ctx.Done():
				break keepSeat
			case <-ticker.C:
				c.WriteMessage(websocket.TextMessage, []byte(`{"type":"keepSeat"}`))
				fmt.Println("INFO", "ws: ⇑", `{"type":"keepSeat"}`)
			case sec = <-keepIntervalSec:
				ticker.Reset(time.Duration(sec) * time.Second)
			}
		}
	}()
	go func() {
		defer close(msgStream)

	loop:
		for {
			_, msg, err := c.ReadMessage()
			if err != nil {
				fmt.Println("ERROR", err)
				break loop
			}
			msgStream <- msg
		}
	}()
	c.WriteMessage(websocket.TextMessage, []byte(`{"type":"startWatching","data":{"stream":{"quality":"abr","protocol":"hls+fmp4","latency":"low","chasePlay":false},"room":{"protocol":"webSocket","commentable":false},"reconnect":false}}`))

	return <-hlsUri, nil
}
