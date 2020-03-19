package tensorflow

import (
	"io/ioutil"
	"log"
	"testing"
)

func TestSmokeTest(t *testing.T) {

	inputWeights0, err := ioutil.ReadFile("testData/0_trainingWeights.in")
	if err != nil {
		log.Fatal(err)
	}

	inputWeights1, err := ioutil.ReadFile("testData/1_trainingWeights.in")
	if err != nil {
		log.Fatal(err)
	}

	inputWeights := []string{string(inputWeights0), string(inputWeights1)}

	result := Aggregate(inputWeights)

	outputWeights, err := ioutil.ReadFile("testData/output.out")

	if result != string(outputWeights) {
		t.Errorf("Aggregation results do not match expected weights from %s", "testData/output.out")
	}
}