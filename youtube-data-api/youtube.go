package main

import (
	"log"
	"net/http"

	"google.golang.org/api/googleapi/transport"
	"google.golang.org/api/youtube/v3"
)

var (
	client = &http.Client{
		Transport: &transport.APIKey{Key: developerKey},
	}
	service, err = youtube.New(client)
	maxResults   = int64(25)
)

const developerKey = "your key"

func getComments(VideoID string) map[string]string {
	call := service.CommentThreads.List("id,snippet").
		VideoId(VideoID).
		MaxResults(maxResults)
	response, err := call.Do()
	if err != nil {
		log.Fatalf("%v", err)
	}

	for _, item := range response.Items {
		println(item.Snippet.TopLevelComment.Snippet.TextDisplay)

	}
	videos := make(map[string]string)
	return videos
}

func getVideoIDs(channelID string) map[string]string {

	videos := make(map[string]string)
	return videos
}

func main() {
	getComments("Qs3sShlgKGk")
}
