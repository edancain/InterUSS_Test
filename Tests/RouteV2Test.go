package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
)

const (
	// Move sensitive data like token and API key to environment variables or configuration files.
	Token  = "your-token"
	APIKey = "your-api-key"
)

type RouteV2Request struct {
	Client *http.Client
}

func NewRouteV2Request(client *http.Client) *RouteV2Request {
	return &RouteV2Request{client}
}

func (r *RouteV2Request) RequestRoute(resolution int, layers []map[string]interface{}, geometry map[string]interface{}) (map[string]interface{}, error) {
	header := map[string]string{
		"Content-Type":  "application/json",
		"Authorization": "Bearer " + Token,
		"X-API-Key":     APIKey,
	}

	data := map[string]interface{}{
		"resolution": resolution,
		"layers":     layers,
		"waypoints":  geometry,
	}

	jsonData, err := json.Marshal(data)
	if err != nil {
		return nil, fmt.Errorf("json marshal error: %v", err)
	}

	request, err := http.NewRequest("POST", "https://airhub-api-dev.airspacelink.com/v2/route", bytes.NewBuffer(jsonData))
	if err != nil {
		return nil, fmt.Errorf("create request error: %v", err)
	}

	for key, value := range header {
		request.Header.Set(key, value)
	}

	response, err := r.Client.Do(request)
	if err != nil {
		return nil, fmt.Errorf("request error: %v", err)
	}
	defer response.Body.Close()

	var responseData map[string]interface{}
	err = json.NewDecoder(response.Body).Decode(&responseData)
	if err != nil {
		return nil, fmt.Errorf("json decode error: %v", err)
	}

	return responseData, nil
}

func main() {
	client := &http.Client{}
	routeV2 := NewRouteV2Request(client)

	layers := []map[string]interface{}{
		{"code": "helipads", "risk": 5},
		{"code": "urgent_care", "risk": 5},
		{"code": "sport_venues", "risk": 5},
		{"code": "police_stations", "risk": 5},
		{"code": "hospitals", "risk": 5},
		{"code": "schools", "risk": 5},
		{"code": "airports", "risk": 5},
	}

	geometry := map[string]interface{}{
		"type":        "MultiPoint",
		"coordinates": [][]float64{{-120.01184223557765, 38.92798049239294}, {-120.00807001908422, 38.93377760076121}, {-120.01050530321129, 38.93760478709354}, {-120.01524562017035, 38.936448577383295}},
	}

	response, err := routeV2.RequestRoute(1, layers, geometry)
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		return
	}

	fmt.Println(response)
}

