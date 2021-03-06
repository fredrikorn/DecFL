package storage

import (
	"io/ioutil"
	"strings"

	"github.com/FMorsbach/DecFL/model/common"
	shell "github.com/ipfs/go-ipfs-api"
)

type IPFS struct {
	connection string
	sh         *shell.Shell
}

func NewIPFS(connection string) (instance *IPFS) {

	return &IPFS{
		connection: connection,
		sh:         shell.NewShell(connection),
	}
}

func (ip *IPFS) Store(content string) (address common.StorageAddress, err error) {

	cid, err := ip.sh.Add(strings.NewReader(content))
	if err != nil {
		return
	}
	logger.Debugf("Wrote to address %s", cid)

	err = ip.sh.Pin(cid)
	if err != nil {
		return
	}
	logger.Debugf("Pinned address %s", cid)

	address = common.StorageAddress(cid)

	return
}

func (ip *IPFS) Load(address common.StorageAddress) (content string, err error) {

	reader, err := ip.sh.Cat(string(address))
	if err != nil {
		return
	}
	logger.Debugf("Loaded address %s", address)

	ip.sh.Pin(string(address))
	if err != nil {
		return
	}
	logger.Debugf("Pinned address %s", address)

	buffer, err := ioutil.ReadAll(reader)
	if err != nil {
		return
	}

	content = string(buffer)
	return
}

func (ip *IPFS) IsReachable() bool {
	return ip.sh.IsUp()
}
