package main

import (
	"fmt"
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
	order        = "relevance"
	searchTerms  = ""
	maxResults   = int64(5)
)

const developerKey = "your key"

func printComments(VideoID string) {
	call := service.CommentThreads.List("id,snippet").
		VideoId(VideoID).
		SearchTerms(searchTerms).
		Order(order).
		MaxResults(maxResults)
	response, err := call.Do()
	if err != nil {
		log.Fatalf("%v", err)
	}

	for _, item := range response.Items {
		authorName := item.Snippet.TopLevelComment.Snippet.AuthorDisplayName
		text := item.Snippet.TopLevelComment.Snippet.TextDisplay
		likeCnt := item.Snippet.TopLevelComment.Snippet.LikeCount
		replyCnt := item.Snippet.TotalReplyCount
		fmt.Printf("\"%v\" by %v\nいいね数: %d 返信数: %d\n\n", text, authorName, likeCnt, replyCnt)
	}
}

func main() {
	videoID := "Qs3sShlgKGk"
	printComments(videoID)
}
