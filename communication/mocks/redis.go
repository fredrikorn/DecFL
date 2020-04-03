package mocks

import (
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"log"
	"math/rand"
	"os"
	"strconv"
	"time"

	c "github.com/FMorsbach/DecFL/communication"
	"github.com/FMorsbach/dlog"
	"github.com/go-redis/redis"
)

const MODEL_CONFIG_KEY string = "globalModelConfiguration"
const MODEL_WEIGHTS_KEY string = "globalModelWeights"
const ITERATIONS_KEY string = "iteration"
const LOCAL_UPDATES_KEY string = "localUpdates"
const MODEL_EPOCH_KEY string = "epoch"

var logger = dlog.New(os.Stderr, "Redis: ", log.LstdFlags, false)

func EnableDebug(b bool) {
	logger.SetDebug(b)
}

type Redis struct {
	client *redis.Client
}

func NewRedis(connection string) (instance *Redis) {

	client := redis.NewClient(&redis.Options{
		Addr:     connection,
		Password: "",
		DB:       0,
	})

	return &Redis{client: client}
}

func (r *Redis) DeployModel(configAddress c.StorageAddress, weightsAddress c.StorageAddress) (id c.ModelIdentifier, err error) {

	rand.Seed(time.Now().UnixNano())
	id = c.ModelIdentifier(strconv.Itoa(rand.Intn(10000)))
	logger.Debugf("Generated %s as model id", id)

	err = r.client.Set(key(id, MODEL_CONFIG_KEY), string(configAddress), 0).Err()
	if err != nil {
		return
	}
	logger.Debugf("Wrote configuration to %s", key(id, MODEL_CONFIG_KEY))

	err = r.client.Set(key(id, MODEL_WEIGHTS_KEY), string(weightsAddress), 0).Err()
	if err != nil {
		return
	}
	logger.Debugf("Wrote weights to %s", key(id, MODEL_WEIGHTS_KEY))

	err = r.client.Set(key(id, MODEL_EPOCH_KEY), strconv.Itoa(0), 0).Err()
	if err != nil {
		return
	}
	logger.Debugf("Wrote model epoch to %s", key(id, MODEL_EPOCH_KEY))

	return
}

func (r *Redis) ModelConfigurationAddress(id c.ModelIdentifier) (address c.StorageAddress, err error) {

	temp, err := r.client.Get(key(id, MODEL_CONFIG_KEY)).Result()
	if err != nil {
		return
	}
	address = c.StorageAddress(temp)

	return
}

func (r *Redis) GlobalWeightsAddress(id c.ModelIdentifier) (address c.StorageAddress, err error) {

	temp, err := r.client.Get(key(id, MODEL_WEIGHTS_KEY)).Result()
	if err != nil {
		return
	}
	address = c.StorageAddress(temp)

	return
}

func (r *Redis) PublishNewModelWeights(id c.ModelIdentifier, address c.StorageAddress) (err error) {

	err = r.client.Set(key(id, MODEL_WEIGHTS_KEY), string(address), 0).Err()
	if err != nil {
		return
	}
	logger.Debugf("Wrote weights to %s", key(id, MODEL_WEIGHTS_KEY))

	epoch, err := r.ModelEpoch(id)
	if err != nil {
		return
	}

	err = r.client.Set(key(id, MODEL_EPOCH_KEY), strconv.Itoa(epoch+1), 0).Err()
	if err != nil {
		return
	}
	logger.Debugf("Wrote model epoch to %s", key(id, MODEL_EPOCH_KEY))

	return
}

func (r *Redis) SubmitLocalUpdate(modelID c.ModelIdentifier, update c.Update) (err error) {

	data, err := json.Marshal(update)
	if err != nil {
		return
	}
	err = r.client.SAdd(key(modelID, LOCAL_UPDATES_KEY), data).Err()
	if err != nil {
		return
	}
	logger.Debugf("Appended %s to %s", update.Address, key(modelID, LOCAL_UPDATES_KEY))

	return
}

func (r *Redis) LocalUpdates(id c.ModelIdentifier) (addresses []c.Update, err error) {

	temp, err := r.client.SMembers(key(id, LOCAL_UPDATES_KEY)).Result()
	if err != nil {
		return
	}

	addresses = make([]c.Update, len(temp))
	for i, t := range temp {
		var data c.Update
		err = json.Unmarshal([]byte(t), &data)
		if err != nil {
			return
		}
		addresses[i] = data
	}

	return
}

func (r *Redis) ClearLocalUpdateAddresses(id c.ModelIdentifier) (err error) {

	err = r.client.Del(key(id, LOCAL_UPDATES_KEY)).Err()
	if err != nil {
		return
	}
	logger.Debugf("Reset local update store at %s", key(id, LOCAL_UPDATES_KEY))

	return
}

func (r *Redis) ModelEpoch(id c.ModelIdentifier) (epoch int, err error) {

	temp, err := r.client.Get(key(id, MODEL_EPOCH_KEY)).Result()
	if err != nil {
		return
	}

	epoch, err = strconv.Atoi(temp)
	if err != nil {
		return
	}

	return
}

func (r *Redis) FlushRedis() (err error) {
	err = r.client.FlushAll().Err()
	if err != nil {
		return
	}
	logger.Debugf("Flushed redis at %s", r.client.Options().Addr)

	return
}

func (r *Redis) IsReachable() (reachable bool, err error) {
	pong, err := r.client.Ping().Result()

	if err != nil || pong != "PONG" {
		return false, fmt.Errorf("%s, expected PONG but got %s", err, pong)
	} else {
		return true, err
	}
}

func key(id c.ModelIdentifier, key string) string {
	return fmt.Sprintf("%s-%s", string(id), key)
}

func (r *Redis) Store(content string) (address c.StorageAddress, err error) {

	h := sha256.Sum256([]byte(content))
	dh := h[0:32]
	address = c.StorageAddress(hex.EncodeToString(dh))

	err = r.client.Set(string(address), content, 0).Err()
	if err != nil {
		return
	}
	logger.Debugf("Saved update with key %s\n", address)

	return
}

func (r *Redis) Load(address c.StorageAddress) (content string, err error) {

	content, err = r.client.Get(string(address)).Result()
	if err == redis.Nil {
		err = fmt.Errorf("Key %s does not exist: %s", address, err)
		return
	} else if err != nil {
		return
	}

	return
}
